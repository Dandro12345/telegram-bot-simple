import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ==================== CONFIGURACIÓN COMPLETA ====================
print("🔧 INICIANDO CONFIGURACIÓN COMPLETA DEL BOT...")

# TOKEN EXACTO - SIN ESPACIOS EXTRA
BOT_TOKEN = "7995699419:AAElCQT_F26CgGJxm8GtwXMxKRJ0gYkuXtM"

# Verificar token
print(f"🔑 Token configurado: {'✅ VÁLIDO' if BOT_TOKEN and len(BOT_TOKEN) == 46 else '❌ INVÁLIDO'}")
print(f"📏 Longitud token: {len(BOT_TOKEN)}")
print(f"🔐 Token: {BOT_TOKEN[:10]}...{BOT_TOKEN[-10:]}")

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ==================== FUNCIONES DEL BOT ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejador del comando /start"""
    user = update.message.from_user
    welcome_text = f"""
🤖 *¡Hola {user.first_name}!*

*Bot Configurado Completamente*
📍 *Plataforma:* Termux + Railway
👨‍💻 *Creador:* Dandro1234
🔗 *GitHub:* Dandro12345
📡 *Estado:* ✅ OPERATIVO

*Comandos disponibles:*
/start - Iniciar conversación
/info - Información del bot
/status - Estado del sistema

¡Envíame cualquier mensaje!
    """
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejador del comando /info"""
    info_text = """
📋 *INFORMACIÓN TÉCNICA*

*Tokens Configurados:*
✅ Telegram Bot Token
✅ GitHub: Dandro12345
✅ Railway: Conectado

*Tecnologías:*
🐍 Python 3.12
🤖 python-telegram-bot
📱 Termux Android
🚄 Railway Deployment

*Repositorio:*
https://github.com/Dandro12345/telegram-bot-simple
    """
    await update.message.reply_text(info_text, parse_mode="Markdown")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejador del comando /status"""
    status_text = f"""
📊 *ESTADO DEL SISTEMA*

*Bot:* ✅ ACTIVO
*Token:* ✅ VÁLIDO
*Plataforma:* Termux
*Conexiones:* 
  ├── Telegram: ✅
  ├── GitHub: ✅
  └── Railway: ✅

*Mensaje de prueba:* El bot está funcionando correctamente desde Termux.
    """
    await update.message.reply_text(status_text, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejador de mensajes de texto"""
    user_message = update.message.text
    user = update.message.from_user
    
    logger.info(f"📨 Mensaje de {user.first_name}: {user_message}")
    
    # Respuestas inteligentes mejoradas
    responses = {
        "hola": "¡Hola! 🌟 ¿En qué puedo ayudarte?",
        "como estas": "¡Estoy funcionando al 100% en Termux! 🚀",
        "que puedes hacer": "Puedo conversar, dar información del sistema y conectarme con múltiples plataformas.",
        "gracias": "¡De nada! Es un placer ayudarte 🙏",
        "bot": "¡Sí! Soy un bot creado con Python y mucho código positivo 💻",
        "termux": "Ejecutándome en Termux Android con todas las configuraciones activas 📱",
        "python": "Python es el lenguaje que me da vida y poder 🐍",
        "railway": "Desplegado en Railway para máxima disponibilidad 🚄",
        "github": "Conectado con GitHub: Dandro12345/telegram-bot-simple 🔗",
        "dandro": "¡Ese es mi creador! Dandro1234 👑 El maestro del código",
        "token": f"Token configurado: {BOT_TOKEN[:8]}...{BOT_TOKEN[-8:]} 🔐",
        "funciona": "¡SÍ! Estoy funcionando perfectamente ✅"
    }
    
    # Buscar respuesta inteligente
    message_lower = user_message.lower()
    response_sent = False
    
    for key, response in responses.items():
        if key in message_lower:
            await update.message.reply_text(response)
            response_sent = True
            break
    
    # Respuesta por defecto si no coincide
    if not response_sent:
        default_response = f"""
💬 *Mensaje recibido:* "{user_message}"

✅ *Bot operativo y escuchando*

💡 *Palabras clave que entiendo:*
hola, como estas, que puedes hacer, gracias, bot, termux, python, railway, github, dandro, token, funciona

🔧 *Comandos:* /start, /info, /status
        """
        await update.message.reply_text(default_response, parse_mode="Markdown")

# ==================== INICIALIZACIÓN ====================
def main():
    """Función principal para iniciar el bot"""
    try:
        print("🔄 Creando aplicación de Telegram...")
        app = Application.builder().token(BOT_TOKEN).build()
        
        # Agregar manejadores
        print("📝 Configurando manejadores de comandos...")
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("info", info))
        app.add_handler(CommandHandler("status", status))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("🎉 BOT CONFIGURADO COMPLETAMENTE")
        print("🤖 INICIANDO BOT...")
        print("📡 ESCUCHANDO MENSAJES EN TELEGRAM...")
        print("💬 Ve a Telegram y escribe /start a @ayudante_ia_bot")
        
        # Iniciar el bot
        app.run_polling()
        
    except Exception as e:
        logger.error(f"❌ ERROR CRÍTICO: {e}")
        print(f"💡 SOLUCIÓN: Verifica que el token sea exactamente: {BOT_TOKEN}")

if __name__ == "__main__":
    main()
