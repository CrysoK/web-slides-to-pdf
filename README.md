# 📄 JessyInk to PDF Converter

Convierte tus presentaciones [Inkscape](https://inkscape.org/) + [JessyInk](https://code.google.com/archive/p/jessyink/) a formato PDF, manteniendo cada efecto y transición como una página individual.

## 🚀 Características

- 🎯 **Captura paso a paso:** Convierte cada "clic" o efecto de la presentación en una página del PDF.
- 🖼️ **Alta Calidad:** Utiliza un motor de navegador real (Chromium) para renderizar los SVG exactamente como se ven en pantalla.
- 📦 **Eficiencia:** El modo CLI permite automatización sin sobrecarga de interfaz gráfica.

## ☁️ Uso Online (sin descargas)

La forma más rápida de usar la herramienta es a través de nuestra aplicación en la nube. No necesitas instalar nada.

👉 **[Abrir JessyInk Converter en Streamlit Cloud](https://jessyink-converter.streamlit.app/)**

---

## 💻 Uso Local (recomendado: `uv`)

Si prefieres ejecutar la herramienta en tu propio equipo (para mayor privacidad o para procesar múltiples archivos por lotes), recomendamos usar **[uv](https://docs.astral.sh/uv/)**.

Esta herramienta gestiona el entorno virtual automáticamente y es extremadamente rápida.

### 1. Preparación

Asegúrate de tener instalado `uv` y clona el repositorio:

```bash
# Instalar uv (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Instalar uv (Windows)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Clonar repo
git clone https://github.com/tu-usuario/jessyink-converter.git
cd jessyink-converter
```

### 2. Opción A: Usar solo la Línea de Comandos (CLI)

Esta es la opción más ligera. **No instala Streamlit** ni otras dependencias web, solo lo necesario para convertir el PDF.

```bash
# 1. Instalar dependencias base (sin Streamlit)
uv sync

# 2. Instalar el navegador necesario (solo la primera vez)
uv run playwright install chromium

# 3. Ejecutar el conversor
uv run cli.py tu-presentacion.svg
```

**Ejemplos de uso CLI:**

```bash
# Convertir con máxima calidad (escala 8x)
uv run cli.py presentacion.svg -q 8

# Procesar una carpeta completa
uv run cli.py ./mis-archivos/
```

### 3. Opción B: Ejecutar la Interfaz Web localmente

Si deseas la interfaz gráfica en tu propia máquina, necesitas instalar el grupo de dependencias `web`.

```bash
# 1. Instalar dependencias incluyendo Streamlit
uv sync --extra web

# 2. Instalar navegador (si no lo hiciste antes)
uv run playwright install chromium

# 3. Iniciar la app
uv run streamlit run app.py
```

## 🛠 Desarrollo y Despliegue

Este proyecto utiliza `pyproject.toml` para la gestión de dependencias moderna.
El archivo `requirements.txt` se incluye principalmente para compatibilidad con el entorno de despliegue de Streamlit Cloud.
