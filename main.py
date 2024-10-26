from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from bot.py import start, merge_files

def main() -> None:
  """Starts the bot."""
  application = ApplicationBuilder().token("TELEGRAM_BOT_TOKEN").build()

  # Register handlers
  application.add_handler(CommandHandler("start", start))
  application.add_handler(MessageHandler(filters.Document.ALL, merge_files))

  # Run the bot
  application.run_polling()

if __name__ == "__main__":
  main()
