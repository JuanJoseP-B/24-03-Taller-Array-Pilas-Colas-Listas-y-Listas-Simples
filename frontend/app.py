import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.hospital_manager import HospitalManager

# --- Page config ---
st.set_page_config(page_title="Sistema de Urgencias", layout="wide")

# --- Custom CSS: white background, blue buttons, no color noise ---
st.markdown(
    """
    <style>
    /* General background */
    .stApp {
        background-color: #ffffff;
    }
    /* All buttons blue */
    .stButton > button {
        background-color: #2563eb;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 0.45rem 1.2rem;
    }
    .stButton > button:hover {
        background-color: #1d4ed8;
        color: #ffffff;
    }
    /* Form submit buttons */
    .stFormSubmitButton > button {
        background-color: #2563eb;
        color: #ffffff;
        border: none;
        border-radius: 6px;
    }
    .stFormSubmitButton > button:hover {
        background-color: #1d4ed8;
        color: #ffffff;
    }
    /* Tabs styling */
    .stTabs [data-baseweb="tab"] {
        color: #1e293b;
    }
    .stTabs [aria-selected="true"] {
        border-bottom-color: #2563eb;
        color: #2563eb;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Session state ---
if "manager" not in st.session_state:
    st.session_state.manager = HospitalManager()

manager = st.session_state.manager

# --- Title ---
st.title("Sistema de Triage y Flujo de Sala de Urgencias")

# --- Tabs ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Camas UCI",
    "Sala de Espera",
    "Deshacer Acciones",
    "Directorio Medico",
    "Historial Paciente",
])

# ----- TAB 1: ICU Beds (Array) -----
with tab1:
    st.header("Camas de Cuidados Intensivos")

    beds_state = manager.get_beds_state()

    cols = st.columns(5)
    for i, bed in enumerate(beds_state):
        with cols[i % 5]:
            if bed is None:
                st.markdown(f"**Cama {i}:** Libre")
            else:
                st.markdown(f"**Cama {i}:** {bed}")

    st.divider()

    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Asignar Cama")
        with st.form("form_assign"):
            bed_index = st.number_input("Indice de cama", min_value=0, max_value=14, step=1)
            patient_name = st.text_input("Nombre del paciente")
            submitted = st.form_submit_button("Asignar")
            if submitted and patient_name:
                success, msg = manager.assign_bed(bed_index, patient_name)
                if success:
                    st.success(msg)
                else:
                    st.warning(msg)
                st.rerun()

    with col_right:
        st.subheader("Liberar Cama")
        with st.form("form_release"):
            release_index = st.number_input("Indice a liberar", min_value=0, max_value=14, step=1)
            released = st.form_submit_button("Dar de Alta")
            if released:
                success, msg = manager.release_bed(release_index)
                if success:
                    st.success(msg)
                else:
                    st.warning(msg)
                st.rerun()

# ----- TAB 2: Waiting Room (Queue) -----
with tab2:
    st.header("Sala de Espera - Nivel 4 y 5")

    col_form, col_list = st.columns([1, 2])
    with col_form:
        st.subheader("Nuevo Ingreso")
        with st.form("form_enqueue"):
            new_patient = st.text_input("Nombre del paciente")
            enqueued = st.form_submit_button("Agregar a la Cola")
            if enqueued and new_patient:
                manager.enqueue_patient(new_patient)
                st.rerun()

        st.subheader("Atender Turno")
        if st.button("Atender Siguiente"):
            success, msg = manager.dequeue_patient()
            if success:
                st.success(msg)
            else:
                st.warning(msg)
            st.rerun()

    with col_list:
        st.subheader("Cola Actual")
        waiting = manager.get_waiting_state()
        if not waiting:
            st.info("La sala de espera esta vacia.")
        else:
            for i, p in enumerate(waiting):
                st.markdown(f"**Turno {i + 1}:** {p}")

# ----- TAB 3: Undo (Stack) -----
with tab3:
    st.header("Control de Acciones - Deshacer")

    if st.button("Deshacer Ultima Accion"):
        success, msg = manager.undo_last_action()
        if success:
            st.success(msg)
        else:
            st.warning(msg)
        st.rerun()

    actions = manager.get_action_history()
    st.subheader("Historial de Acciones")
    if not actions:
        st.info("No hay acciones registradas.")
    else:
        for action in actions:
            st.markdown(f"- {action['description']}")

# ----- TAB 4: Medical Directory (List) -----
with tab4:
    st.header("Directorio de Personal Medico")

    col_doc_form, col_doc_list = st.columns(2)
    with col_doc_form:
        st.subheader("Agregar Doctor")
        with st.form("form_add_doctor"):
            doc_name = st.text_input("Nombre")
            doc_specialty = st.text_input("Especialidad")
            added = st.form_submit_button("Agregar")
            if added and doc_name and doc_specialty:
                success, msg = manager.add_doctor(doc_name, doc_specialty)
                if success:
                    st.success(msg)
                else:
                    st.warning(msg)
                st.rerun()

        st.subheader("Remover Doctor")
        with st.form("form_remove_doctor"):
            rm_name = st.text_input("Nombre exacto")
            removed = st.form_submit_button("Remover")
            if removed and rm_name:
                success, msg = manager.remove_doctor(rm_name)
                if success:
                    st.success(msg)
                else:
                    st.warning(msg)
                st.rerun()

    with col_doc_list:
        st.subheader("Doctores en Turno")
        doctors = manager.get_directory()
        if not doctors:
            st.info("No hay doctores registrados.")
        else:
            for d in doctors:
                st.markdown(f"**{d['name']}** - {d['specialty']}")

# ----- TAB 5: Patient History (Singly Linked List) -----
with tab5:
    st.header("Historial de Intervenciones")

    col_hist_form, col_hist_view = st.columns(2)
    with col_hist_form:
        with st.form("form_intervention"):
            patient_id = st.text_input("Nombre del paciente")
            procedure = st.text_input("Procedimiento (ej. Triage, Rayos X)")
            saved = st.form_submit_button("Registrar")
            if saved and patient_id and procedure:
                success, msg = manager.add_intervention(patient_id, procedure)
                st.success(msg)
                st.rerun()

    with col_hist_view:
        st.subheader("Ruta Clinica del Paciente")
        search_name = st.text_input("Buscar historial de...")
        if search_name:
            history = manager.get_patient_history(search_name)
            if not history:
                st.warning("No hay registros para este paciente.")
            else:
                sequence = " -> ".join([f"[{step}]" for step in history])
                st.info(sequence)