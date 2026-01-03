import streamlit as st
from services.image_generator import generate_image
from services.text_editor import improve_text
from services.moderation import moderate_content
from utils.image_gallery import prepare_image_for_gallery
from utils.text_history import save_version, load_history
from utils.session_utils import clear_session, clear_temp_files
from auth.roles import get_permissions

# ================================
# Configuración de página
# ================================
st.set_page_config(
    page_title="BikeCreative AI",
    layout="wide"
)

# ================================
# Cargar estilos
# ================================
with open("assets/styles.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ================================
# Estado de sesión
# ================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_role" not in st.session_state:
    st.session_state.user_role = None

if "gallery" not in st.session_state:
    st.session_state.gallery = []

if "image_generated" not in st.session_state:
    st.session_state.image_generated = False

# ================================
# SIDEBAR – IDENTIDAD + ACCESO
# ================================
with st.sidebar:
    st.markdown("🚴 **TIENDA BIKE STORE**", unsafe_allow_html=True)
    st.markdown("**Módulo Creativo**", unsafe_allow_html=True)
    st.markdown("<hr class='sidebar-divider'>", unsafe_allow_html=True)

    st.subheader("Acceso")

    with st.expander("Seguridad y privacidad"):
        st.info(
            "Los textos e imágenes generados se almacenan cifrados "
            "mediante **Fernet (AES-128)** para garantizar confidencialidad."
        )

    with st.expander("Uso ético de la IA"):
        st.info(
            "Este sistema mitiga sesgos, evita contenido inapropiado "
            "y promueve el respeto a derechos de autor."
        )

    # ---------------- LOGIN ----------------
    if not st.session_state.logged_in:
        role = st.selectbox(
            "Selecciona tu rol",
            ["Diseñador", "Redactor"]
        )

        if st.button("Ingresar"):
            st.session_state.logged_in = True
            st.session_state.user_role = role
            st.rerun()

    # ---------------- SESIÓN ACTIVA ----------------
    else:
        st.success(f"Sesión activa: {st.session_state.user_role}")

        if st.button("Salir"):
            clear_session()
            clear_temp_files()
            st.rerun()

# ================================
# CONTENIDO PRINCIPAL
# ================================
st.title("BikeCreative AI")
st.caption("IA Generativa para Marketing de Bicicletas")

if not st.session_state.logged_in:
    st.info("Por favor, inicia sesión desde el menú lateral.")
    st.stop()

permissions = get_permissions(st.session_state.user_role)

# ================================
# MENÚ SEGÚN ROL
# ================================
menu_options = []

if "texto" in permissions:
    menu_options.append("Edición de texto")

if "imagenes" in permissions:
    menu_options.append("Generación de imágenes")

option = st.sidebar.radio(
    "Funciones disponibles",
    menu_options
)

# ================================
# EDICIÓN DE TEXTO
# ================================
if option == "Edición de texto":

    st.header("Edición de contenido")

    if "text_input" not in st.session_state:
        st.session_state.text_input = ""

    if "pending_text" in st.session_state:
        st.session_state.text_input = st.session_state.pending_text
        del st.session_state.pending_text

    text = st.text_area(
        "Texto publicitario",
        key="text_input",
        height=150
    )

    action = st.selectbox(
        "Acción",
        ["Mejorar", "Resumir", "Expandir", "Corregir", "Variar"]
    )

    if st.button("Procesar texto", key="btn_procesar_texto"):

        # 1️⃣ Validación de dominio semántico
        is_valid, validation_msg = is_text_within_store_domain(text)
        if not is_valid:
            st.warning(validation_msg)
            st.stop()

        # 2️⃣ Moderación del texto del usuario (ética / lenguaje)
        is_ok, msg = moderate_content(text)
        if not is_ok:
            st.error(
                "El texto contiene lenguaje inapropiado, agresivo o discriminatorio.\n\n"
                f"Detalle: {msg}"
            )
            st.stop()

        # 3️⃣ Generación del texto
        result = improve_text(text, action)

        # 4️⃣ Moderación del texto generado (MUY IMPORTANTE)
        is_ok_out, msg_out = moderate_content(result)
        if not is_ok_out:
            st.error(
                "El contenido generado fue bloqueado por razones éticas.\n\n"
                "Intenta reformular el texto inicial."
            )
            st.stop()

        # 5️⃣ Guardar versión segura
        save_version(
            st.session_state.user_role,
            action,
            text,
            result
        )

        st.success("Resultado")
        st.write(result)

    st.divider()
    st.subheader("Historial de versiones")

    history = load_history()

    if history:
        for idx, item in enumerate(reversed(history)):
            with st.expander(f"{item['timestamp']} | {item['action']}"):
                st.markdown("**Texto original:**")
                st.write(item["original_text"])
                st.markdown("**Resultado:**")
                st.write(item["result_text"])

                if st.button("Revertir", key=f"revert_{idx}"):
                    st.session_state.pending_text = item["result_text"]
                    st.rerun()
    else:
        st.info("No hay versiones previas.")

# ================================
# GENERACIÓN DE IMÁGENES
# ================================
elif option == "Generación de imágenes":

    st.header("Generación de imágenes")

    prompt = st.text_input("Describe la imagen")

    style = st.selectbox(
        "Estilo",
        ["Realista", "Ilustración", "Minimalista", "Publicidad"]
    )

    st.session_state.image_generated = False

    is_ok, msg = moderate_content(prompt)

    if not is_ok:
        st.error(msg)
    elif st.button("Generar imagen") and not st.session_state.image_generated:
        image = generate_image(prompt, style)
        img_buffer = prepare_image_for_gallery(image)

        st.session_state.gallery.append({
            "image": img_buffer,
            "label": prompt
        })

        st.session_state.image_generated = True
        st.success("Imagen generada y agregada a la galería")

    if st.session_state.gallery:
        st.subheader("Galería")

        cols = st.columns(3)

        for idx, item in enumerate(st.session_state.gallery):
            with cols[idx % 3]:
                st.image(item["image"])
                st.caption(item["label"])
                st.download_button(
                    "Descargar",
                    data=item["image"],
                    file_name=f"bike_image_{idx+1}.png",
                    mime="image/png"
                )

        if st.button("Limpiar galería"):
            st.session_state.gallery = []
            st.session_state.image_generated = False
