import streamlit as st
from PIL import Image
import pytesseract
from googletrans import Translator
from gtts import gTTS
import os

# --- Configuración de la página ---
st.set_page_config(page_title="OCR Traductor con Voz", page_icon="📝")

# --- Fondo y estilo personalizado ---
page_bg = """
<style>
    .stApp {
        background-color: #b6ad90;
        color: #582f0e;
    }
    h1, h2, h3, h4, h5, h6, p, label {
        color: #582f0e !important;
    }
    .stButton>button {
        background-color: #582f0e;
        color: white;
        border-radius: 8px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #7f5539;
    }
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# --- Título principal ---
st.title("📝 OCR Traductor con Voz")

# --- Subir imagen ---
uploaded_file = st.file_uploader("Sube una imagen para extraer texto", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📷 Imagen subida", use_column_width=True)

    # --- Sección de configuración de idioma ---
    st.markdown("### 🌍 Opciones de idioma")
    col1, col2 = st.columns(2)

    with col1:
        idioma_origen = st.selectbox(
            "Idioma del texto original",
            ["auto", "en", "es", "fr", "de", "it", "pt"],
            index=0
        )
    with col2:
        idioma_destino = st.selectbox(
            "Traducir a",
            ["es", "en", "fr", "de", "it", "pt"],
            index=0
        )

    # --- Procesar OCR ---
    with st.spinner("🔍 Extrayendo texto de la imagen..."):
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=custom_config)

    if text.strip():
        st.subheader("📝 Texto detectado:")
        st.write(text)

        # --- Traducir texto ---
        translator = Translator()
        translated = translator.translate(text, src=idioma_origen, dest=idioma_destino)
        st.subheader("🌎 Texto traducido:")
        st.write(translated.text)

        # --- Sección de voz ---
        st.markdown("### 🎧 Opciones de voz")
        voz_idioma = st.selectbox("Idioma de la voz", ["es", "en", "fr", "it", "pt"], index=0)
        velocidad = st.slider("Velocidad de voz", 0.5, 1.5, 1.0)

        if st.button("🔊 Generar y reproducir voz"):
            with st.spinner("🎙️ Generando audio..."):
                tts = gTTS(translated.text, lang=voz_idioma, slow=(velocidad < 1.0))
                tts.save("output.mp3")

            st.audio("output.mp3", format="audio/mp3")

            # --- Botón para descargar el audio ---
            with open("output.mp3", "rb") as f:
                st.download_button("⬇️ Descargar audio", f, file_name="traduccion.mp3")

    else:
        st.warning("⚠️ No se detectó texto en la imagen.")

