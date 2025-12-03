
# The Abyssal Archive - Automated YouTube Content Engine

This repository contains the source code for a fully automated YouTube channel, "The Abyssal Archive," which generates high-quality, cinematic videos about mysteries, horror, and science.

## Features

* **Fully Automated**: From idea generation to upload, the entire process is handled by the bot.
* **Cinematic Quality**: Implements a multi-layer VFX stack including 4K grain, fog, scanlines, and cinematic color grading.
* **Advanced Audio Engineering**: Features 8D audio panning, background whispers, and dynamic sound effects for an immersive experience.
* **AI-Powered**: Utilizes multiple LLMs (Gemini, Groq) and Image/Video generation APIs (GetImg, Pexels) for content creation.
* **Fail-Safe Architecture**: Intelligently rotates between multiple API keys to handle failures and quota limits.
* **SEO & Growth Optimized**: Automatically generates localized titles/descriptions for 10+ languages, posts to the community tab, and creates optimized thumbnails.
* **User-Friendly Control**: All major settings can be controlled via a simple `config/settings.py` file.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/youssefahap-create/abyssal-archive-engine.git](https://github.com/youssefahap-create/abyssal-archive-engine.git)
    cd abyssal-archive-engine
    ```
2.  **Create a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    # You may need to install FFmpeg and ImageMagick on your system
    # On Debian/Ubuntu: sudo apt-get update && sudo apt-get install ffmpeg imagemagick
    ```
4.  **Configure Secrets:** This project is designed to run in GitHub Actions. Add all your API keys to your repository's secrets (`Settings -> Secrets and variables -> Actions`).

## Running the Bot

The bot is designed to be run via the GitHub Actions workflow defined in `.github/workflows/main.yml`. It runs on a schedule and can also be triggered manually from the Actions tab.
