import streamlit as st
import requests

# ============================================================
# Configuración de la página
# ============================================================
st.set_page_config(
    page_title="InfoVIH - Chatbot Informativo",
    page_icon="🎗️",
    layout="centered"
)

# API Configuration
API_KEY = 'sk-6549f06fb6b941cea7442e5451561a58'  # <-- Coloca aquí tu API Key de DeepSeek
API_URL = 'https://api.deepseek.com/v1/chat/completions'

# ============================================================
# Prompt de sistema: define el "carácter" experto del bot
# ============================================================
SYSTEM_PROMPT = """
Eres "InfoVIH", un asistente virtual educativo especializado EXCLUSIVAMENTE en brindar
información clara, precisa y actualizada sobre el VIH (Virus de Inmunodeficiencia Humana) y el SIDA.

Tus principios son:
1. Brindas información basada en evidencia científica y en guías de organismos de salud
   reconocidos (OMS, ONUSIDA, CDC, ministerios de salud).
2. Hablas con un tono cálido, respetuoso, empático y libre de juicios o estigma.
3. Cubres temas como: formas de transmisión y NO transmisión, prevención (preservativo, PrEP, PEP),
   pruebas de detección, tratamiento antirretroviral, indetectable = intransmisible (I=I),
   vivir con VIH, derechos de las personas con VIH, y desmentir mitos comunes.
4. NUNCA diagnosticas a una persona ni das indicaciones de dosis de medicamentos.
   Para diagnóstico, tratamiento personalizado o resultados de pruebas, siempre remites
   a un médico, centro de salud o línea de atención especializada.
5. Si detectas angustia emocional, una posible exposición reciente de riesgo, o pensamientos
   de autolesión, respondes con calma, validas la emoción y recomiendas buscar ayuda
   profesional o de emergencia de inmediato, sin dejar de responder con información útil.
6. Si te preguntan algo fuera del tema VIH/salud sexual, indicas amablemente que tu
   especialidad es el VIH y rediriges la conversación a ese tema.
7. Usas lenguaje sencillo, evitas tecnicismos innecesarios y explicas los términos médicos
   cuando los usas.

Recuerda siempre cerrar temas sensibles recordando que este chatbot no sustituye una
consulta médica profesional.
"""

# ============================================================
# Función para llamar a la API
# ============================================================
def enviar_mensaje(historial, modelo='deepseek-chat'):
    """Envía el historial de conversación al API y retorna la respuesta"""
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    # Construimos la lista de mensajes incluyendo el system prompt
    mensajes = [{'role': 'system', 'content': SYSTEM_PROMPT}] + historial

    data = {
        'model': modelo,
        'messages': mensajes,
        'temperature': 0.4  # Respuestas más consistentes y menos "creativas"
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        if response.status_code != 200:
            error_detail = response.json() if response.text else "Sin detalles"
            return f"❌ Error {response.status_code}: {error_detail}"
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.Timeout:
        return "⏰ Tiempo de espera agotado. Por favor, intenta de nuevo."
    except requests.exceptions.RequestException as e:
        return f"🔌 Error de conexión: {e}"
    except Exception as e:
        return f"⚠️ Error Inesperado: {e}"


# ============================================================
# Aplicación principal
# ============================================================
def main():
    # Título y descripción
    st.title("🎗️ InfoVIH - Chatbot Informativo")
    st.markdown(
        "Pregunta lo que quieras saber sobre **prevención, pruebas, tratamiento, "
        "vida con VIH y más**. Este espacio es confidencial, respetuoso y libre de estigma."
    )
    st.markdown("---")

    # Aviso importante siempre visible
    st.info(
        "ℹ️ **Aviso:** Este chatbot ofrece información educativa y **no reemplaza** "
        "una consulta médica. Ante dudas sobre tu situación personal, acude a un "
        "centro de salud o línea de atención especializada.",
        icon="ℹ️"
    )

    # Sidebar con información y recursos
    with st.sidebar:
        st.header("⚙️ Configuración")
        st.write("Modelo: DeepSeek Chat")
        st.write("Estado: ✅ Conectado")

        if st.button("🗑️ Limpiar conversación"):
            st.session_state.messages = []
            st.rerun()

        st.markdown("---")
        st.subheader("📞 Recursos de ayuda")
        st.markdown(
            "- Línea nacional de salud sexual (verifica el número de tu país)\n"
            "- Centro de salud u hospital más cercano\n"
            "- ONUSIDA: [unaids.org](https://www.unaids.org)\n"
        )
        st.markdown("---")
        st.caption("Desarrollado con Streamlit y DeepSeek API")

    # Inicializar historial
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Verificar la API al inicio (solo una vez)
    if "api_verificada" not in st.session_state:
        test_response = enviar_mensaje([{"role": "user", "content": "Hola"}])
        if "Error" in test_response or "❌" in test_response:
            st.error(f"⚠️ No se pudo conectar con la API: {test_response}")
            st.info("Por favor, verifica tu API Key en https://platform.deepseek.com/")
            return
        st.session_state.api_verificada = True

    # Mostrar mensajes anteriores
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Mensaje de bienvenida si no hay historial
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            st.markdown(
                "¡Hola! 👋 Soy **InfoVIH**. Puedes preguntarme sobre prevención, "
                "pruebas de detección, tratamiento, PrEP/PEP, o cualquier duda "
                "relacionada con el VIH. ¿En qué puedo ayudarte hoy?"
            )

    # Input del usuario
    if prompt := st.chat_input("Escribe tu pregunta sobre VIH aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Buscando información confiable..."):
                response = enviar_mensaje(st.session_state.messages)
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()