from PIL import Image
import io

MAX_SIZE = (300, 300)  # 8x8 cm aprox

def prepare_image_for_gallery(image: Image.Image):
    """
    Recibe una imagen PIL, la redimensiona y la devuelve como buffer PNG
    """
    img = image.copy()
    img.thumbnail(MAX_SIZE)

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer
