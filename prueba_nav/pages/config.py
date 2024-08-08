import streamlit as st
import json
from connection import connection

st.set_page_config(page_title="Config", page_icon="⚙️")
st.title("Configuracion de medidores")

# Cargar los medidores al session_state si no están cargados

st.session_state.lista_medidores = []
with open("medidores/meters.json", "r") as file:
    savedMeters = json.load(file)
    st.session_state.lista_medidores = list(savedMeters.keys())
    print(st.session_state.lista_medidores)

if 'form_agregar_medidor' not in st.session_state:
    st.session_state.form_agregar_medidor = False

#Cargado del estado de los parametros
if 'params' not in st.session_state:
    st.session_state.params = {}
    with open("medidores/meters.json", "r") as file:
        medidores = json.load(file)
        for nombre, datos in medidores.items():
            st.session_state.params[nombre] = datos.get("PARAMS", {
                "Activa": False,
                "Reactiva": False,
                "Aparente": False,
                "Corriente": False,
                "Tension": False,
                "Factor de Potencia": False
            })

# Funciones para agregar y eliminar medidores
def add_to_list(agregar, ip, id):
    st.session_state.lista_medidores.append(agregar)
    try:
        with open("medidores/meters.json", "r") as data_file:
            medidores = json.load(data_file)
    except (FileNotFoundError, json.JSONDecodeError):
        medidores = {}
    try:
        with open("medidores/mediciones.json", "r") as file:
            mediciones = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        mediciones = {}
    nuevo_medidor = {
        agregar: {
            "STATE": "ON",
            "IP": ip,
            "ID": id,
            "PARAMS": {
                "Activa": False,
                "Reactiva": False,
                "Aparente": False,
                "Corriente": False,
                "Tension": False,
                "Factor de Potencia": False
            }
        }
    }
    medidores.update(nuevo_medidor)
    nuevos_parametros = {
        agregar: {
            "Activa": 0,
            "Reactiva": 0,
            "Aparente": 0,
            "Corriente": 0,
            "Tension": 0,
            "Factor de Potencia": 0
        }
    }
    mediciones.update(nuevos_parametros)
    with open("medidores/meters.json", "w") as data_file:
        json.dump(medidores, data_file, indent=4)
    with open("medidores/mediciones.json", "w") as file:
        json.dump(mediciones, file, indent=4)
    st.success(f"Medidor {agregar} agregado exitosamente!")
    st.session_state.form_agregar_medidor = False
    st.session_state.params[agregar] = {
        "Activa": False,
        "Reactiva": False,
        "Aparente": False,
        "Corriente": False,
        "Tension": False,
        "Factor de Potencia": False
    }
    connection(agregar)
    st.rerun()


def delete_from_list(eliminar):
    st.session_state.lista_medidores.remove(eliminar)
    try:
        with open("medidores/meters.json", "r") as data_file:
            medidores = json.load(data_file)
        del medidores[eliminar]
        with open("medidores/meters.json", "w") as data_file:
            json.dump(medidores, data_file, indent=4)
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        st.error("Error al eliminar el medidor. No se encontró el archivo o el medidor.")
        st.write("Error:", str(e))
    st.success(f"Medidor {eliminar} eliminado exitosamente!")
    st.rerun()

# Inputs de los medidores a agregar o eliminar
col1, col2 = st.columns(2)
with col1:
    agregar = st.text_input("Ingrese el nombre del medidor a agregar:")
    if st.button("Agregar medidor"):
        st.session_state.form_agregar_medidor = True

with col2:
    eliminar = st.selectbox("Seleccione el medidor que desea eliminar:", options=st.session_state.lista_medidores)
    if st.button("Eliminar medidor"):
        delete_from_list(eliminar)

# Formulario para agregar medidor
if st.session_state.form_agregar_medidor:
    st.subheader(f"Ingrese los datos del medidor:")
    with st.form(key="form"):
        col1, col2 = st.columns(2)
        ip = col1.text_input(label="Ingrese la direccion del equipo.")
        id = col2.text_input(label="Ingrese el ID", key="id")
        submit = st.form_submit_button(label="Submit")
        if submit:
            add_to_list(agregar, ip, id)

# Mostrar los medidores configurados en tabs
if st.session_state.lista_medidores:
    st.divider()
    tablas = st.tabs(st.session_state.lista_medidores)
    for n in range(len(st.session_state.lista_medidores)):
        nombre = st.session_state.lista_medidores[n]
        tablas[n].header(f"Medidor {nombre}")
        col1, col2 = tablas[n].columns(2)
        col1.text("Estado: ")
        col1.text("Direccion IP del equipo: ")
        col1.text("ID del equipo: ")
        with open("medidores/meters.json", "r") as data_file:
            medidores = json.load(data_file)
        if medidores[nombre]["STATE"] == "ON":
            col2.markdown(":green[Conectado]")
        else:
            col2.markdown(":red[Desconectado]")
        col2.text(medidores[nombre]["IP"])
        col2.text(medidores[nombre]["ID"])
        # Parametros de interes para mostrar en el dashboard
        potAct = col1.toggle(label= "Potencia Activa", key=f"potAct_{n}", value=st.session_state.params[nombre]["Activa"])
        potReact = col1.toggle(label= "Potencia Reactiva", key=f"potReact_{n}", value=st.session_state.params[nombre]["Reactiva"])
        potApt = col1.toggle(label= "Potencia Aparente", key=f"potApt_{n}", value=st.session_state.params[nombre]["Aparente"])
        corrientes = col2.toggle(label= "Corrientes", key=f"corrientes_{n}", value=st.session_state.params[nombre]["Corriente"])
        tensiones = col2.toggle(label= "Tensiones", key=f"tensiones_{n}", value=st.session_state.params[nombre]["Tension"])
        fdp = col2.toggle(label= "Factor de Potencia", key=f"fdp_{n}", value=st.session_state.params[nombre]["Factor de Potencia"])
        if tablas[n].button(label="Save", key=f"btn_{n}", use_container_width=True):
            medidores[nombre]["PARAMS"] = {
                "Activa": potAct,
                "Reactiva": potReact,
                "Aparente": potApt,
                "Corriente": corrientes,
                "Tension": tensiones,
                "Factor de Potencia": fdp
            }
            st.session_state.params[nombre] = {
                "Activa": potAct,
                "Reactiva": potReact,
                "Aparente": potApt,
                "Corriente": corrientes,
                "Tension": tensiones,
                "Factor de Potencia": fdp
            }
            with open("medidores/meters.json", "w") as file:
                    json.dump(medidores, file, indent=4)
        if tablas[n].button(label="Reconnect", key=f"reconnect_{n}",use_container_width=True):
            connection(nombre)

# Sidebar
with st.sidebar:
    st.page_link("./prueba_nav.py", label="Pagina Principal", icon="📊")
    st.page_link("./pages/config.py", label="Configuracion", icon="⚙️")
    st.page_link("./pages/alarmas.py", label="Alarmas", icon="🚨")
