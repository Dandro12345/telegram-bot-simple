import os
import logging
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuración para Render
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Obtener token de variable de entorno o usar el directo
BOT_TOKEN = os.environ.get('BOT_TOKEN', '7995699419:AAElCQT_F26CgGJxm8GtwXMxKRJ0gYkuXtM')

print("🚀 BOT INICIANDO EN RENDER...")
print(f"🔑 Token: {'✅ Configurado' if BOT_TOKEN else '❌ Faltante'}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(
        f"🤖 ¡Hola {user.first_name}!\n\n"
        "✅ *Bot ejecutándose en Render 24/7*\n"
        "📍 *Plataforma:* Render Cloud\n"
        "🔧 *Estado:* Siempre activo\n"
        "👨‍💻 *Creador:* Dandro1234\n\n"
        "¡Estoy en la nube, no en tu teléfono! ☁️",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = (
        f"✅ Mensaje recibido en Render: '{user_message}'\n\n"
        "🌐 *Ejecutándose en la nube*\n"
        "⚡ *Rendimiento máximo*\n"
        "🕒 *Disponibilidad:* 24/7\n"
        "📱 *Sin depender de tu teléfono*"
    )
    await update.message.reply_text(response, parse_mode="Markdown")

def main():
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("✅ BOT INICIADO CORRECTAMENTE EN RENDER")
        print("🌐 Ejecutándose en la nube...")
        print("📡 Escuchando mensajes...")
        
        app.run_polling()
        
    except Exception as e:
        print(f"❌ Error al iniciar bot: {e}")
        print("💡 Verifica el BOT_TOKEN y la conexión")

if __name__ == "__main__":
    main()
