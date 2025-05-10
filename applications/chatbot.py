from flask import Blueprint, request, jsonify, session
import google.generativeai as genai
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

# Crear el Blueprint para el chatbot
chatbot_bp = Blueprint('chatbot', __name__)

# Configurar Gemini correctamente
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key="AIzaSyBMbE4UVJJM5PQ0tBjonqc0lw3SQ6D9eAA")

# Mapeo de sesiones de chat
chat_sessions = {}

SYSTEM_PROMPT__ = """
Realiza una presentación: mi nombre es Joy, asistente de charla. La presentación debe ser corta y natural, como si fuera una persona real...
"""

SYSTEM_PROMPT = """
Tu nombre es Joy, un asistente de apoyo emocional diseñado para ayudar a los usuarios a gestionar la ansiedad, el estrés y otros temas de salud mental. Siempre brindas confianza y empatía. Tu enfoque combina la sensibilidad de un psicólogo con la cercanía de un amigo que escucha activamente.

Tono y Estilo de Comunicación

Empático y comprensivo: Evita respuestas mecánicas o frías.

Conciso y claro: Respuestas cortas (mínimo 2 palabras, máximo 2 oraciones).

No sobrecargar con preguntas: Formula solo las necesarias en el momento oportuno.

Validación emocional: Ayuda al usuario a empatizar consigo mismo.

Transmitir calma y seguridad: Ofrecer herramientas prácticas para reducir el estrés.

Realiza ejercicios de primeros auxilios psicológicos cuando la persona dice que está pasando por un mal estado emocional.
"""



@chatbot_bp.route('/get_response', methods=['POST'])
def process_message():
    user_message = request.json['message']
    chat_id = session.get('chat_id', str(uuid.uuid4()))

    try:
        if chat_id not in chat_sessions:
            chat_sessions[chat_id] = []

        chat_sessions[chat_id].append({"role": "user", "parts": [{"text": user_message}]})

        model = genai.GenerativeModel("gemini-2.0-flash", generation_config={
            'temperature': 0.9, 'top_p': 0.95, 'top_k': 40, 'max_output_tokens': 1024
        })

        response = model.generate_content(
            [{"role": "model", "parts": [{"text": SYSTEM_PROMPT}]}] + chat_sessions[chat_id]
        )

        bot_response = response.text
        chat_sessions[chat_id].append({"role": "model", "parts": [{"text": bot_response}]})

        return jsonify({'response': bot_response})

    except Exception as e:
        print(f"Error con la API de Gemini: {e}")
        return jsonify({'response': "Lo siento, tuve un problema procesando tu pregunta."})

@chatbot_bp.route('/reset_chat', methods=['POST'])
def reset_chat():
    chat_id = session.get('chat_id')
    if chat_id and chat_id in chat_sessions:
        del chat_sessions[chat_id]
    session['chat_id'] = str(uuid.uuid4())
    return jsonify({'status': 'success', 'message': 'Conversación reiniciada'})
