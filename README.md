# Telegram Video Merger Bot for Koyeb Free Plan

This repository contains the code for a Telegram bot that can merge videos with audio, videos with other videos, and add subtitles to videos, specifically optimized for Koyeb's free plan.

## Features

- **Video + Audio:** Merge a video with an audio file.
- **Video + Video:** Combine multiple videos into a single video.
- **Video + Subtitles:** Add subtitles to a video.
- **Koyeb Free Plan Compatible:** Lightweight and optimized for Koyeb's free plan resource limitations.

## Installation and Setup

1. **Create a Telegram Bot:**
  - Go to the BotFather on Telegram ([https://t.me/BotFather](https://t.me/BotFather)).
  - Use the `/newbot` command and provide a name and username for your bot.
  - BotFather will give you a unique token for your bot.

2. **Create a Koyeb App:**
  - Sign up for a free Koyeb account ([https://koyeb.com/](https://koyeb.com/)).
  - Create a new app with the following configuration:
    - **Runtime:** Python 3.9
    - **Free Plan:** Choose the free plan.
    - **Port:** 8080 (default)

3. **Set Environment Variables:**
  - Set the `TELEGRAM_BOT_TOKEN` environment variable in your Koyeb app's settings to the token you received from BotFather.

4. **Deploy to Koyeb:**
  - Push your project code to a GitHub repository.
  - Connect your Koyeb app to your GitHub repository.
  - Deploy the app.

5. **Start the Bot:**
  - Send a message to your bot in Telegram.
  - The bot will reply with instructions on how to use its features.

## Usage

- **Start the Bot:** Send `/start` to the bot.
- **Merge Videos with Audio:** Send the video and audio files to the bot in any order.
- **Merge Multiple Videos:** Send the videos one by one to the bot.
- **Add Subtitles to a Video:** Send the video and subtitles file to the bot.

## Koyeb Free Plan Considerations

- **Resource Limitations:** The Koyeb free plan has resource limitations, so the bot's performance may be affected if many users are actively using it.
- **Cold Starts:** If your app hasn't been active for a while, it may take a few seconds to start up, resulting in a delay in responding to Telegram messages.
- **File Size Limits:** The bot can handle video and audio files within the size limits allowed by Telegram.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
