import os
from io import BytesIO
from PIL import Image
from google import genai

# Inicializar cliente Gemini
client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)

MODEL_ID = "models/gemini-2.5-flash-image"

#-------------------------------
# Mapa de estilos
#-------------------------------
STYLE_MAP = {
    "Realista": (
        "fotografía realista de producto, iluminación natural controlada, "
        "texturas reales, proporciones exactas, nivel profesional"
    ),
    "Ilustración": (
        "ilustración digital detallada, estilo gráfico limpio, colores definidos, "
        "apariencia ilustrada, no fotográfica"
    ),
    "Minimalista": (
        "estilo minimalista, diseño limpio, pocos colores, fondo blanco puro, "
        "composición simple y elegante"
    ),
    "Publicidad": (
        "fotografía publicitaria profesional, iluminación dramática, "
        "alto contraste, enfoque comercial"
    )
}



def generate_image(prompt, style):
    
    style_description = STYLE_MAP.get(style, style)

    full_prompt = f"""
        
        Objeto a generar:
        {prompt}

        Clasificación obligatoria del objeto:        
        - bicicleta completa
        - componente de bicicleta
        - prenda de ciclismo

        Instrucciones estrictas (OBLIGATORIAS):
        -Mostrar ÚNICAMENTE el objeto solicitado.
        -Primer plano.
        -Objeto aislado.
        -Fondo neutro.
        -Sin personas ni escenas.
        -Sin elementos adicionales.

        PROHIBIDO INCLUIR:
        - bicicleta completa cuando no se solicite
        - ciclista o personas
        - paisajes
        - carreteras
        - ciudades
        - tiendas
        - escenarios
        - fondos complejos
        - logotipos
        - marcas de agua
        
        Contexto:
        El objeto pertenece exclusivamente al mundo del ciclismo y debe ser
técnicamente realista y coherente.

        Estilo visual:
        {style_description}
        """
    response = client.models.generate_content(
            model=MODEL_ID,
            contents=full_prompt
        )

    # Extraer imagen
    for part in response.candidates[0].content.parts:
        if part.inline_data and part.inline_data.mime_type.startswith("image"):
            image_bytes = part.inline_data.data
            return Image.open(BytesIO(image_bytes))

    return None
