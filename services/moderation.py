import re

def moderate_content(text):
    text = text.lower()

    # Categorías éticas
    offensive_terms = [
        "miserable", "miserables", "mendigo", "mendigos",
        "pobre", "pobres", "ignorante", "ignorantes",
        "basura", "asqueroso", "asquerosos"
    ]

    discriminatory_patterns = [
        r"no\s+es\s+para\s+\w+",
        r"no\s+son\s+para\s+\w+",
        r"solo\s+para\s+\w+",
        r"gente\s+como\s+ellos",
        r"no\s+merecen"
    ]

    # 1️⃣ Palabras ofensivas explícitas
    for term in offensive_terms:
        if term in text:
            return False, (
                "El texto contiene lenguaje ofensivo o despectivo "
                "hacia personas o grupos sociales."
            )

    # 2️⃣ Patrones de exclusión / discriminación
    for pattern in discriminatory_patterns:
        if re.search(pattern, text):
            return False, (
                "El texto presenta expresiones excluyentes o discriminatorias, "
                "lo cual no está permitido."
            )

    return True, "Contenido aprobado"
