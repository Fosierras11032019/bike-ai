import re

# Palabras clave permitidas en la tienda Bike Store
ALLOWED_KEYWORDS = [
    # Bicicletas
    "bicicleta", "ruta", "montaña", "mtb", "pista", "bmx", "gravel",

    # Componentes
    "rueda", "llanta", "neumático", "marco", "cuadro",
    "manubrio", "manillar", "sillín", "asiento",
    "pedales", "cadena", "cassette", "piñón",
    "frenos", "disco", "cambios", "desviador",

    # Accesorios
    "casco", "guantes", "gafas", "luces", "botella",
    "portacaramañola", "bomba", "herramienta",

    # Ropa de ciclismo
    "jersey", "camiseta", "culotte", "licra",
    "chaqueta", "ropa ciclismo"
    ]

def is_request_in_store_domain(prompt: str) -> bool:
    """
    Valida si la petición del usuario corresponde
    a productos que se venden en Bike Store.
    """
    prompt = prompt.lower()

    for keyword in ALLOWED_KEYWORDS:
        # Coincidencia exacta por palabra (evita falsos positivos)
        if re.search(rf"\b{keyword}\b", prompt):
            return True

    return False
