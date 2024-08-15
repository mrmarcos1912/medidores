import streamlit as st
import json

st.title("Configuración de las Alarmas")

# Inicializar lista de alarmas #
if 'lista_alarmas' not in st.session_state:
    st.session_state.lista_alarmas = []
    with open("alarms/alarmas.json", "r") as file:
        savedAlarms = json.load(file)
        st.session_state.lista_alarmas = list(savedAlarms.keys())

# Inicializar lista medidores #
if 'lista_medidores' not in st.session_state:
    st.session_state.lista_medidores = []

# Show Form #
if 'show_form_add' not in st.session_state:
    st.session_state.show_form_add = False

if 'show_form_eliminate' not in st.session_state:
    st.session_state.show_form_eliminate = False

# Sidebar #
with st.sidebar:
    st.page_link("./prueba_nav.py", label= "Pagina Principal", icon="📊")
    st.page_link("./pages/config.py", label= "Configuracion", icon="⚙️")
    st.page_link("./pages/alarmas.py", label= "Alarmas", icon="🚨")

# ----------------- Alarmas ----------------- #

# Seleccion #
alarma_seleccionada = st.selectbox(label= "Seleccione una alarma:", options= st.session_state.lista_alarmas)

# Mostrar alarma seleccionada #
if alarma_seleccionada:
    col1, col2 = st.columns(2)
    col1.write(f"Nombre de la alarma:")
    col2.text(alarma_seleccionada)

    col1.write("Limites:")
    col21, col22, col23 = col2.columns([2, 1, 1])
    with open("alarms/alarmas.json", "r") as data_file:
        alarmas = json.load(data_file)
    col21.text(alarmas[alarma_seleccionada]["parametro"])
    col22.text(alarmas[alarma_seleccionada]["comparador"])
    col23.text(alarmas[alarma_seleccionada]["limite"])

st.divider()

col1, col2 = st.columns(2)

if col1.button("➕ Agregar Alarma"):
    st.session_state.show_form_add = True

# Eliminar una alarma #
if col2.button("❌ Eliminar Alarma"):
    st.session_state.show_form_eliminate = True

# Agregado #
if st.session_state.show_form_add:
    with st.form(key = "form"):
        nombre = st.text_input(label= "Ingrese el nombre: ")
        col1, col2, col3 = st.columns(3)
        medidor = st.selectbox(label="Seleccione el medidor", options= st.session_state.lista_medidores)
        parametro = col1.selectbox(label="Seleccione el parametro", options= ["Potencia Activa", "Potencia Reactiva", "Potencia Aparente"])
        comparador = col2.selectbox(label= "Comparador", options=["<", "=", ">"])
        limite = col3.number_input("Limite", min_value= 0, max_value=5000, step= 1, value= 0)
        submit = st.form_submit_button(label="Submit", )
        if submit:
            st.session_state.lista_alarmas.append(nombre)
            st.success(f"Alarma '{nombre}' agregada exitosamente!")
            # Crear nueva key con la alarma y agregarla al diccionario # 
            with open("alarms/alarmas.json", "r") as data_file:
                alarmas = json.load(data_file)
            nueva_alarma = {
                nombre: {
                    "medidor": medidor,
                    "parametro": parametro,
                    "comparador": comparador,
                    "limite": limite
                }
            }
            alarmas.update(nueva_alarma)
            with open("alarms/alarmas.json", "w") as data_file:
                json.dump(alarmas, data_file, indent= 4)
            st.session_state.show_form_add = False
            st.rerun()

if st.session_state.show_form_eliminate:
    with st.form(key= "form2"):
        alarma = st.selectbox(label= "Seleccione la alarma: ", options=st.session_state.lista_alarmas)
        submit = st.form_submit_button(label= "Submit")
        if submit:
            st.session_state.lista_alarmas.remove(alarma)
            st.success(f"Alarma '{alarma}' eliminada exitosamente!")
            st.session_state.show_form_eliminate = False
            with open("alarms/alarmas.json", "r") as data_file:
                alarmas = json.load(data_file)
            del alarmas[alarma]
            with open("alarms/alarmas.json", "w") as data_file:
                json.dump(alarmas, data_file, indent= 4)

            st.rerun()