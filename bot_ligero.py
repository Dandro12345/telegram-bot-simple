import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

print("🚀 INICIANDO BOT LIGERO MEJORADO...")

# TOKEN - CAMBIAR POR EL REAL
BOT_TOKEN = "7995699419:AAElCQT_F26CgGJxm8GtwXMxKRJ0gYkuXtMI"

print(f"🔑 Token: {'7995699419:AAElCQT_F26CgGJxm8GtwXMxKRJ0gYkuXtM_'}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await update.message.reply_text(f"🤖 ¡Hola {user.first_name}! Soy tu bot desde Termux + Railway.")

async def chat_inteligente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()
    print(f"📨 Mensaje: {user_message}")
    
    # Respuestas inteligentes básicas
    respuestas = {
        "hola": "¡Hola! ¿Cómo estás? 🌟",
        "como estas": "¡Funcionando perfectamente en Termux! 🚀",
        "que puedes hacer": "Puedo chatear y responder tus mensajes.",
        "gracias": "¡De nada! 🙏",
        "bot": "¡Sí, soy un bot en Python! 💻",
        "termux": "Estoy corriendo en Termux Android 🌍",
        "dandro": "¡Ese es mi creador! Dandro1234 👑",
        "python": "Python es mi lenguaje 🐍",
        "railway": "Conectado a Railway para deployment 🚄"
    }
    
    # Buscar respuesta
    for clave, valor in respuestas.items():
        if clave in user_message:
            await update.message.reply_text(valor)
            return
    
    # Respuesta default
    await update.message.reply_text(f"✅ Recibí: '{update.message.text}'\n💡 Prueba: hola, como estas, python")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info_text = """🤖 INFORMACIÓN DEL BOT

Creado por: Dandro1234
Plataforma: Termux + Railway
Estado: ✅ Funcionando
GitHub: Dandro12345

Comandos:
/start - Iniciar bot
/info - Esta información"""
    await update.message.reply_text(info_text)

def main():
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("info", info))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_inteligente))
        
        print("🤖 Bot INICIADO CORRECTAMENTE")
        print("📡 Esperando mensajes en Telegram...")
        app.run_polling()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("💡 Edita el token en nano: PON_TU_TOKEN_AQUI → token_real")

if __name__ == "__main__":
    main()
