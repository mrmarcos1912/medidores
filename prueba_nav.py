import streamlit as st
import streamlit_authenticator as stauth
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from connection import connection
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(page_title="Dashboard", page_icon="📊")

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
            connection(medidor)
            st.rerun()
        col1, espacio, col2, espacio, col3 = st.columns([1, 0.2, 1, 0.2, 1])
        columns = [col1, col2, col3]
        listParams = list(dataMedidores[medidor]["PARAMS"].keys())
        true_params = [param for param, value in dataMedidores[medidor]["PARAMS"].items() if value]
        for idx, element in enumerate(true_params):
            valorBool = dataMedidores[medidor]["PARAMS"][element]
            if valorBool:
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

    # chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["Activa", "Reactiva", "Aparente"])
    # st.line_chart(chart_data)
