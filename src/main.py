
import logging
import sys

from utils.logger import setup_logging, log_telegram
from config import settings
from content_manager import ContentManager
from script_writer import ScriptWriter
from voice_generator import VoiceGenerator
from visual_generator import VisualGenerator
from video_editor import VideoEditor
from uploader import YouTubeUploader


def main():
    """
    Main orchestration script for The Abyssal Archive bot.
    This function controls the entire workflow from idea to upload.
    """
    setup_logging()
    logging.info(f"--- [{settings.get_current_est_time().strftime('%Y-%m-%d %H:%M:%S')}] The Abyssal Archive Engine: Activated ---")

    try:
        # 1. Content Strategy: Decide what to create today
        content_manager = ContentManager()
        topic_details = content_manager.get_topic_for_today()
        log_telegram(f"✅ Topic selected: {topic_details['title']} | Theme: {topic_details['theme']}")

        # 2. Script Generation (with fail-safes)
        script_writer = ScriptWriter()
        script_data = script_writer.generate_script(topic_details)
        log_telegram(f"✅ Script generated successfully for '{topic_details['title']}'.")

        # 3. Voice Generation (with fail-safes)
        voice_generator = VoiceGenerator()
        audio_path, whispers_paths = voice_generator.generate_all_audio(script_data)
        log_telegram(f"✅ Audio generated and mastered at {audio_path}")

        # 4. Visual Asset Collection (with fail-safes)
        visual_generator = VisualGenerator()
        visual_assets = visual_generator.gather_assets(script_data, topic_details['theme'])
        log_telegram(f"✅ Visual assets gathered: {len(visual_assets['images'])} images, {len(visual_assets['videos'])} videos.")

        # 5. Video Editing & Rendering
        video_editor = VideoEditor(script_data, audio_path, whispers_paths, visual_assets, topic_details['theme'])
        final_video_path = video_editor.create_video()
        log_telegram(f"✅ Video rendered successfully: {final_video_path}")

        # 6. Thumbnail Generation
        thumbnail_path = visual_generator.generate_thumbnail(script_data)
        log_telegram(f"✅ Thumbnail created: {thumbnail_path}")

        # 7. YouTube Upload & SEO
        if settings.FEATURES['upload_to_youtube']:
            uploader = YouTubeUploader(script_data, final_video_path, thumbnail_path, topic_details['theme'])
            video_url = uploader.upload_video()
            log_telegram(f"🚀 Video uploaded successfully! URL: {video_url}")
            
            if settings.FEATURES['post_to_community_tab']:
                uploader.post_to_community_tab(video_url)
                log_telegram(f"✅ Community tab post created.")
        else:
            logging.warning("YouTube upload is disabled in settings.")

        logging.info(f"--- Process completed successfully for '{topic_details['title']}' ---")
        log_telegram(f"🎉 Engine finished successfully. The Abyssal Archive is updated.")

    except Exception as e:
        error_message = f"An error occurred in the main pipeline: {e}"
        logging.error(error_message, exc_info=True)
        log_telegram(f"🔥 FATAL ERROR: {error_message}")
        sys.exit(1) # Exit with error code to fail the GitHub Action

if __name__ == "__main__":
    main()
