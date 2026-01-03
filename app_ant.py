import streamlit as st

from services.image_generator import generate_image
from services.text_editor import improve_text
from services.moderation import moderate_content

from utils.image_gallery import prepare_image_for_gallery
from utils.text_history import save_version, load_history
from utils.session_utils import clear_session, clear_temp_files
from auth.roles import get_permissions

# =================================================
# CONFIGURACIÓN DE LA PÁGINA
# =================================================
st.set_page_config(
    page_title="BikeCreative AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

#------------- Carga de estilos -------------
def load_css():
    with open("assets/styles.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        
load_css()

st.sidebar.markdown(
    """
    <div class="sidebar-header">
        🚴 TIENDA BIKE STORE
    </div>

    <div class="sidebar-subtitle">
        Módulo Creativo
    </div>

    <hr class="sidebar-divider">
    """,
    unsafe_allow_html=True
)
st.sidebar.title("Acceso")


# Aviso de seguridad para los usuarios:
st.info(
    "Seguridad de la información: "
    "Este aplicativo protege los textos e historiales mediante "
    "encriptación fuerte antes de almacenarlos."
)

# =================================================
# INICIALIZACIÓN DE SESSION STATE
# =================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_role" not in st.session_state:
    st.session_state.user_role = None

if "gallery" not in st.session_state:
    st.session_state.gallery = []

if "image_generated" not in st.session_state:
    st.session_state.image_generated = False

if "text_input" not in st.session_state:
    st.session_state.text_input = ""

if "last_role" not in st.session_state:
    st.session_state.last_role = None



# _____________________________
# Condiciones de seguridad y privacidad
#______________________________

with st.sidebar.expander("Seguridad y privacidad"):
    st.markdown("""
    - Los textos generados y editados se almacenan **cifrados**.
    - Se utiliza **encriptación simétrica Fernet (AES-128)**.
    - Las claves de cifrado se gestionan mediante variables de entorno.
    - El sistema no almacena datos personales del usuario.
    """)

#---------------------------------------
# Condiciones de uso ético del aplicativo
#-------------------------------------
with st.sidebar.expander("Uso ético de la IA"):
    st.markdown("""
    - Este sistema aplica moderación automática de contenido.
    - Los textos e imágenes generados deben ser revisados antes de su uso comercial.
    - La IA puede presentar sesgos; se promueve un uso responsable.
    - No se garantiza exclusividad ni derechos de autor absolutos.
    """)



# =================================================
# SIDEBAR – LOGIN / MENÚ
# =================================================

if not st.session_state.logged_in:
    role = st.sidebar.selectbox(
        "Selecciona tu rol",
        ["Diseñador", "Redactor"]
    )

    if st.sidebar.button("Ingresar"):
        st.session_state.logged_in = True
        st.session_state.user_role = role
        st.session_state.last_role = role
        st.rerun()

else:
    st.sidebar.success(f"Sesión activa: {st.session_state.user_role}")

    if st.session_state.user_role == "Redactor":
        option = st.sidebar.radio(
            "Funciones disponibles",
            ["Edición de texto", "Historial"]
        )

    elif st.session_state.user_role == "Diseñador":
        option = st.sidebar.radio(
            "Funciones disponibles",
            ["Generación de imágenes", "Galería"]
        )

    st.sidebar.divider()

    if st.sidebar.button("Salir"):
        clear_session()
        clear_temp_files()
        st.rerun()


# =================================================
# CUERPO PRINCIPAL
# =================================================
st.title("BikeCreative AI")
st.caption("IA Generativa para Marketing de Bicicletas by Freddy Sierra Silva")

if not st.session_state.logged_in:
    st.info("Por favor, inicia sesión desde el menú lateral.")
    st.stop()


# =================================================
# LIMPIEZA DE TEXTO AL VOLVER A REDACTOR
# =================================================
if st.session_state.user_role == "Redactor":
    if st.session_state.last_role != "Redactor":
        st.session_state.text_input = ""

st.session_state.last_role = st.session_state.user_role


# =================================================
# EDICIÓN DE TEXTO (REDACTOR)
# =================================================
if st.session_state.user_role == "Redactor" and option == "Edición de texto":

    st.header("Edición de contenido")

    # Texto pendiente al revertir
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

    if st.button("Procesar texto"):
        is_ok, msg = moderate_content(text)

        if not is_ok:
            st.error(msg)
        else:
            result = improve_text(text, action)
            save_version(
                st.session_state.user_role,
                action,
                text,
                result
            )
            st.success("Resultado")
            st.write(result)

    st.caption(
        "El contenido procesado se almacena de forma cifrada "
        "como parte de las medidas de seguridad del sistema."
    )


# =================================================
# HISTORIAL DE VERSIONES (REDACTOR)
# =================================================
elif st.session_state.user_role == "Redactor" and option == "Historial":

    st.header("Historial de versiones")

    history = load_history()

    if history:
        for idx, item in enumerate(reversed(history)):
            with st.expander(
                f"{item['timestamp']} | {item['action']}"
            ):
                st.markdown("**Texto original:**")
                st.write(item["original_text"])

                st.markdown("**Resultado generado:**")
                st.write(item["result_text"])

                if st.button(
                    "Revertir a esta versión",
                    key=f"revert_{idx}"
                ):
                    st.session_state.pending_text = item["result_text"]
                    st.rerun()
    else:
        st.info("No hay versiones previas registradas.")


# =================================================
# GENERACIÓN DE IMÁGENES (DISEÑADOR)
# =================================================
elif st.session_state.user_role == "Diseñador" and option == "Generación de imágenes":

    st.header("Generación de imágenes")

    prompt = st.text_input("Describe la imagen")

    style = st.selectbox(
        "Estilo",
        ["Realista", "Ilustración", "Minimalista", "Publicidad"]
    )

    # Permite nueva generación al cambiar prompt/estilo
    st.session_state.image_generated = False

    is_ok, msg = moderate_content(prompt)

    if not is_ok:
        st.error(msg)

    elif st.button("Generar imagen") and not st.session_state.image_generated:
        image = generate_image(prompt, style)

        img_buffer = prepare_image_for_gallery(image)
        st.session_state.gallery.append({
            "image": img_buffer,
            "label": prompt})

        st.session_state.image_generated = True
        st.success("Imagen generada y agregada a la galería")


# =================================================
# GALERÍA (DISEÑADOR)
# =================================================
elif st.session_state.user_role == "Diseñador" and option == "Galería":

    st.header("Galería")

    if st.session_state.gallery:
        cols = st.columns(3)

        for idx, item in enumerate(st.session_state.gallery):
            with cols[idx % 3]:
                st.image(item["image"])
                st.caption(f"📝 {item['label']}")

                st.download_button(
                    label="Descargar",
                    data=item["image"],
                    file_name=f"bike_image_{idx +1}.png",
                    mime="image/png"
                )

        if st.button("Limpiar galería"):
            st.session_state.gallery = []
            st.session_state.image_generated = False

    else:
        st.info("La galería está vacía.")

#________________________________________
# DETALLES DE SEGURIDAD Y CRIFRADO
#________________________________________

