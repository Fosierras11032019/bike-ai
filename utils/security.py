from cryptography.fernet import Fernet
import os

# Clave desde variable de entorno
FERNET_KEY = os.getenv("FERNET_KEY")

if not FERNET_KEY:
    raise RuntimeError("FERNET_KEY no definida")

fernet = Fernet(FERNET_KEY.encode())

def encrypt_data(data: str) -> bytes:
    return fernet.encrypt(data.encode("utf-8"))

def decrypt_data(token: bytes) -> str:
    return fernet.decrypt(token).decode("utf-8")
