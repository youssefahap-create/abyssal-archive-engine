# The Abyssal Archive - YouTube Automation Project

## Overview
The Abyssal Archive is an automated YouTube channel that produces mystery and scary facts content targeting international audiences for monetization.
The system runs on GitHub Actions, creating 2 long-form videos and 4 shorts daily using AI-generated content, images, and audio.

## Features
- **Daily Production**: Creates 6 videos per day (2 long, 4 shorts)
- **Multi-Source Content**: Pulls from Wikipedia, Google Trends, Reddit RSS, NASA, NOAA
- **AI-Powered**: Generates scripts, images, and audio automatically
- **Ad-Safe Content**: Filters content to maintain monetization eligibility
- **Multi-API Support**: Uses multiple API keys to avoid quotas
- **Smart Scheduling**: Publishes at optimal times for US/UK audience
- **Telegram Notifications**: Real-time monitoring and alerts

## Architecture
- **Content Sourcing**: Wikipedia, Google Trends, Reddit, NASA/NOAA APIs
- **AI Processing**: Gemini for script generation, multiple image APIs
- **Media Creation**: Edge-TTS for narration, MoviePy for video assembly
- **Publishing**: YouTube API with multi-account quota management
- **Monitoring**: Telegram bots and logging systems

## Environment Variables Required
All sensitive data is managed through GitHub Secrets:

### Content APIs
- `GEMINI_API_KEY_1`, `GEMINI_API_KEY_2`
- `OPENAI_API_KEY_1`, `OPENAI_API_KEY_2`
- `GROQ_API_KEY`
- `HF_API_TOKEN_1`
- `TAVILY_API_KEY`
- `NEWS_API`

### Image Generation
- `GETIMG_API_KEY_1`, `GETIMG_API_KEY_2`
- `REPLICATE_API_TOKEN_1`, `REPLICATE_API_TOKEN_2`
- `PEXELS_API_KEY`
- `PIXABAY_API_KEY`
- `UNSPLASH_ACCESS_KEY`, `UNSPLASH_SECRET_KEY`
- `FREEPIK_API_KEY`
- `VECTEEZY_API_KEY`, `VECTEEZEY_ID_KEY`
- `COVERR_API_ID`, `COVERR_API_KEY`

### Audio/Sound
- `ELEVEN_API_KEY_1`, `ELEVEN_API_KEY_2`, `ELEVEN_API_KEY_3`
- `FREESOUND_API`, `FREESOUND_ID`

### Data Sources
- `NASA_API_KEY`
- `NOAA_API_KEY`
- `INTERNET_ARCHIVE_ACCESS_KEY`, `INTERNET_ARCHIVE_SECRET_KEY`

### YouTube Integration
- `YOUTUBE_API_KEY`
- `YT_CHANNEL_ID`
- `YT_CLIENT_ID_1`, `YT_CLIENT_ID_2`
- `YT_CLIENT_SECRET_1`, `YT_CLIENT_SECRET_2`
- `YT_REFRESH_TOKEN_1`, `YT_REFRESH_TOKEN_2`

### Communication
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

### Other Services
- `CAMB_AI_KEY_1`
- `CLOUDINARY_API_KEY`
- `REMOVE_BG_API`
- `OPENROUTER_KEY`

## Installation
1. Clone the repository
2. Set up all required environment variables in GitHub Secrets
3. Configure YouTube API access with proper OAuth credentials
4. Review and approve the content policies for your channel

## Usage
The system runs automatically via GitHub Actions on a scheduled basis:
- Daily production: Twice per day at 6 AM and 1 PM EST
- Health checks: Every 6 hours

Manual triggers are also available through the GitHub Actions interface.

## Content Strategy
- **Long Videos**: 3-6 minutes, deep mystery explorations
- **Shorts**: 1-minute highlights and teasers
- **Categories**: Space mysteries, Ocean anomalies, Historical enigmas, True crime, Paranormal phenomena
- **Themes**: Focus on liminal spaces, nightmare facts, and unsolved mysteries

## Safety & Compliance
- Ad-safe content filtering
- Multiple API key rotation to prevent quota issues
- Content moderation for international audiences
- Proper licensing and attribution practices

## Monitoring
- Comprehensive logging system
- Telegram notifications for errors and status updates
- Performance tracking and optimization

## Legal Notice
This project is designed for educational and entertainment purposes.
Content creators are responsible for ensuring compliance with YouTube's terms of service, advertising policies, and local regulations.
The system is designed to produce ad-safe content but creators should monitor their channels regularly.
The owner assumes full responsibility for the content produced by this system.
