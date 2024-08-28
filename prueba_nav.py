import streamlit as st
import streamlit_authenticator as stauth
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from connection import connection
from streamlit_extras.stylable_container import stylable_container
import sqlite3
import time
from datetime import datetime, timedelta, time

st.set_page_config(page_title="Dashboard", page_icon="📊")

# Desmarcar para que la pagina ocupe todo el ancho de la pantalla #
# with open('.streamlit/styles.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Inicializacion lista medidores #
with open("medidores/meters.json", "r") as file:
    savedMeters = json.load(file)
    st.session_state.lista_medidores = list(savedMeters.keys())

# Importacion de los json con los datos de los medidores
with open("medidores/meters.json", "r") as file:
    dataMedidores = json.load(file)
with open("medidores/mediciones.json", "r") as file:
    dataMediciones = json.load(file)

# Autenticacion #

config_json = "config_json.json"

with open(config_json) as archivo_1:
	config = json.load(archivo_1)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login(location= 'main', max_concurrent_users= None, max_login_attempts= None)

if authentication_status is False:
    st.error('El Usuario y/o la contraseña es incorrecta')
elif authentication_status is None:
    st.warning('Porfavor ingrese su Usuario y Contraseña')
elif authentication_status:

    with st.sidebar:
        st.page_link("./prueba_nav.py", label= "Pagina Principal", icon="📊")
        st.page_link("./pages/config.py", label= "Configuracion", icon="⚙️")
        st.page_link("./pages/alarmas.py", label= "Alarmas", icon="🚨")
        authenticator.logout()

# ------------- Dashboard ------------- #
    st.title("Dashboard")
    medidor = st.selectbox(label= "Seleccione uno de los medidores:", options= st.session_state.lista_medidores)
    
    #Lista parametros
    if dataMedidores:
        space, cola, space, colb, space = st.columns([0.1, 1.3, 0.1, 1, 0.2])
        cola.subheader(f'{medidor}')
        if colb.button(label="Actualizar", use_container_width=True):
            st.rerun()
        col1, espacio, col2, espacio, col3 = st.columns([1, 0.2, 1, 0.2, 1])
        columns = [col1, col2, col3]
        listParams = list(dataMedidores[medidor]["PARAMS"].keys())
        true_params = [param for param, value in dataMedidores[medidor]["PARAMS"].items() if value]
        for idx, element in enumerate(true_params):
            valorBool = dataMedidores[medidor]["PARAMS"][element]
            if valorBool:
                if element == "FactordePotencia":
                    label = "Factor de Potencia"
                else:
                    label = element
                value = round(dataMediciones[medidor][element], 2)
                delta = 10
                # columns[idx % 3].metric(label= label, value= value, delta= delta)
                with columns[idx % 3]:
                    with stylable_container(
                        key= "medicion",
                        css_styles=
                        """
                        div[data-testid="stMetric"] {
                            background-color: rgb(255 255 255 / 4%);
                            color: white;
                            border: 1px solid #d0d3d4;
                            border-radius: 10px;
                            padding: 20px 20px 20px 55px;
                            box-shadow: 1px 3px 3px #d0d3d4;
                        }
                        """
                        ):
                            st.metric(label, value, delta)

    # --- Grafica de valores --- #
    st.divider()
    # Manejo de limites temporales
    st.text("Ingrese el rango temporal para la visualizacion de valores:")
    c1, c2 = st.columns(2)
    dia1 = c1.date_input(label="Fecha inicial:")
    dia2 = c2.date_input(label="Fecha final", value=datetime.now().date() + + timedelta(days=1))
    hora1 = c1.time_input(label="Hora inicial", value= time(0,0,0))
    hora2 = c2.time_input(label="Hora final", value=time(23,59,59))
    fecha1 = datetime.combine(dia1, hora1)
    fecha2 = datetime.combine(dia2, hora2)
    # Division en tabs de los parametros
    tablas = st.tabs(listParams)
    for n in range(len(listParams)):
        parametro = listParams[n]
        with tablas[n]:
            if parametro == "FactordePotencia":
                st.header(f":blue[Factor de Potencia]")
            else:
                st.header(f":blue[{parametro}]")
            conn = sqlite3.connect("mediciones.db")
            query = f"SELECT tiempo, {parametro} AS parametro FROM mediciones WHERE medidor = '{medidor}'"
            df = pd.read_sql_query(query, conn)
            # Crear la gráfica de corriente vs tiempo
            if parametro != "FactordePotencia":
                fig = px.line(df, x='Tiempo', y='parametro', title=f'{parametro} vs Tiempo')
            else:
                fig = px.line(df, x='Tiempo', y='parametro', title=f'Factor de Potencia vs Tiempo')
            fig.update_xaxes(range=[fecha1, fecha2])

            # Mostrar la gráfica en Streamlit
            st.plotly_chart(fig)

# params = st.query_params

# # Verificar si hay un parámetro 'refresh'
# if "refresh" in params:
#     refresh_time = 10
# else:
#     refresh_time = 10  # Valor por defecto

# # Mostrar la hora actual
# st.write(f"Tiempo actual: {time.strftime('%H:%M:%S')}")

# # Refrescar la página cada 10 segundos
# st.query_params["refresh"] = str(refresh_time)
# time.sleep(refresh_time)
# st.rerun()