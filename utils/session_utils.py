import os
from pathlib import Path
import shutil
import streamlit as st

TEMP_DIRS = [
    Path("data/temp"),
    Path("data/images_temp")
]

def clear_session():
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def clear_temp_files():
    for folder in TEMP_DIRS:
        if folder.exists():
            shutil.rmtree(folder)
            folder.mkdir(parents=True, exist_ok=True)
