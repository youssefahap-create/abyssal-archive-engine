from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from config.settings import *
from config.secrets_manager import SecretsManager

class YouTubeManager:
    def __init__(self, secrets_manager: SecretsManager):
        self.secrets = secrets_manager
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """المصادقة مع يوتيوب API"""
        try:
            # استخدام refresh token إذا كان متاحاً
            refresh_token = self.secrets.get_key("youtube", "refresh")
            
            if refresh_token:
                credentials = google.oauth2.credentials.Credentials(
                    token=None,
                    refresh_token=refresh_token,
                    token_uri="https://oauth2.googleapis.com/token",
                    client_id=self.secrets.secrets.get("YT_CLIENT_ID_1"),
                    client_secret=self.secrets.secrets.get("YT_CLIENT_SECRET_1")
                )
                
                self.service = build('youtube', 'v3', credentials=credentials)
                return
            
            # استخدام API key مباشرة (صلاحيات محدودة)
            api_key = self.secrets.get_key("youtube", "api")
            if api_key:
                self.service = build('youtube', 'v3', developerKey=api_key)
                
        except Exception as e:
            print(f"❌ خطأ في المصادقة: {e}")
            self.service = None
    
    def upload_video(self, video_path: Path, metadata: Dict, 
                    schedule_time: str, is_compilation: bool = False) -> Optional[str]:
        """رفع فيديو إلى يوتيوب"""
        if not self.service or not video_path.exists():
            return None
        
        try:
            # حساب وقت النشر
            publish_time = self._calculate_publish_time(schedule_time)
            
            # إعداد بيانات الفيديو
            body = {
                'snippet': {
                    'title': metadata['title'],
                    'description': metadata['description'],
                    'tags': metadata['tags'],
                    'categoryId': metadata['category']
                },
                'status': {
                    'privacyStatus': 'private',
                    'publishAt': publish_time.isoformat() + 'Z',
                    'selfDeclaredMadeForKids': False
                }
            }
            
            if is_compilation:
                body['snippet']['title'] = "🔥 " + body['snippet']['title']
            
            # رفع الفيديو
            media = MediaFileUpload(
                str(video_path),
                chunksize=1024*1024,
                resumable=True,
                mimetype='video/mp4'
            )
            
            request = self.service.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = request.execute()
            return response.get('id')
            
        except Exception as e:
            print(f"❌ خطأ في رفع الفيديو: {e}")
            return None
    
    def _calculate_publish_time(self, schedule_time: str) -> datetime:
        """حساب وقت النشر"""
        now = datetime.utcnow()
        
        # تحليل وقت الجدولة
        hour, minute = map(int, schedule_time.split(':'))
        
        # إنشاء تاريخ اليوم مع الوقت المحدد
        publish_date = datetime(now.year, now.month, now.day, hour, minute)
        
        # إذا كان الوقت قد مضى، الجدولة للغد
        if publish_date < now:
            publish_date += timedelta(days=1)
        
        return publish_date
    
    def create_playlist(self, title: str, description: str = "") -> Optional[str]:
        """إنشاء قائمة تشغيل جديدة"""
        if not self.service:
            return None
        
        try:
            body = {
                'snippet': {
                    'title': title,
                    'description': description
                },
                'status': {
                    'privacyStatus': 'public'
                }
            }
            
            request = self.service.playlists().insert(
                part='snippet,status',
                body=body
            )
            
            response = request.execute()
            return response.get('id')
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء قائمة التشغيل: {e}")
            return None
    
    def add_to_playlist(self, playlist_id: str, video_id: str) -> bool:
        """إضافة فيديو إلى قائمة تشغيل"""
        if not self.service:
            return False
        
        try:
            body = {
                'snippet': {
                    'playlistId': playlist_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id
                    }
                }
            }
            
            request = self.service.playlistItems().insert(
                part='snippet',
                body=body
            )
            
            request.execute()
            return True
            
        except Exception as e:
            print(f"⚠️  خطأ في إضافة الفيديو للقائمة: {e}")
            return False
