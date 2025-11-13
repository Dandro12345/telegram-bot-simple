import os
import logging
import aiohttp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuración logging PARA VER ERRORES
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Variables de entorno
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_KEY')
PORT = int(os.environ.get('PORT', 10000))

async def gemini_ai(mensaje: str) -> str:
    """Función mejorada con mejor manejo de errores"""
    try:
        logger.info(f"🔍 Consultando Gemini: {mensaje[:50]}...")
        
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_KEY}"
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Responde en español de forma útil y concisa: {mensaje}"
                }]
            }],
            "generationConfig": {
                "maxOutputTokens": 800,
                "temperature": 0.7
            }
        }
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'candidates' in data and data['candidates']:
                        texto = data['candidates'][0]['content']['parts'][0]['text']
                        logger.info("✅ Respuesta Gemini obtenida")
                        return texto
                    else:
                        return "❌ No se pudo generar respuesta"
                else:
                    return f"❌ Error API: {response.status}"
                    
    except Exception as e:
        logger.error(f"💥 Error en Gemini: {e}")
        return "⚠️ Servicio AI temporalmente no disponible"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando start mejorado"""
    user = update.message.from_user
    logger.info(f"👤 Usuario {user.id} inició chat")
    
    await update.message.reply_text(
        f"🧠 **¡Hola {user.first_name}!**\n\n"
        f"Soy tu asistente con **Google Gemini AI**\n\n"
        f"🤖 **Características:**\n"
        f"• Respuestas inteligentes\n"
        f"• Procesamiento en la nube\n"
        f"• Completamente funcional\n\n"
        f"💡 **Escribe tu pregunta...**"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejador de chat optimizado"""
    user_message = update.message.text
    user_id = update.message.from_user.id
    
    logger.info(f"💬 Mensaje de {user_id}: {user_message[:30]}...")
    
    # Mensaje de procesamiento
    processing_msg = await update.message.reply_text("⚡ Consultando AI...")
    
    try:
        # Obtener respuesta
        respuesta = await gemini_ai(user_message)
        
        # Enviar respuesta
        await context.bot.edit_message_text(
            chat_id=update.message.chat_id,
            message_id=processing_msg.message_id,
            text=respuesta
        )
        
        logger.info(f"✅ Respuesta enviada a {user_id}")
        
    except Exception as e:
        logger.error(f"💥 Error en chat: {e}")
        await context.bot.edit_message_text(
            chat_id=update.message.chat_id,
            message_id=processing_msg.message_id,
            text="❌ Error temporal. Intenta nuevamente."
        )

def main():
    """Función principal con verificación completa"""
    logger.info("🚀 INICIANDO BOT DEFINITIVO...")
    
    # Verificar variables críticas
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN no configurado")
        return
        
    if not GEMINI_KEY:
        logger.error("❌ GEMINI_KEY no configurado")
        return
    
    try:
        # Crear aplicación
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
        
        logger.info("✅ Bot configurado correctamente")
        logger.info(f"🌐 URL: https://telegram-bot-simple-1.onrender.com")
        
        # Iniciar webhook
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=BOT_TOKEN,
            webhook_url=f"https://telegram-bot-simple-1.onrender.com/{BOT_TOKEN}",
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.critical(f"💥 ERROR FATAL: {e}")

if __name__ == '__main__':
    main()
# Última actualización: Wed Nov 12 23:14:24 -04 2025
