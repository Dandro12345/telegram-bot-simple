import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuración básica
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
PORT = int(os.environ.get('PORT', 10000))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 ¡Bot funcionando! Escribe algo...")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📝 Recibí: {update.message.text}")

def main():
    logger.info("🚀 Iniciando bot simple...")
    
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN no configurado")
        return
    
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        
        logger.info("✅ Bot configurado - iniciando webhook...")
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=BOT_TOKEN,
            webhook_url=f"https://telegram-bot-simple-1.onrender.com/{BOT_TOKEN}"
        )
    except Exception as e:
        logger.error(f"💥 Error: {e}")

if __name__ == '__main__':
    main()
