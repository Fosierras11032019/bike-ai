from google import genai
import os

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_ID = "models/gemini-2.5-flash"


def improve_text(text: str, action: str) -> str:
    """
    Procesa un texto publicitario según la acción seleccionada
    por el rol Redactor.
    """

    if action == "Mejorar":
        prompt = f"""
            Actúa como un redactor publicitario profesional y ético experto en ciclismo.
            Evita lenguaje discriminatorio, exageraciones engañosas
            o afirmaciones no verificables.

            Reescribe el siguiente texto en español,
            mejorando claridad, impacto y persuasión
            sin cambiar la idea principal.
            
            Genera máximo hasta 2 opciones de mejora.

            Texto original:
            {text}
            """

    elif action == "Resumir":
        prompt = f"""
            Actúa como un redactor publicitario profesional y ético experto en ciclismo.
            Evita lenguaje discriminatorio, exageraciones engañosas
            o afirmaciones no verificables.

            Resume el siguiente texto en español, conservando las ideas clave
            y eliminando información redundante.

            Texto original:
            {text}
            """

    elif action == "Expandir":
        prompt = f"""
            Actúa como un redactor publicitario profesional y ético experto en ciclismo.
            Evita lenguaje discriminatorio, exageraciones engañosas
            o afirmaciones no verificables.

            Amplía el siguiente texto en español, agregando nuevas ideas,
            beneficios del producto y lenguaje inspirador, manteniendo coherencia
            con el mensaje original.

            Texto original:
            {text}
            """

    elif action == "Corregir":
        prompt = f"""
            Actúa como un corrector de estilo profesional y ético experto en ciclismo.
            Evita lenguaje discriminatorio, exageraciones engañosas
            o afirmaciones no verificables.

            Corrige errores gramaticales, ortográficos y de estilo en el siguiente texto,
            mejorando la redacción sin alterar el significado.

            Texto original:
            {text}
            """

    elif action == "Variar":
        prompt = f"""
            Actúa como un redactor publicitario profesional muy creativo y ético, experto en ciclismo.
            Evita lenguaje discriminatorio, exageraciones engañosas
            o afirmaciones no verificables..

            Genera 2 variaciones diferentes del siguiente texto en español.
            Las versiones deben transmitir la misma idea, pero con redacciones distintas
            y enfoques creativos variados.

            Texto original:
            {text}
            """

    else:
        raise ValueError("Acción no soportada")

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt
    )

    return response.text.strip()
