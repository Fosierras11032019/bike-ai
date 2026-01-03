import re

# Sustantivos PROHIBIDOS (infraestructura / escenarios)
FORBIDDEN_TERMS = [
    "edificio","torre","ascensor"
]

# ✅ Dominio permitido: ciclismo, productos, experiencia deportiva
ALLOWED_TERMS = [
    # Ciclismo general
    "ciclismo", "ciclista", "bicicleta", "pedalear",

    # Tipos de bicicleta
    "ruta", "montaña", "mtb", "pista", "bmx", "gravel",

    # Componentes y repuestos
    "rueda", "llanta", "neumático", "marco", "cuadro",
    "manubrio", "manillar", "sillín", "asiento",
    "pedales", "cadena", "cassette", "piñón",
    "frenos", "disco", "cambios", "desviador",

    # Accesorios
    "casco", "guantes", "gafas", "luces",
    "botella", "caramañola", "bomba", "herramienta",

    # Ropa
    "jersey", "camiseta", "culotte", "licra",
    "chaqueta", "ropa", "indumentaria", 

    # Experiencia y desempeño
    "rendimiento", "desempeño", "resistencia",
    "velocidad", "competencia", "entrenamiento",
    "desafío", "logro", "experiencia", "aventura"
]

# Lenguaje comercial y de marketing
COMMERCIAL_TERMS = [
    "tienda", "selección", "modelo", "productos",
    "oferta", "catálogo", "marca", "línea",
    "colección", "ventas", "comprar", "adquirir",
    "disponible", "ideal", "necesidades", "estilo"
]

def is_text_within_store_domain(text: str) -> tuple[bool, str]:
    """
    Valida que el texto esté dentro del alcance
    del ciclismo y de los productos de Bike Store.

    Retorna:
    (True, "") si es válido
    (False, mensaje) si debe bloquearse
    """

    text = text.lower()

    # 1️⃣ Bloqueo por términos prohibidos
    for term in FORBIDDEN_TERMS:
        if re.search(rf"\b{term}\b", text):
            return (
                False,
                "El texto hace referencia a infraestructura o escenarios "
                "que no forman parte del alcance de la tienda Bike Store."
            )

    # 2️⃣ Validación por pertenencia al dominio del ciclismo
    for term in ALLOWED_TERMS + COMMERCIAL_TERMS:
        if re.search(rf"\b{term}\b", text):
            return True, ""

    # 3️⃣ Texto completamente fuera del dominio
    return (
        False,
        "El texto no está relacionado con el ciclismo ni con productos, "
        "repuestos, prendas, experiencias o desafíos propios de Bike Store. "
        "Por favor redacta contenido alineado con la naturaleza y propósito de la tienda."
    )
