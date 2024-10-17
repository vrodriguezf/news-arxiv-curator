import os

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'YOUR_TELEGRAM_BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./newsletter_bot.db')                
WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://yourdomain.com/webhook')
WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', '8443'))