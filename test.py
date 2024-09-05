# ---- Prueba para filtrar valores dentro de la DB entre dos fechas ---- #
import sqlite3
import streamlit as st
from datetime import time
from datetime import datetime

# Input de las fechas limites
c01, c02 = st.columns(2)
diaInicial = datetime.combine(c01.date_input(label="Día Inicial:", key="diainicial"), time(9, 54, 0))
diaFinal = datetime.combine(c02.date_input(label="Día Final:", key="diafinal"), time(9, 55, 0))
ingresar = st.button(label="Ingresar", key="ingresar_btn", use_container_width=True)

if ingresar:
    conn = sqlite3.connect("mediciones.db")
    cursor = conn.cursor()
    
    query = """
    SELECT 
        (SELECT Tiempo FROM mediciones WHERE Corriente = (SELECT MAX(Corriente) FROM mediciones WHERE Tiempo BETWEEN ? AND ?) AND Tiempo BETWEEN ? AND ?) AS tiempo_corriente,
        (SELECT MAX(Corriente) FROM mediciones WHERE Tiempo BETWEEN ? AND ?) AS max_corriente,
        (SELECT Tiempo FROM mediciones WHERE Tension = (SELECT MAX(Tension) FROM mediciones WHERE Tiempo BETWEEN ? AND ?) AND Tiempo BETWEEN ? AND ?) AS tiempo_tension,
        (SELECT MAX(Tension) FROM mediciones WHERE Tiempo BETWEEN ? AND ?) AS max_tension,
        (SELECT Tiempo FROM mediciones WHERE Activa = (SELECT MAX(Activa) FROM mediciones WHERE Tiempo BETWEEN ? AND ?) AND Tiempo BETWEEN ? AND ?) AS tiempo_activa,
        (SELECT MAX(Activa) FROM mediciones WHERE Tiempo BETWEEN ? AND ?) AS max_activa,
        (SELECT Tiempo FROM mediciones WHERE Reactiva = (SELECT MAX(Reactiva) FROM mediciones WHERE Tiempo BETWEEN ? AND ?) AND Tiempo BETWEEN ? AND ?) AS tiempo_reactiva,
        (SELECT MAX(Reactiva) FROM mediciones WHERE Tiempo BETWEEN ? AND ?) AS max_reactiva,
        (SELECT Tiempo FROM mediciones WHERE Aparente = (SELECT MAX(Aparente) FROM mediciones WHERE Tiempo BETWEEN ? AND ?) AND Tiempo BETWEEN ? AND ?) AS tiempo_aparente,
        (SELECT MAX(Aparente) FROM mediciones WHERE Tiempo BETWEEN ? AND ?) AS max_aparente,
        (SELECT Tiempo FROM mediciones WHERE FactordePotencia = (SELECT MAX(FactordePotencia) FROM mediciones WHERE Tiempo BETWEEN ? AND ?) AND Tiempo BETWEEN ? AND ?) AS tiempo_fdp,
        (SELECT MAX(FactordePotencia) FROM mediciones WHERE Tiempo BETWEEN ? AND ?) AS max_fdp
    """
    
    cursor.execute(query, (diaInicial, diaFinal, diaInicial, diaFinal,
                        diaInicial, diaFinal,
                        diaInicial, diaFinal, diaInicial, diaFinal,
                        diaInicial, diaFinal,
                        diaInicial, diaFinal, diaInicial, diaFinal,
                        diaInicial, diaFinal,
                        diaInicial, diaFinal, diaInicial, diaFinal,
                        diaInicial, diaFinal,
                        diaInicial, diaFinal, diaInicial, diaFinal,
                        diaInicial, diaFinal))
    
    result = cursor.fetchone()
    conn.close()
    
    st.write(f"Corriente máxima: {result[1]} a las {result[0]}")
    st.write(f"Tensión máxima: {result[3]} a las {result[2]}")
    st.write(f"Activa máxima: {result[5]} a las {result[4]}")
    st.write(f"Reactiva máxima: {result[7]} a las {result[6]}")
    st.write(f"Aparente máxima: {result[9]} a las {result[8]}")
    st.write(f"Factor de potencia máximo: {result[11]} a las {result[10]}")