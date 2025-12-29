import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

from utils.logger import logger


class DatabaseManager:
    """مدير قاعدة البيانات المركزية"""
    
    def __init__(self, db_path: str = "database/youtube_auto.db"):
        """تهيئة مدير قاعدة البيانات"""
        
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """تهيئة قاعدة البيانات وإنشاء الجداول"""
        
        # إنشاء مجلد قاعدة البيانات إذا لم يكن موجوداً
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # جدول الأسئلة
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            category TEXT NOT NULL,
            difficulty TEXT DEFAULT 'medium',
            image_prompt TEXT,
            used BOOLEAN DEFAULT 0,
            used_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source TEXT DEFAULT 'local'
        )
        ''')
        
        # جدول الفيديوهات
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT UNIQUE,
            question_id INTEGER,
            video_path TEXT NOT NULL,
            video_type TEXT CHECK(video_type IN ('short', 'compilation')),
            title TEXT,
            description TEXT,
            tags TEXT,
            upload_status TEXT DEFAULT 'pending',
            upload_time TEXT,
            youtube_url TEXT,
            scheduled_time TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (question_id) REFERENCES questions(id)
        )
        ''')
        
        # جدول الإحصائيات
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id INTEGER,
            views INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0,
            engagement_rate REAL DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (video_id) REFERENCES videos(id)
        )
        ''')
        
        # جدول استخدام API
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS api_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_name TEXT NOT NULL,
            request_count INTEGER DEFAULT 0,
            success_count INTEGER DEFAULT 0,
            last_used TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # جدول المهام المجدولة
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS scheduled_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            task_type TEXT NOT NULL,
            scheduled_time TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            last_run TEXT,
            next_run TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # جدول الأخطاء
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS errors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            error_type TEXT NOT NULL,
            error_message TEXT NOT NULL,
            module TEXT,
            function TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
        
        logger.info("Database initialized successfully")
    
    def _get_connection(self):
        """الحصول على اتصال قاعدة البيانات"""
        
        return sqlite3.connect(self.db_path)
    
    # === عمليات الأسئلة ===
    
    def save_question(self, question_data: Dict[str, Any]) -> int:
        """حفظ سؤال في قاعدة البيانات"""
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            INSERT INTO questions (question, answer, category, difficulty, image_prompt, source)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                question_data['question'],
                question_data['answer'],
                question_data.get('category', 'general'),
                question_data.get('difficulty', 'medium'),
                question_data.get('image_prompt', ''),
                question_data.get('source', 'local')
            ))
            
            question_id = cursor.lastrowid
            conn.commit()
            
            logger.info(f"Question saved with ID: {question_id}")
            return question_id
            
        except Exception as e:
            logger.error(f"Error saving question: {e}")
            conn.rollback()
            return -1
        finally:
            conn.close()
    
    def get_unused_questions(self, category: str = None, limit: int = 10) -> List[Dict]:
        """الحصول على أسئلة غير مستخدمة"""
        
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            if category:
                cursor.execute('''
                SELECT * FROM questions 
                WHERE used = 0 AND category = ?
                ORDER BY RANDOM()
                LIMIT ?
                ''', (category, limit))
            else:
                cursor.execute('''
                SELECT * FROM questions 
                WHERE used = 0
                ORDER BY RANDOM()
                LIMIT ?
                ''', (limit,))
            
            results = cursor.fetchall()
            return [dict(row) for row in results]
            
        except Exception as e:
            logger.error(f"Error getting unused questions: {e}")
            return []
        finally:
            conn.close()
    
    def mark_question_used(self, question_id: int):
        """تحديد السؤال كمستخدم"""
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            UPDATE questions 
            SET used = 1, used_date = ?
            WHERE id = ?
            ''', (datetime.now().isoformat(), question_id))
            
            conn.commit()
            logger.info(f"Question {question_id} marked as used")
            
        except Exception as e:
            logger.error(f"Error marking question as used: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    # === عمليات الفيديوهات ===
    
    def save_video(self, video_data: Dict[str, Any]) -> int:
        """حفظ معلومات الفيديو"""
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # تحويل القوائم إلى JSON
            tags_json = json.dumps(video_data.get('tags', [])) if video_data.get('tags') else None
            
            cursor.execute('''
            INSERT INTO videos (
                video_id, question_id, video_path, video_type, 
                title, description, tags, upload_status, scheduled_time
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                video_data.get('video_id'),
                video_data.get('question_id'),
                video_data['video_path'],
                video_data.get('video_type', 'short'),
                video_data.get('title'),
                video_data.get('description'),
                tags_json,
                video_data.get('upload_status', 'pending'),
                video_data.get('scheduled_time')
            ))
            
            video_id = cursor.lastrowid
            conn.commit()
            
            logger.info(f"Video saved with ID: {video_id}")
            return video_id
            
        except Exception as e:
            logger.error(f"Error saving video: {e}")
            conn.rollback()
            return -1
        finally:
            conn.close()
    
    def update_video_status(self, video_id: int, status: str, youtube_url: str = None):
        """تحديث حالة الفيديو"""
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            if youtube_url:
                cursor.execute('''
                UPDATE videos 
                SET upload_status = ?, youtube_url = ?, upload_time = ?
                WHERE id = ?
                ''', (status, youtube_url, datetime.now().isoformat(), video_id))
            else:
                cursor.execute('''
                UPDATE videos 
                SET upload_status = ?, upload_time = ?
                WHERE id = ?
                ''', (status, datetime.now().isoformat(), video_id))
            
            conn.commit()
            logger.info(f"Video {video_id} status updated to: {status}")
            
        except Exception as e:
            logger.error(f"Error updating video status: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def get_pending_videos(self) -> List[Dict]:
        """الحصول على الفيديوهات المنتظرة"""
        
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            SELECT * FROM videos 
            WHERE upload_status = 'pending'
            ORDER BY created_at ASC
            ''')
            
            results = cursor.fetchall()
            return [dict(row) for row in results]
            
        except Exception as e:
            logger.error(f"Error getting pending videos: {e}")
            return []
        finally:
            conn.close()
    
    # === عمليات الإحصائيات ===
    
    def update_video_stats(self, youtube_video_id: str, stats: Dict[str, int]):
        """تحديث إحصائيات الفيديو"""
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # البحث عن video_id باستخدام youtube_video_id
            cursor.execute('SELECT id FROM videos WHERE video_id = ?', (youtube_video_id,))
            result = cursor.fetchone()
            
            if result:
                video_db_id = result[0]
                
                # حساب معدل التفاعل
                views = stats.get('views', 0)
                likes = stats.get('likes', 0)
                comments = stats.get('comments', 0)
                
                engagement_rate = 0
                if views > 0:
                    engagement_rate = ((likes + comments) / views) * 100
                
                cursor.execute('''
                INSERT OR REPLACE INTO statistics (video_id, views, likes, comments, engagement_rate)
                VALUES (?, ?, ?, ?, ?)
                ''', (video_db_id, views, likes, comments, engagement_rate))
                
                conn.commit()
                logger.info(f"Updated stats for YouTube video: {youtube_video_id}")
            
        except Exception as e:
            logger.error(f"Error updating video stats: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def get_performance_report(self, days: int = 7) -> Dict[str, Any]:
        """الحصول على تقرير أداء"""
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # حساب تاريخ البدء
            from datetime import datetime, timedelta
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            
            # إحصائيات عامة
            cursor.execute('''
            SELECT 
                COUNT(*) as total_videos,
                SUM(CASE WHEN upload_status = 'uploaded' THEN 1 ELSE 0 END) as uploaded_videos,
                AVG(engagement_rate) as avg_engagement
            FROM videos v
            LEFT JOIN statistics s ON v.id = s.video_id
            WHERE v.created_at >= ?
            ''', (start_date,))
            
            stats = cursor.fetchone()
            
            # أفضل الفيديوهات أداءً
            cursor.execute('''
            SELECT v.title, s.views, s.likes, s.engagement_rate
            FROM videos v
            JOIN statistics s ON v.id = s.video_id
            WHERE v.created_at >= ?
            ORDER BY s.engagement_rate DESC
            LIMIT 5
            ''', (start_date,))
            
            top_performers = cursor.fetchall()
            
            # تحليل الفئات
            cursor.execute('''
            SELECT q.category, COUNT(*) as count, AVG(s.engagement_rate) as avg_engagement
            FROM questions q
            JOIN videos v ON q.id = v.question_id
            LEFT JOIN statistics s ON v.id = s.video_id
            WHERE v.created_at >= ?
            GROUP BY q.category
            ORDER BY avg_engagement DESC
            ''', (start_date,))
            
            category_analysis = cursor.fetchall()
            
            report = {
                "period": f"Last {days} days",
                "total_videos": stats[0],
                "uploaded_videos": stats[1],
                "average_engagement": round(stats[2] or 0, 2),
                "top_performers": [
                    {"title": row[0], "views": row[1], "likes": row[2], "engagement": round(row[3] or 0, 2)}
                    for row in top_performers
                ],
                "category_analysis": [
                    {"category": row[0], "count": row[1], "engagement": round(row[2] or 0, 2)}
                    for row in category_analysis
                ]
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating performance report: {e}")
            return {}
        finally:
            conn.close()
    
    # === عمليات API ===
    
    def log_api_usage(self, api_name: str, success: bool):
        """تسجيل استخدام API"""
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            # التحقق من وجود السجل
            cursor.execute('''
            SELECT id, request_count, success_count 
            FROM api_usage 
            WHERE api_name = ?
            ''', (api_name,))
            
            result = cursor.fetchone()
            
            if result:
                # تحديث السجل الموجود
                api_id, request_count, success_count = result
                new_request_count = request_count + 1
                new_success_count = success_count + (1 if success else 0)
                
                cursor.execute('''
                UPDATE api_usage 
                SET request_count = ?, success_count = ?, last_used = ?
                WHERE id = ?
                ''', (new_request_count, new_success_count, datetime.now().isoformat(), api_id))
            else:
                # إنشاء سجل جديد
                cursor.execute('''
                INSERT INTO api_usage (api_name, request_count, success_count, last_used)
                VALUES (?, 1, ?, ?)
                ''', (api_name, 1 if success else 0, datetime.now().isoformat()))
            
            conn.commit()
            
        except Exception as e:
            logger.error(f"Error logging API usage: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def get_api_usage_stats(self) -> Dict[str, Dict]:
        """الحصول على إحصائيات استخدام API"""
        
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM api_usage')
            results = cursor.fetchall()
            
            stats = {}
            for row in results:
                row_dict = dict(row)
                api_name = row_dict['api_name']
                
                # حساب نسبة النجاح
                request_count = row_dict['request_count']
                success_count = row_dict['success_count']
                success_rate = (success_count / request_count * 100) if request_count > 0 else 0
                
                stats[api_name] = {
                    "requests": request_count,
                    "successes": success_count,
                    "success_rate": round(success_rate, 2),
                    "last_used": row_dict['last_used']
                }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting API usage stats: {e}")
            return {}
        finally:
            conn.close()
    
    # === عمليات الأخطاء ===
    
    def log_error(self, error_type: str, error_message: str, module: str = None, function: str = None):
        """تسجيل خطأ في قاعدة البيانات"""
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            INSERT INTO errors (error_type, error_message, module, function)
            VALUES (?, ?, ?, ?)
            ''', (error_type, error_message, module, function))
            
            conn.commit()
            logger.debug(f"Error logged in database: {error_type}")
            
        except Exception as e:
            logger.error(f"Error logging error to database: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def get_recent_errors(self, limit: int = 20) -> List[Dict]:
        """الحصول على الأخطاء الأخيرة"""
        
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            SELECT * FROM errors 
            ORDER BY timestamp DESC 
            LIMIT ?
            ''', (limit,))
            
            results = cursor.fetchall()
            return [dict(row) for row in results]
            
        except Exception as e:
            logger.error(f"Error getting recent errors: {e}")
            return []
        finally:
            conn.close()
    
    # === عمليات المهام المجدولة ===
    
    def save_scheduled_task(self, task_name: str, task_type: str, scheduled_time: str):
        """حفظ مهمة مجدولة"""
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
            INSERT OR REPLACE INTO scheduled_tasks (task_name, task_type, scheduled_time, status)
            VALUES (?, ?, ?, 'pending')
            ''', (task_name, task_type, scheduled_time))
            
            conn.commit()
            logger.info(f"Scheduled task saved: {task_name}")
            
        except Exception as e:
            logger.error(f"Error saving scheduled task: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def update_task_status(self, task_name: str, status: str, next_run: str = None):
        """تحديث حالة المهمة"""
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            if next_run:
                cursor.execute('''
                UPDATE scheduled_tasks 
                SET status = ?, last_run = ?, next_run = ?
                WHERE task_name = ?
                ''', (status, datetime.now().isoformat(), next_run, task_name))
            else:
                cursor.execute('''
                UPDATE scheduled_tasks 
                SET status = ?, last_run = ?
                WHERE task_name = ?
                ''', (status, datetime.now().isoformat(), task_name))
            
            conn.commit()
            logger.debug(f"Task {task_name} status updated to: {status}")
            
        except Exception as e:
            logger.error(f"Error updating task status: {e}")
            conn.rollback()
        finally:
            conn.close()


# إنشاء نسخة عامة
db_manager = DatabaseManager()
