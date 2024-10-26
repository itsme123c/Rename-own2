from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from bot import start, merge_files

def main() -> None:
  """Starts the bot."""
  application = ApplicationBuilder().token("7825342391:AAFyHNUHeY4fC8jxS8iV_iuM-iDtdlQH_8Q").build()

  # Register handlers
  application.add_handler(CommandHandler("start", start))
  application.add_handler(MessageHandler(filters.Document.ALL, merge_files))

  # Run the bot
  application.run_polling()

if __name__ == "__main__":
  main()
