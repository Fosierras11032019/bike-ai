def moderate_content(text):
    forbidden  = ["violencia", "odio", "discriminación"]
    
    for word in forbidden:
        if word in text.lower():
            return False, f"Contenido no permitido: {word}"
    
    return True, "Contenido aprobado"
