import streamlit as st
import streamlit_authenticator as stauth
import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from connection import connection


st.set_page_config(page_title="Prueba")

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
        space, cola, space, colb, space = st.columns([0.3, 1, 0.2, 1, 0.2])
        cola.subheader(f'Dashboard "{medidor}"')
        if colb.button(label="Actualizar", use_container_width=True):
            connection(medidor)
        col1, espacio, col2, espacio, col3 = st.columns([1, 0.2, 1, 0.2, 1])
        columns = [col1, col2, col3]
        listParams = list(dataMedidores[medidor]["PARAMS"].keys())
        true_params = [param for param, value in dataMedidores[medidor]["PARAMS"].items() if value]
        for idx, element in enumerate(true_params):
            valorBool = dataMedidores[medidor]["PARAMS"][element]
            if valorBool:
                fig = go.Figure(go.Indicator(
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    value = dataMediciones[medidor][element],
                    mode = "gauge+number+delta",
                    title = {'text': element},
                    delta = {'reference': 380},
                    gauge = {'axis': {'range': [None, 500]},
                            'steps' : [
                                {'range': [0, 250], 'color': "lightgray"},
                                {'range': [250, 400], 'color': "gray"}],
                            'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 490}}))
                fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height= 200)
                columns[idx % 3].plotly_chart(fig, use_container_width=True)

    # chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["Activa", "Reactiva", "Aparente"])
    # st.line_chart(chart_data)
