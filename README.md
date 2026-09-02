# actividad-4

# 🎗️ InfoVIH - Chatbot Informativo sobre VIH

Un chatbot hecho con Streamlit que responde preguntas sobre VIH: prevención, pruebas,
tratamiento, PrEP/PEP y vida con VIH. Usa la API de DeepSeek para generar las respuestas.

> ⚠️ Este chatbot es informativo, no reemplaza a un médico. Ante dudas personales,
> consulta con un profesional de salud.

## ¿Qué hace?

Es un chat como el de WhatsApp: el usuario escribe una pregunta, el bot responde.
Por dentro, cada vez que el usuario escribe algo, la app le manda ese mensaje (y
todo el historial de la conversación) a la API de DeepSeek, junto con instrucciones
ocultas ("system prompt") que le dicen al modelo: "eres un experto en VIH, responde
con empatía, no diagnostiques, y si detectas angustia recomienda ayuda profesional".
La API responde y esa respuesta se muestra en pantalla.

## Cómo correrlo

1. Instala las librerías necesarias:
   ```bash
   pip install streamlit requests
   ```

2. Pon tu API Key de DeepSeek dentro de `app.py`, en la línea:
   ```python
   API_KEY = ''
   ```

3. Corre la app:
   ```bash
   streamlit run app.py
   ```

4. Se abrirá solo en tu navegador, normalmente en `http://localhost:8501`.

## Partes del código (explicadas simple)

- **`SYSTEM_PROMPT`**: es como el "manual de comportamiento" del bot. Aquí le decimos
  de qué temas puede hablar y cómo debe comportarse.
- **`enviar_mensaje()`**: es la función que habla con la API de DeepSeek. Le manda el
  mensaje del usuario y recibe la respuesta.
- **`st.session_state.messages`**: es la memoria de la app. Ahí se guardan todos los
  mensajes (del usuario y del bot) mientras la página sigue abierta.
- **`main()`**: arma toda la interfaz visual (título, barra lateral, caja de chat).

## Importante sobre la API Key

Como subiste esto a GitHub, ten cuidado de no dejar tu API Key visible en el código
público, porque cualquiera podría usarla. Lo ideal es sacarla del código y ponerla
como variable de entorno o en un archivo `secrets.toml` que no se suba al repo.
Si quieres, te ayudo a hacer ese cambio.

## Recursos de ayuda

- [ONUSIDA](https://www.unaids.org)
- [OMS - VIH/SIDA](https://www.who.int/es/health-topics/hiv-aids)
- Línea de salud sexual o centro de salud de tu país
