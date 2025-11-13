import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuración optimizada
BOT_TOKEN = os.environ.get('BOT_TOKEN')
PORT = int(os.environ.get('PORT', 10000))

# Logging optimizado
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando start optimizado"""
    user = update.message.from_user
    await update.message.reply_text(
        f'🤖 **¡Hola {user.first_name}!**\n\n'
        f'✅ **Bot 100% Funcional en Render**\n'
        f'🚀 **Versión:** Ultra Optimizada\n'
        f'💡 **Estado:** Conectado y Activo\n\n'
        f'Escribe cualquier mensaje...'
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo optimizado"""
    user_text = update.message.text
    response = f'📝 **Mensaje recibido:**\n"{user_text}"\n\n✅ **Bot activo y respondiendo**'
    await update.message.reply_text(response)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando status"""
    await update.message.reply_text('🟢 **STATUS:** BOT 100% OPERATIVO\n🔥 Render + Python 3.13\n🚀 Versión Ultra Optimizada')

def main():
    """Función principal optimizada"""
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN no configurado")
        return
    
    try:
        # Crear aplicación con configuración robusta
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Handlers optimizados
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("status", status))
        application.add_handler(CommandHandler("info", status))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        
        logger.info("🚀 BOT INICIANDO - VERSIÓN OPTIMIZADA")
        logger.info(f"🔑 Token: {'✅ CONFIGURADO' if BOT_TOKEN else '❌ FALTANTE'}")
        logger.info(f"🌐 Puerto: {PORT}")
        logger.info(f"📡 Webhook: https://telegram-bot-simple-y7lc.onrender.com/{BOT_TOKEN}")
        
        # Webhook optimizado para Render
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=BOT_TOKEN,
            webhook_url=f"https://telegram-bot-simple-y7lc.onrender.com/{BOT_TOKEN}",
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.error(f"❌ ERROR CRÍTICO: {e}")
        raise

if __name__ == '__main__':
    main()
