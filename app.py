import streamlit as st
import asyncio
import tempfile
import subprocess
import sys
import os
from pathlib import Path
from core import convert_presentation

st.set_page_config(page_title="JessyInk a PDF", page_icon="📄", layout="centered")

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


@st.cache_resource
def ensure_playwright_installed():
    """
    Instala los binarios de Playwright (Chromium).
    Usamos @st.cache_resource para que esto solo corra una vez al iniciar la app.
    """
    try:
        # Usamos sys.executable para asegurar que usamos el entorno python correcto
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            check=True,
            capture_output=True,
        )
        print("✅ Navegador Chromium verificado/instalado.")
    except subprocess.CalledProcessError as e:
        # Si falla, mostramos el error en la interfaz
        st.error(f"Error crítico instalando el navegador: {e}")
        if e.stderr:
            st.code(e.stderr.decode())
        st.stop()


# Ejecutar la instalación al inicio
ensure_playwright_installed()

# --- Interfaz de Usuario ---
st.title("📄 JessyInk a PDF Converter")
st.markdown(
    """
Convierte tus presentaciones **SVG** (creadas con Inkscape + JessyInk) a formato **PDF**.
La herramienta captura cada "paso" de la animación como una página individual.
"""
)

uploaded_file = st.file_uploader("Sube tu archivo .svg", type="svg")

col1, col2 = st.columns(2)
with col1:
    quality = st.slider(
        "Calidad (Escala)",
        min_value=1,
        max_value=8,
        value=4,
        help="Aumenta la resolución de las capturas. Mayor calidad = archivo más pesado y proceso más lento.",
    )

if uploaded_file is not None:
    if st.button("Convertir a PDF", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()

        def web_progress(current, total, message):
            status_text.text(f"⏳ {message}")
            if total > 0:
                progress_bar.progress(min(current / total, 1.0))

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            input_path = tmp_path / "input.svg"
            output_path = tmp_path / "output.pdf"

            with open(input_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            try:
                # Ejecutar la conversión
                asyncio.run(
                    convert_presentation(input_path, output_path, quality, web_progress)
                )

                progress_bar.progress(1.0)
                status_text.text("✅ ¡Conversión completada!")
                st.success("Tu PDF está listo.")

                with open(output_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Descargar PDF",
                        data=f,
                        file_name=f"{Path(uploaded_file.name).stem}.pdf",
                        mime="application/pdf",
                    )

            except Exception as e:
                status_text.empty()
                st.error(f"Ocurrió un error durante la conversión: {e}")
