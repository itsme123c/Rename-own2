import os
import moviepy.editor as mp
from telegram import Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from .env import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Store videos temporarily
VIDEOS = []

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hi! Send me videos to merge. Type /done when you are finished.")

def handle_video(update: Update, context: CallbackContext):
    # Download and save the video
    video = update.message.video or update.message.document
    file_id = video.file_id
    file_obj = context.bot.get_file(file_id)
    
    # Ensure the downloads directory exists
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    
    # Save the video with its original filename
    video_path = f"downloads/{file_id}.mp4"
    file_obj.download(video_path)

    VIDEOS.append(video_path)
    update.message.reply_text(f"Video received! Total videos: {len(VIDEOS)}")

def merge_videos(update: Update, context: CallbackContext):
    if len(VIDEOS) < 2:
        update.message.reply_text("Please upload at least 2 videos to merge.")
        return
    
    # Merge videos using moviepy
    clips = [mp.VideoFileClip(video) for video in VIDEOS]
    final_clip = mp.concatenate_videoclips(clips, method="compose")
    
    output_path = "downloads/merged_video.mp4"
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # Send the merged video back to the user
    with open(output_path, "rb") as f:
        update.message.reply_video(InputFile(f, filename="merged_video.mp4"))

    # Clean up: remove all downloaded files
    for video in VIDEOS:
        os.remove(video)
    VIDEOS.clear()
    os.remove(output_path)

    update.message.reply_text("Merging complete! Here is your video.")

def error_handler(update: Update, context: CallbackContext):
    update.message.reply_text("An error occurred. Please try again.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.video | Filters.document, handle_video))
    dp.add_handler(CommandHandler("done", merge_videos))
    dp.add_error_handler(error_handler)

    updater.start_polling()
    print("Bot is running...")
    updater.idle()

if __name__ == "__main__":
    main()
