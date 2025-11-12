import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

print("🚀 BOT EJECUTÁNDOSE EN RAILWAY - 24/7 ACTIVO")

# Token de Telegram
BOT_TOKEN = "7995699419:AAElCQT_F26CgGJxm8GtwXMxKRJ0gYkuXtM"

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(
        f"🤖 ¡Hola {user.first_name}!\n\n"
        "✅ *Bot ejecutándose en Railway Cloud*\n"
        "📍 *Plataforma:* Nube (Railway) 24/7\n"  
        "🔧 *Estado:* Siempre activo\n"
        "👨‍💻 *Creador:* Dandro1234\n"
        "📅 *Desplegado:* Noviembre 2025\n\n"
        "¡No estoy en tu teléfono, estoy en la nube! ☁️",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = (
        f"✅ Mensaje recibido en Railway: '{user_message}'\n\n"
        "🌐 *Ejecutándose en la nube*\n"
        "💾 *Memoria:* Persistente\n"
        "⚡ *Rendimiento:* Máximo\n"
        "🕒 *Disponibilidad:* 24/7"
    )
    await update.message.reply_text(response, parse_mode="Markdown")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info_text = """
📋 *INFORMACIÓN TÉCNICA RAILWAY*

*Plataforma:* Railway Cloud
*Estado:* ✅ Producción
*Bot:* @ayudante_ia_bot
*GitHub:* Dandro12345/telegram-bot-simple
*Creador:* Dandro1234

*Tecnologías:*
🐍 Python 3.12
🤖 python-telegram-bot
☁️ Railway
📱 Telegram API

*Comandos:*
/start - Iniciar bot
/info - Esta información
    """
    await update.message.reply_text(info_text, parse_mode="Markdown")

def main():
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("info", info))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("✅ BOT INICIADO EN RAILWAY")
        print("🌐 Ejecutándose en la nube...")
        print("📡 Escuchando mensajes...")
        
        app.run_polling()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
