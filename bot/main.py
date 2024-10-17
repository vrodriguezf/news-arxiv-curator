import logging
from telegram import __version__ as TG_VER
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot.handlers import setup_handlers
from database.db import init_db
from config.config import TELEGRAM_TOKEN, WEBHOOK_URL, WEBHOOK_PORT

async def main():
    # Initialize the database
    init_db()
    
    # Set up the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Set up handlers
    setup_handlers(application)
    
    # Set up the webhook
    await application.start()
    await application.update_set_webhook(url=WEBHOOK_URL)
    
    # Run the bot until manually stopped
    await application.run_polling()

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    import asyncio
    asyncio.run(main())