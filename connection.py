import streamlit as st
from pymodbus.client import ModbusTcpClient
import json
import struct
import numpy as np
import time

# --- Para pasar de enteros a decimales --- #
def int2float(b1, b2):
    bin_number = f"{b1:016b}{b2:016b}"
    return bin_number

def read_float(client, register, ID):
    try:
        result = client.read_holding_registers(register, 2, ID)
        if isinstance(result, Exception):
            raise result
        if result is None or not hasattr(result, 'registers') or len(result.registers) < 2:
            raise ValueError(f"Lectura de registros inválida en la dirección {register}.")
        bin1 = result.registers[0]
        bin2 = result.registers[1]
        bin_number = int2float(bin1, bin2)
        final = struct.unpack('f', struct.pack('I',int(bin_number, 2)))[0]
        return final
    except Exception as e:
        st.error(f"Error al leer el registro {register}: {e}")
        return None

def connection(medidor):
    with open("medidores/meters.json", "r") as file:
        dataMedidores = json.load(file)

    IP = dataMedidores[medidor]["IP"]
    ID = int(dataMedidores[medidor]["ID"])
    client = ModbusTcpClient(IP, timeout = 2)
    try:
        if client.connect():
            # --- Indicador de conexión --- #
            dataMedidores[medidor]["STATE"] = "ON"
            with open("medidores/meters.json", "w") as file:
                json.dump(dataMedidores, file, indent=4)

            # --- Toma de valores de los HR --- #
            activa_f = read_float(client, 3059, ID)
            reactiva_f = read_float(client, 3067, ID)
            aparente_f = read_float(client, 3075, ID)
            corriente_f = read_float(client, 3009, ID)
            tension_f = read_float(client, 3035, ID)
            fdp_f = read_float(client, 3083, ID)

            # --- Guardado de resultados --- #
            if None not in (activa_f, reactiva_f, aparente_f, corriente_f, tension_f, fdp_f):
                with open("medidores/mediciones.json", "r") as file:
                    mediciones = json.load(file)
                newMediciones = {
                    medidor: {
                        "Activa": activa_f,
                        "Reactiva": reactiva_f,
                        "Aparente": aparente_f,
                        "Corriente": corriente_f,
                        "Tension": tension_f,
                        "Factor de Potencia": fdp_f
                    }
                }
                mediciones.update(newMediciones)
                with open("medidores/mediciones.json", "w") as file:
                    json.dump(mediciones, file, indent=4)
        else:
            raise ConnectionError(f"No se pudo conectar con el medidor en {IP}")
    except Exception as e:
        # --- Indicador de conexión fallida --- #
        dataMedidores[medidor]["STATE"] = "OFF"
        with open("medidores/meters.json", "w") as file:
            json.dump(dataMedidores, file, indent=4)
        with open("medidores/mediciones.json", "r") as file:
            mediciones = json.load(file)
        anular_parametros = {
            medidor: {
                "Activa": 0,
                "Reactiva": 0,
                "Aparente": 0,
                "Corriente": 0,
                "Tension": 0,
                "Factor de Potencia": 0
            }
        }
        mediciones.update(anular_parametros)
        with open("medidores/mediciones.json", "w") as file:
            json.dump(mediciones, file, indent=4)
        print(f"Error al conectar con {IP}: {e}")
    finally:
        client.close()







