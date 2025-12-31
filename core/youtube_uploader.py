import os
import time
from pathlib import Path
from typing import Optional, Dict, List
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from config import config
from core.logger import logger

class YouTubeUploader:
    def __init__(self):
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with YouTube API"""
        try:
            # Try first set of credentials
            credentials = Credentials(
                token=None,
                refresh_token=os.getenv("YT_REFRESH_TOKEN_1"),
                token_uri="https://oauth2.googleapis.com/token",
                client_id=os.getenv("YT_CLIENT_ID_1"),
                client_secret=os.getenv("YT_CLIENT_SECRET_1")
            )
            
            if credentials.expired:
                credentials.refresh(Request())
            
            self.service = build('youtube', 'v3', credentials=credentials)
            logger.info("YouTube authentication successful with first token")
            
        except Exception as e:
            logger.warning(f"First YouTube token failed: {str(e)}")
            
            # Try second set of credentials
            try:
                credentials = Credentials(
                    token=None,
                    refresh_token=os.getenv("YT_REFRESH_TOKEN_2"),
                    token_uri="https://oauth2.googleapis.com/token",
                    client_id=os.getenv("YT_CLIENT_ID_2"),
                    client_secret=os.getenv("YT_CLIENT_SECRET_2")
                )
                
                if credentials.expired:
                    credentials.refresh(Request())
                
                self.service = build('youtube', 'v3', credentials=credentials)
                logger.info("YouTube authentication successful with second token")
                
            except Exception as e2:
                logger.error(f"All YouTube authentication failed: {str(e2)}")
                self.service = None
    
    def upload_short(self, video_path: Path, metadata: Dict) -> Optional[str]:
        """Upload a Short video to YouTube"""
        
        if not self.service:
            logger.error("YouTube service not authenticated")
            return None
        
        try:
            # Prepare metadata
            title = metadata.get("title", "Daily Quiz Challenge")
            description = metadata.get("description", "Test your knowledge! Write your answer in the comments below.")
            tags = metadata.get("tags", ["quiz", "challenge", "trivia", "test", "knowledge"])
            
            # YouTube Shorts requirements
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags,
                    'categoryId': config.YOUTUBE_CATEGORY_ID
                },
                'status': {
                    'privacyStatus': config.YOUTUBE_PRIVACY_STATUS,
                    'selfDeclaredMadeForKids': False
                }
            }
            
            # Upload video
            media = MediaFileUpload(
                str(video_path),
                chunksize=1024*1024,
                resumable=True,
                mimetype='video/mp4'
            )
            
            request = self.service.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )
            
            # Execute upload
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    logger.info(f"Upload progress: {int(status.progress() * 100)}%")
            
            video_id = response['id']
            logger.info(f"Successfully uploaded Short: {video_id}")
            
            # Add to playlist if exists
            self._add_to_playlist(video_id)
            
            return video_id
            
        except Exception as e:
            logger.error(f"Failed to upload Short: {str(e)}")
            return None
    
    def upload_compilation(self, video_path: Path, metadata: Dict) -> Optional[str]:
        """Upload a compilation video to YouTube"""
        
        if not self.service:
            logger.error("YouTube service not authenticated")
            return None
        
        try:
            # Prepare metadata for compilation
            title = metadata.get("title", "Daily Quiz Compilation")
            description = metadata.get("description", "Today's quiz challenges compilation. Watch all shorts in one video!")
            tags = metadata.get("tags", ["compilation", "quiz", "challenge", "daily", "shorts"])
            
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags,
                    'categoryId': config.YOUTUBE_CATEGORY_ID
                },
                'status': {
                    'privacyStatus': config.YOUTUBE_PRIVACY_STATUS,
                    'selfDeclaredMadeForKids': False
                }
            }
            
            # Upload video
            media = MediaFileUpload(
                str(video_path),
                chunksize=1024*1024,
                resumable=True,
                mimetype='video/mp4'
            )
            
            request = self.service.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )
            
            # Execute upload
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    logger.info(f"Upload progress: {int(status.progress() * 100)}%")
            
            video_id = response['id']
            logger.info(f"Successfully uploaded compilation: {video_id}")
            
            return video_id
            
        except Exception as e:
            logger.error(f"Failed to upload compilation: {str(e)}")
            return None
    
    def _add_to_playlist(self, video_id: str):
        """Add video to playlist"""
        try:
            playlist_id = self._get_or_create_playlist("Daily Quiz Shorts")
            
            if playlist_id:
                self.service.playlistItems().insert(
                    part="snippet",
                    body={
                        "snippet": {
                            "playlistId": playlist_id,
                            "resourceId": {
                                "kind": "youtube#video",
                                "videoId": video_id
                            }
                        }
                    }
                ).execute()
                
                logger.info(f"Added video {video_id} to playlist")
        
        except Exception as e:
            logger.warning(f"Failed to add to playlist: {str(e)}")
    
    def _get_or_create_playlist(self, title: str) -> Optional[str]:
        """Get or create a playlist"""
        try:
            # Search for existing playlist
            response = self.service.playlists().list(
                part="snippet",
                mine=True,
                maxResults=50
            ).execute()
            
            for playlist in response.get('items', []):
                if playlist['snippet']['title'] == title:
                    return playlist['id']
            
            # Create new playlist
            response = self.service.playlists().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": title,
                        "description": "Daily quiz shorts compilation"
                    },
                    "status": {
                        "privacyStatus": "public"
                    }
                }
            ).execute()
            
            return response['id']
        
        except Exception as e:
            logger.error(f"Failed to create playlist: {str(e)}")
            return None
    
    def update_daily(self, shorts_metadata: List[Dict], compilation_metadata: Dict):
        """Upload all daily content"""
        
        if not self.service:
            logger.error("Cannot upload - not authenticated")
            return
        
        # Upload shorts
        short_ids = []
        for i, metadata in enumerate(shorts_metadata):
            video_path = metadata.get("video_path")
            if video_path and video_path.exists():
                video_id = self.upload_short(video_path, metadata)
                if video_id:
                    short_ids.append(video_id)
                    # Add delay between uploads
                    if i < len(shorts_metadata) - 1:
                        time.sleep(30)  # 30-second delay
        
        # Upload compilation
        compilation_path = compilation_metadata.get("video_path")
        if compilation_path and compilation_path.exists():
            self.upload_compilation(compilation_path, compilation_metadata)
