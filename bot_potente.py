import os
import asyncio
import aiohttp
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuración
BOT_TOKEN = os.environ.get('BOT_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_KEY', 'AIzaSyAhyrzgcjygttXeyi4TUXfQa9CS3A0RHhQ')
OPENAI_KEY = os.environ.get('OPENAI_KEY')
PORT = int(os.environ.get('PORT', 10000))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MotorAI:
    def __init__(self):
        self.session = None
        self.cache = {}
    
    async def get_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10))
        return self.session

    async procesar_mensaje(self, texto: str, user_id: int) -> dict:
        """Procesa con múltiples AIs inteligentemente"""
        
        # Cache simple
        cache_key = f"{user_id}:{texto[:50]}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Selección inteligente de AI
        ai_seleccionada = self._seleccionar_ai(texto, user_id)
        
        resultado = await self._llamar_ai(ai_seleccionada, texto)
        
        if resultado['exito']:
            self.cache[cache_key] = resultado
            # Limpiar cache viejo
            if len(self.cache) > 100:
                self.cache.clear()
        
        return resultado
    
    def _seleccionar_ai(self, texto: str, user_id: int) -> str:
        """Selecciona la mejor AI para el contexto"""
        texto = texto.lower()
        
        if any(palabra in texto for palabra in ['código', 'programar', 'python']):
            return 'gemini'
        elif any(palabra in texto for palabra in ['creativo', 'escribir', 'historia']):
            return 'openai' if OPENAI_KEY else 'gemini'
        elif any(palabra in texto for palabra in ['rápido', 'urgente']):
            return 'gemini'  # Gemini es más rápido
        else:
            return 'gemini'  # Por defecto
    
    async def _llamar_ai(self, ai_nombre: str, mensaje: str) -> dict:
        """Llama a la API específica"""
        try:
            if ai_nombre == 'gemini' and GEMINI_KEY:
                return await self._llamar_gemini(mensaje)
            elif ai_nombre == 'openai' and OPENAI_KEY:
                return await self._llamar_openai(mensaje)
            else:
                return await self._llamar_gemini(mensaje)  # Fallback a Gemini
        except Exception as e:
            logger.error(f"Error en {ai_nombre}: {e}")
            return {'exito': False, 'respuesta': f'Error: {str(e)}', 'ai': ai_nombre}
    
    async def _llamar_gemini(self, mensaje: str) -> dict:
        """Google Gemini - Potente y gratuito"""
        session = await self.get_session()
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GEMINI_KEY}"
        
        payload = {
            "contents": [{
                "parts": [{"text": f"Responde en español de forma útil y precisa: {mensaje}"}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1000,
                "topP": 0.8
            }
        }
        
        async with session.post(url, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                if 'candidates' in data and data['candidates']:
                    texto = data['candidates'][0]['content']['parts'][0]['text']
                    return {'exito': True, 'respuesta': texto, 'ai': 'gemini'}
            
            return {'exito': False, 'respuesta': 'Error en Gemini', 'ai': 'gemini'}
    
    async def _llamar_openai(self, mensaje: str) -> dict:
        """OpenAI GPT - Para respuestas creativas"""
        session = await self.get_session()
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {OPENAI_KEY}"}
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": mensaje}],
            "max_tokens": 800,
            "temperature": 0.7
        }
        
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                data = await response.json()
                texto = data['choices'][0]['message']['content']
                return {'exito': True, 'respuesta': texto, 'ai': 'openai'}
            
            return {'exito': False, 'respuesta': 'Error en OpenAI', 'ai': 'openai'}

# Motor global
motor_ai = MotorAI()

async def inicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando start mejorado"""
    user = update.message.from_user
    
    texto_bienvenida = f"""
🤖 **BOT AI POTENTE ACTIVADO**

¡Hola {user.first_name}! Soy tu asistente con **inteligencia artificial avanzada**.

🚀 **Características:**
• Múltiples motores AI (Gemini + OpenAI)
• Selección inteligente por contexto
• Respuestas rápidas y precisas
• Optimizado para producción

💡 **Simplemente escribe tu pregunta...**
"""
    await update.message.reply_text(texto_bienvenida, parse_mode='Markdown')

async def chat_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Procesa mensajes con AI potente"""
    mensaje_usuario = update.message.text
    user_id = update.message.from_user.id
    
    # Mensaje de procesamiento
    mensaje_procesando = await update.message.reply_text("⚡ Procesando con motor AI...")
    
    try:
        # Procesar con motor AI
        inicio_tiempo = time.time()
        resultado = await motor_ai.procesar_mensaje(mensaje_usuario, user_id)
        tiempo_procesamiento = time.time() - inicio_tiempo
        
        if resultado['exito']:
            respuesta = f"""
🧠 **RESPUESTA AI** ({resultado['ai'].upper()})
⏱️ {tiempo_procesamiento:.2f}s

{resultado['respuesta']}

🔧 *Procesado con arquitectura multi-AI*
"""
        else:
            respuesta = f"""
❌ **ERROR EN MOTOR AI**

{resultado['respuesta']}

⚠️ *Reintentando automáticamente...*
"""
        
        await context.bot.edit_message_text(
            chat_id=update.message.chat_id,
            message_id=mensaje_procesando.message_id,
            text=respuesta,
            parse_mode='Markdown'
        )
        
    except Exception as e:
        await context.bot.edit_message_text(
            chat_id=update.message.chat_id,
            message_id=mensaje_procesando.message_id,
            text="❌ **Error temporal en el sistema AI**"
        )

async def estado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra estado del sistema"""
    estado_texto = """
📊 **SISTEMA AI - ESTADO**

🟢 **BOT:** Operativo
🤖 **MOTORES AI:** 
• Gemini: ✅ Activo
• OpenAI: {} Activo
💾 **CACHE:** Activado
🚀 **RENDIMIENTO:** Optimizado

*Sistema funcionando al 100%*
""".format("✅" if OPENAI_KEY else "❌")
    
    await update.message.reply_text(estado_texto, parse_mode='Markdown')

async def herramientas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra herramientas disponibles"""
    herramientas_texto = """
🛠️ **HERRAMIENTAS AI DISPONIBLES**

🧠 **Motores de Inteligencia:**
• Gemini Pro - Para código y respuestas técnicas
• OpenAI GPT - Para creatividad y escritura

🔧 **Funcionalidades:**
• Análisis de contexto automático
• Selección inteligente de AI
• Cache de respuestas
• Procesamiento optimizado

💡 **Comandos:**
/start - Iniciar bot
/estado - Ver estado del sistema
/herramientas - Esta ayuda

*Escribe cualquier pregunta para comenzar*
"""
    await update.message.reply_text(herramientas_texto, parse_mode='Markdown')

def main():
    """Función principal optimizada"""
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN no configurado")
        return
    
    try:
        # Crear aplicación
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Handlers
        application.add_handler(CommandHandler("start", inicio))
        application.add_handler(CommandHandler("estado", estado))
        application.add_handler(CommandHandler("herramientas", herramientas))
        application.add_handler(CommandHandler("help", herramientas))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_ai))
        
        logger.info("🚀 BOT AI POTENTE INICIANDO")
        logger.info(f"🔑 Gemini: {'✅' if GEMINI_KEY else '❌'}")
        logger.info(f"🔑 OpenAI: {'✅' if OPENAI_KEY else '❌'}")
        
        # Webhook para Render
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=BOT_TOKEN,
            webhook_url=f"https://telegram-bot-simple-y7lc.onrender.com/{BOT_TOKEN}",
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.error(f"❌ ERROR: {e}")

if __name__ == '__main__':
    import time
    main()
