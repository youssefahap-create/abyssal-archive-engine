import os
import json
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from pathlib import Path

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from config.settings import YOUTUBE_SETTINGS, SCHEDULE_SETTINGS
from config.secrets_manager import secrets_manager
from utils.logger import logger
from services.seo_optimizer import SEOOptimizer


class YouTubeUploader:
    """فئة رفع الفيديوهات إلى يوتيوب"""
    
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    def __init__(self):
        self.seo_optimizer = SEOOptimizer()
        self.credentials = None
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """المصادقة مع YouTube API"""
        try:
            # استخدام Refresh Token إذا كان متوفراً
            refresh_token = secrets_manager.get_api_key("youtube_refresh")
            
            if refresh_token:
                # هناك طريقة للحصول على Credentials من Refresh Token
                # لكننا سنستخدم الطريقة القياسية مع ملف client_secret
                pass
            
            # المحاولة باستخدام OAuth 2.0
            creds = None
            token_file = "token.json"
            
            if os.path.exists(token_file):
                creds = Credentials.from_authorized_user_file(token_file, self.SCOPES)
            
            # إذا لم توجد بيانات اعتماد صالحة
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    # محاولة استخدام Client ID و Secret
                    client_id = secrets_manager.get_api_key("youtube_client_id")
                    client_secret = secrets_manager.get_api_key("youtube_client_secret")
                    
                    if client_id and client_secret:
                        # إنشاء Flow
                        flow = InstalledAppFlow.from_client_config(
                            {
                                "web": {
                                    "client_id": client_id,
                                    "client_secret": client_secret,
                                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                                    "token_uri": "https://oauth2.googleapis.com/token"
                                }
                            },
                            self.SCOPES
                        )
                        
                        # الحصول على Credentials
                        creds = flow.run_local_server(port=0)
                    
                    else:
                        logger.error("YouTube authentication failed: No credentials available")
                        return
                
                # حفظ Credentials للمرة القادمة
                with open(token_file, 'w') as token:
                    token.write(creds.to_json())
            
            self.credentials = creds
            self.service = build('youtube', 'v3', credentials=creds)
            logger.info("YouTube authentication successful")
            
        except Exception as e:
            logger.error(f"YouTube authentication failed: {e}")
    
    def upload_short(self, video_path: str, question_data: dict, 
                    schedule_time: datetime = None) -> Optional[str]:
        """رفع فيديو شورت إلى يوتيوب"""
        
        if not self.service:
            logger.error("YouTube service not initialized")
            return None
        
        try:
            # تحسين SEO
            title = self.seo_optimizer.generate_title(question_data)
            description = self.seo_optimizer.generate_description(question_data)
            tags = self.seo_optimizer.generate_tags(question_data)
            
            # إعداد بيانات الفيديو
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags,
                    'categoryId': YOUTUBE_SETTINGS["category_id"],
                    'defaultLanguage': YOUTUBE_SETTINGS["default_language"]
                },
                'status': {
                    'privacyStatus': YOUTUBE_SETTINGS["privacy_status"],
                    'selfDeclaredMadeForKids': False
                }
            }
            
            # إذا كان هناك وقت جدولة
            if schedule_time:
                # تحويل إلى تنسيق RFC 3339
                scheduled_time_rfc3339 = schedule_time.isoformat() + 'Z'
                body['status']['publishAt'] = scheduled_time_rfc3339
            
            # رفع الفيديو
            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
            
            request = self.service.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    logger.info(f"Upload progress: {int(status.progress() * 100)}%")
            
            video_id = response['id']
            logger.info(f"Video uploaded successfully: {video_id}")
            
            # حفظ معلومات الرفع
            self._save_upload_info(video_id, video_path, question_data, title)
            
            return video_id
            
        except Exception as e:
            logger.error(f"Error uploading video: {e}")
            return None
    
    def upload_compilation(self, video_path: str, shorts_data: List[dict],
                          schedule_time: datetime = None) -> Optional[str]:
        """رفع فيديو تجميعي"""
        
        if not self.service:
            logger.error("YouTube service not initialized")
            return None
        
        try:
            # إنشاء عنوان ووصف للتجميع
            today = datetime.now().strftime("%B %d, %Y")
            title = f"Daily Brain Teasers Compilation - {today} | Test Your Knowledge!"
            
            # إنشاء وصف التجميع
            description = f"🎯 Daily Brain Teasers Compilation - {today}\n\n"
            description += "Can you solve all these puzzles? Test your knowledge with today's compilation!\n\n"
            
            for i, data in enumerate(shorts_data, 1):
                description += f"{i}. {data.get('question', '')}\n"
            
            description += "\n🔔 Subscribe for daily brain teasers!\n"
            description += "💬 Comment your score below!\n\n"
            description += "#brainteaser #quiz #compilation #dailyquiz #trivia"
            
            # إعداد بيانات الفيديو
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': ['compilation', 'brainteaser', 'quiz', 'daily', 'trivia', 
                            'puzzle', 'knowledge', 'test', 'challenge'],
                    'categoryId': YOUTUBE_SETTINGS["category_id"],
                    'defaultLanguage': YOUTUBE_SETTINGS["default_language"]
                },
                'status': {
                    'privacyStatus': YOUTUBE_SETTINGS["privacy_status"],
                    'selfDeclaredMadeForKids': False
                }
            }
            
            # إذا كان هناك وقت جدولة
            if schedule_time:
                scheduled_time_rfc3339 = schedule_time.isoformat() + 'Z'
                body['status']['publishAt'] = scheduled_time_rfc3339
            
            # رفع الفيديو
            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
            
            request = self.service.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    logger.info(f"Compilation upload progress: {int(status.progress() * 100)}%")
            
            video_id = response['id']
            logger.info(f"Compilation uploaded successfully: {video_id}")
            
            return video_id
            
        except Exception as e:
            logger.error(f"Error uploading compilation: {e}")
            return None
    
    def _save_upload_info(self, video_id: str, video_path: str, 
                         question_data: dict, title: str):
        """حفظ معلومات الرفع"""
        
        uploads_dir = Path("assets/uploads")
        uploads_dir.mkdir(exist_ok=True)
        
        info_file = uploads_dir / f"upload_{video_id}.json"
        info = {
            "video_id": video_id,
            "video_path": video_path,
            "question": question_data["question"],
            "answer": question_data["answer"],
            "category": question_data.get("category", "general"),
            "title": title,
            "uploaded_at": datetime.now().isoformat(),
            "scheduled": False
        }
        
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
    
    def check_upload_status(self, video_id: str) -> Dict:
        """التحقق من حالة الفيديو"""
        
        if not self.service:
            return {"error": "Service not initialized"}
        
        try:
            request = self.service.videos().list(
                part="status,snippet,statistics",
                id=video_id
            )
            response = request.execute()
            
            if response['items']:
                video = response['items'][0]
                return {
                    "status": video['status']['uploadStatus'],
                    "privacy": video['status']['privacyStatus'],
                    "title": video['snippet']['title'],
                    "view_count": video['statistics'].get('viewCount', 0),
                    "like_count": video['statistics'].get('likeCount', 0),
                    "comment_count": video['statistics'].get('commentCount', 0)
                }
            
            return {"error": "Video not found"}
            
        except Exception as e:
            return {"error": str(e)}
    
    def update_video_details(self, video_id: str, updates: Dict) -> bool:
        """تحديث تفاصيل الفيديو"""
        
        if not self.service:
            return False
        
        try:
            # الحصول على الفيديو الحالي أولاً
            request = self.service.videos().list(
                part="snippet",
                id=video_id
            )
            response = request.execute()
            
            if not response['items']:
                return False
            
            video = response['items'][0]
            snippet = video['snippet']
            
            # تحديث الحقول المطلوبة
            if 'title' in updates:
                snippet['title'] = updates['title']
            if 'description' in updates:
                snippet['description'] = updates['description']
            if 'tags' in updates:
                snippet['tags'] = updates['tags']
            if 'category_id' in updates:
                snippet['categoryId'] = updates['category_id']
            
            # تحديث الفيديو
            update_request = self.service.videos().update(
                part="snippet",
                body={
                    "id": video_id,
                    "snippet": snippet
                }
            )
            update_request.execute()
            
            logger.info(f"Video {video_id} updated successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error updating video {video_id}: {e}")
            return False
    
    def delete_video(self, video_id: str) -> bool:
        """حذف فيديو"""
        
        if not self.service:
            return False
        
        try:
            request = self.service.videos().delete(id=video_id)
            request.execute()
            
            logger.info(f"Video {video_id} deleted successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting video {video_id}: {e}")
            return False
    
    def get_channel_stats(self) -> Dict:
        """الحصول على إحصائيات القناة"""
        
        if not self.service:
            return {"error": "Service not initialized"}
        
        try:
            channel_id = secrets_manager.get_api_key("youtube_channel_id")
            if not channel_id:
                return {"error": "Channel ID not configured"}
            
            request = self.service.channels().list(
                part="statistics,snippet",
                id=channel_id
            )
            response = request.execute()
            
            if response['items']:
                channel = response['items'][0]
                return {
                    "title": channel['snippet']['title'],
                    "subscribers": channel['statistics'].get('subscriberCount', '0'),
                    "views": channel['statistics'].get('viewCount', '0'),
                    "videos": channel['statistics'].get('videoCount', '0')
                }
            
            return {"error": "Channel not found"}
            
        except Exception as e:
            return {"error": str(e)}
