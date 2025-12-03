
# =========================================
# THE MANAGER FILE (settings.py)
# User: You can change any value here safely.
# =========================================
import os
from datetime import datetime
import pytz

# --- Channel & Bot Identity ---
CHANNEL_NAME = "The Abyssal Archive"
CHANNEL_TAGLINE = "Where science meets fear."
GITHUB_REPO_URL = "https://github.com/youssefahap-create/abyssal-archive-engine"
BUSINESS_EMAIL = "youssefehap082@gmail.com"

# --- Affiliate & Monetization Links ---
AFFILIATE_LINKS = {
    "space": "https://amzn.to/49GrAwP",    # Galaxy Projector
    "ocean": "https://amzn.to/4itgqh9",    # Ocean Wave Light
    "horror": "https://amzn.to/3Mr4VuC",   # Horror Books
    "default": "https://amzn.to/48sqNxn", # General/Default
    "audible": "https://amzn.to/48sqNxn"      # Audible Free Trial
}

# --- Content Schedule & Strategy ---
# Defines the theme for each day of the week. 1=Monday, 7=Sunday.
WEEKLY_SCHEDULE = {
    1: "ocean",
    2: "horror", # True Crime is a sub-category of Horror
    3: "space",
    4: "horror", # Psychology is a sub-category of Horror
    5: "horror",
    6: "space",    # Versus can be space vs ocean, handled by script
    7: "ocean"
}

# --- Video & Audio Style ---
STYLE = {
    "font_path": os.path.abspath("assets/fonts/CourierPrime-Bold.ttf"),
    "watermark_path": os.path.abspath("assets/watermarks/logo_transparent.png"),
    "narrator_voice": "en-US-ChristopherNeural",
    "narrator_pitch": "-10%",
    "narrator_rate": "-5%",
    "enable_8d_audio": True,
    "enable_whispers": True,
    "enable_cinematic_black_bars": True,
    "caption_text_color": "white",
    "caption_highlight_color": "red"
}

# --- Feature Flags ---
FEATURES = {
    "upload_to_youtube": True,
    "post_to_community_tab": True,
    "generate_polls": True,
    "use_telegram_notifications": True,
    "use_fail_safe_apis": True,
    "enable_shorts_generation": True,
    "shorts_per_long_video": 2
}

# --- Technical Settings ---
OUTPUT_VIDEO_RESOLUTION = (1080, 1920) # For YouTube Shorts (vertical)
LONG_FORM_RESOLUTION = (1920, 1080) # For standard videos


def get_current_est_time():
    """Returns the current time in US Eastern Time Zone."""
    return datetime.now(pytz.timezone('US/Eastern'))
