import json
import base64
from datetime import datetime
from pathlib import Path

from utils.security import encrypt_data, decrypt_data

HISTORY_FILE = Path("data/text_history.json")

# -------------------------------------------------
# Guardar versión (con cifrado + base64)
# -------------------------------------------------
def save_version(role, action, original, result):
    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "role": role,
        "action": action,
        # bytes -> base64 string
        "original_text": base64.b64encode(
            encrypt_data(original)
        ).decode("utf-8"),
        "result_text": base64.b64encode(
            encrypt_data(result)
        ).decode("utf-8")
    }

    if not HISTORY_FILE.exists():
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        HISTORY_FILE.write_text("[]", encoding="utf-8")

    history = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    history.append(record)

    HISTORY_FILE.write_text(
        json.dumps(history, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


# -------------------------------------------------
# Cargar historial (base64 + descifrado)
# -------------------------------------------------
def load_history():
    if not HISTORY_FILE.exists():
        return []

    raw_history = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    decoded_history = []

    for item in raw_history:
        try:
            decoded_history.append({
                "timestamp": item["timestamp"],
                "role": item["role"],
                "action": item["action"],
                "original_text": decrypt_data(
                    base64.b64decode(item["original_text"])
                ),
                "result_text": decrypt_data(
                    base64.b64decode(item["result_text"])
                )
            })
        except Exception:
            # Si un registro no se puede descifrar, se ignora
            continue

    return decoded_history
