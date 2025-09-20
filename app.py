import streamlit as st
from PIL import Image
import pytesseract
from googletrans import Translator
from gtts import gTTS
import os

# Configuración de la página
st.set_page_config(page_title="OCR Traductor", page_icon="📝")

# Fondo y estilo de letras
page_bg = """
<style>
    .stApp {
        background-color: #b6ad90;
        color: #582f0e;
    }
    h1, h2, h3, h4, h5, h6, p, label {
        color: #582f0e !important;
    }
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# Título
st.title("OCR Traductor con Voz")

# Subir imagen
uploaded_file = st.file_uploader("Sube una imagen para extraer texto", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen subida", use_column_width=True)

    # Extraer texto con Tesseract
    text = pytesseract.image_to_string(image)
    st.subheader("Texto detectado:")
    st.write(text)

    if text.strip():
        # Traducir texto
        translator = Translator()
        translated = translator.translate(text, dest="es")
        st.subheader("Texto traducido al español:")
        st.write(translated.text)

        # Convertir a voz
        tts = gTTS(translated.text, lang="es")
        tts.save("output.mp3")

        st.audio("output.mp3", format="audio/mp3")
