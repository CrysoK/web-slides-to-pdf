import asyncio
import img2pdf
import tempfile
from pathlib import Path
from playwright.async_api import async_playwright

TRANSITION_DELAY = 0.6


async def convert_presentation(
    svg_path: Path, output_path: Path, quality: int, progress_callback=None
):
    """
    Convierte una presentación SVG JessyInk a un archivo PDF.

    Args:
        svg_path (Path): Ruta al archivo SVG de entrada.
        output_path (Path): Ruta donde se guardará el PDF.
        quality (int): Factor de escala para el viewport (DPI).
        progress_callback (func, optional): Función (step, total, msg) para reportar progreso.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(device_scale_factor=quality)
        page = await context.new_page()

        file_url = svg_path.absolute().as_uri()

        try:
            if progress_callback:
                progress_callback(0, 0, "Cargando presentación...")

            await page.goto(file_url)
            await page.wait_for_load_state("networkidle")

            is_jessyink = await page.evaluate(
                "typeof slides !== 'undefined' && slides.length > 0"
            )
            if not is_jessyink:
                raise ValueError(
                    "El archivo no es una presentación válida de JessyInk."
                )

            data = await page.evaluate(
                """() => {
                return {
                    width: window.WIDTH || 1024,
                    height: window.HEIGHT || 768,
                    structure: Array.from(slides).map((s, i) => ({
                        slide_index: i,
                        effect_count: (s.effects) ? s.effects.length : 0
                    }))
                }
            }"""
            )

            width = data["width"]
            height = data["height"]
            structure = data["structure"]

            await page.set_viewport_size({"width": int(width), "height": int(height)})

            total_steps = sum([1 + s["effect_count"] for s in structure])
            image_files = []
            current_step = 0

            with tempfile.TemporaryDirectory() as temp_dir_path:
                temp_dir = Path(temp_dir_path)

                for slide in structure:
                    slide_num = slide["slide_index"] + 1
                    max_effects = slide["effect_count"]

                    for effect_step in range(max_effects + 1):
                        current_step += 1

                        if progress_callback:
                            progress_callback(
                                current_step,
                                total_steps,
                                f"Capturando paso {current_step} de {total_steps}",
                            )

                        hash_url = f"{file_url}#{slide_num}_{effect_step}"
                        await page.goto(hash_url)
                        await page.reload()
                        await asyncio.sleep(TRANSITION_DELAY)

                        img_name = f"{current_step:04d}.png"
                        img_path = temp_dir / img_name

                        await page.screenshot(path=img_path, type="png")
                        image_files.append(img_path)

                if progress_callback:
                    progress_callback(total_steps, total_steps, "Ensamblando PDF...")

                if not image_files:
                    raise RuntimeError("No se generaron imágenes para el PDF.")

                with open(output_path, "wb") as f:
                    f.write(img2pdf.convert([str(p) for p in image_files]))

        finally:
            await browser.close()
