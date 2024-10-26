import logging
import os
import time
from typing import List, Tuple

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Your Telegram bot token
TOKEN = os.environ['TELEGRAM_BOT_TOKEN']

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Constants for file types
VIDEO_TYPES = ['video/mp4', 'video/webm']
AUDIO_TYPES = ['audio/mpeg', 'audio/ogg']
SUBTITLE_TYPES = ['text/plain', 'text/srt']


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Hi! I can help you merge videos.\n\n'
                                  'To merge a video with audio, send me the video and then the audio file.\n'
                                  'To merge multiple videos, send me the videos one by one.\n'
                                  'To add subtitles to a video, send me the video and then the subtitles file.\n'
                                  'Please note that the files should be in the correct format.')

async def merge_files(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the merging of files based on their types."""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    # Get the last two messages sent by the user
    last_messages = await context.bot.get_updates(offset=update.update_id, timeout=10)
    last_messages = last_messages.result
    
    if len(last_messages) < 2:
        await update.message.reply_text('Please send me at least two files.')
        return

    # Get the types of the files
    file_types = [message.document.mime_type for message in last_messages]
    
    # Determine the merging type based on the files
    if all(file_type in VIDEO_TYPES for file_type in file_types):
        await merge_videos(update, context, last_messages)
    elif any(file_type in VIDEO_TYPES for file_type in file_types) and any(file_type in AUDIO_TYPES for file_type in file_types):
        await merge_video_audio(update, context, last_messages)
    elif any(file_type in VIDEO_TYPES for file_type in file_types) and any(file_type in SUBTITLE_TYPES for file_type in file_types):
        await merge_video_subtitle(update, context, last_messages)
    else:
                await update.message.reply_text('Invalid file types. Please send a video and audio or a video and subtitles file.')


async def merge_videos(update: Update, context: ContextTypes.DEFAULT_TYPE, messages: List[Update.Message]) -> None:
    """Merges multiple videos into a single video."""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    # Download the videos
    video_paths = [await download_file(message.document.file_id, chat_id, user_id) for message in messages]
    
    # Merge the videos using ffmpeg
    merged_video_path = f'/tmp/{user_id}_merged_video.mp4'
    merged_video_command = f'ffmpeg -i {video_paths[0]} -i {video_paths[1]} -c copy {merged_video_path}'
    os.system(merged_video_command)
    
    # Send the merged video to the user
    await context.bot.send_video(chat_id=chat_id, video=open(merged_video_path, 'rb'))
    
    # Clean up the downloaded files
    for video_path in video_paths:
        os.remove(video_path)
    os.remove(merged_video_path)
    
    # Send a success message
    await update.message.reply_text('Videos merged successfully!')

async def merge_video_audio(update: Update, context: ContextTypes.DEFAULT_TYPE, messages: List[Update.Message]) -> None:
    """Merges a video with an audio file."""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    # Determine the video and audio files
    video_message = next((message for message in messages if message.document.mime_type in VIDEO_TYPES), None)
    audio_message = next((message for message in messages if message.document.mime_type in AUDIO_TYPES), None)
    
    if not video_message or not audio_message:
        await update.message.reply_text('Please send a video and an audio file.')
        return
    
    # Download the files
    video_path = await download_file(video_message.document.file_id, chat_id, user_id)
    audio_path = await download_file(audio_message.document.file_id, chat_id, user_id)
    
    # Merge the video and audio using ffmpeg
    merged_video_path = f'/tmp/{user_id}_merged_video.mp4'
    merged_video_command = f'ffmpeg -i {video_path} -i {audio_path} -c copy {merged_video_path}'
    os.system(merged_video_command)
    
    # Send the merged video to the user
    await context.bot.send_video(chat_id=chat_id, video=open(merged_video_path, 'rb'))
    
    # Clean up the downloaded files
    os.remove(video_path)
    os.remove(audio_path)
    os.remove(merged_video_path)
    
    # Send a success message
    await update.message.reply_text('Video and audio merged successfully!')


async def merge_video_subtitle(update: Update, context: ContextTypes.DEFAULT_TYPE, messages: List[Update.Message]) -> None:
    """Adds subtitles to a video."""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    # Determine the video and subtitle files
    video_message = next((message for message in messages if message.document.mime_type in VIDEO_TYPES), None)
    subtitle_message = next((message for message in messages if message.document.mime_type in SUBTITLE_TYPES), None)
    
    if not video_message or not subtitle_message:
        await update.message.reply_text('Please send a video and a subtitles file.')
        return
    
    # Download the files
    video_path = await download_file(video_message.document.file_id, chat_id, user_id)
    subtitle_path = await download_file(subtitle_message.document.file_id, chat_id, user_id)
    
    # Add subtitles to the video using ffmpeg
    merged_video_path = f'/tmp/{user_id}_merged_video.mp4'
    merged_video_command = f'ffmpeg -i {video_path} -i {subtitle_path} -map 0:v -map 1:s -c:v copy -c:a copy -c:s mov_text {merged_video_path}'
    os.system(merged_video_command)
    
    # Send the merged video to the user
    await context.bot.send_video(chat_id=chat_id, video=open(merged_video_path, 'rb'))
    
    # Clean up the downloaded files
    os.remove(video_path)
    os.remove(subtitle_path)
    os.remove(merged_video_path)
    
    # Send a success message
    await update.message.reply_text('Subtitles added to video successfully!')

async def download_file(file_id: str, chat_id: int, user_id: int) -> str:
    """Downloads a file from Telegram and returns its path."""
    file = await context.bot.get_file(file_id)
    file_path = f'/tmp/{user_id}_{file.file_name}'
    await file.download(file_path)
    return file_path

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL, merge_files))

    # Start the bot
    application.run_polling()
