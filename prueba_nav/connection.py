import streamlit as st
from pymodbus.client import ModbusTcpClient
import json
import struct
import numpy as np

# --- Para pasar de enteros a decimales --- #
def int2float(b1, b2):
    len_b1 = len(b1)
    len_b2 = len(b2)
    dif_b1 = 16 - len_b1
    dif_b2 = 16 - len_b2
    for i in range(dif_b1):
        b1 = '0' + b1
    for ii in range(dif_b2):
        b2 = '0' + b2
    return b1 + b2

def connection(medidor):
    with open("medidores/meters.json", "r") as file:
        dataMedidores = json.load(file)

    IP = dataMedidores[medidor]["IP"]
    ID = dataMedidores[medidor]["ID"]
    client = ModbusTcpClient(IP)
    try:
        if client.connect():
            # --- Indicador de conexion --- #
            print(f"Conexión exitosa con el medidor en {IP}")
            dataMedidores[medidor]["STATE"] = "ON"
            with open("medidores/meters.json", "w") as file:
                json.dump(dataMedidores, file, indent=4)
            # --- Toma de valores de los HR --- #
            activa = client.read_holding_registers(3059,2,ID)
            activa_bin1 = str(np.base_repr(activa.registers[0], base=2))
            activa_bin2 = str(np.base_repr(activa.registers[1], base=2))
            activa_bin_number = int2float(activa_bin1,activa_bin2)
            activa_f = struct.unpack('f', struct.pack('I',int(activa_bin_number, 2)))[0]

            reactiva = client.read_holding_registers(3067,2,ID)
            reactiva_bin1 = str(np.base_repr(reactiva.registers[0], base=2))
            reactiva_bin2 = str(np.base_repr(reactiva.registers[1], base=2))
            reactiva_bin_number = int2float(reactiva_bin1,reactiva_bin2)
            reactiva_f = struct.unpack('f', struct.pack('I',int(reactiva_bin_number, 2)))[0]

            aparente = client.read_holding_registers(3075,2,ID)
            aparente_bin1 = str(np.base_repr(aparente.registers[0], base=2))
            aparente_bin2 = str(np.base_repr(aparente.registers[1], base=2))
            aparente_bin_number = int2float(aparente_bin1,aparente_bin2)
            aparente_f = struct.unpack('f', struct.pack('I',int(aparente_bin_number, 2)))[0]

            corriente = client.read_holding_registers(3009,2,ID)
            corriente_bin1 = str(np.base_repr(corriente.registers[0], base=2))
            corriente_bin2 = str(np.base_repr(corriente.registers[1], base=2))
            corriente_bin_number = int2float(corriente_bin1,corriente_bin2)
            corriente_f = struct.unpack('f', struct.pack('I',int(corriente_bin_number, 2)))[0]
            
            tension = client.read_holding_registers(3035,2,ID)
            tension_bin1 = str(np.base_repr(tension.registers[0], base=2))
            tension_bin2 = str(np.base_repr(tension.registers[1], base=2))
            tension_bin_number = int2float(tension_bin1,tension_bin2)
            tension_f = struct.unpack('f', struct.pack('I',int(tension_bin_number, 2)))[0]\
            
            fdp = client.read_holding_registers(3083,2,ID)
            fdp_bin1 = str(np.base_repr(fdp.registers[0], base=2))
            fdp_bin2 = str(np.base_repr(fdp.registers[1], base=2))
            fdp_bin_number = int2float(fdp_bin1,fdp_bin2)
            fdp_f = struct.unpack('f', struct.pack('I',int(fdp_bin_number, 2)))[0]

            with open("medidores/mediciones.json", "r") as file:
                mediciones = json.load(file)
            newMediciones = {
                medidor: {
                    "Activa": activa_f,
                    "Reactiva": reactiva_f,
                    "Aparente": aparente_f,
                    "Corriente": corriente_f,
                    "Tension": tension_f,
                    "fdp": fdp_f
                }
            } 
            mediciones.update(newMediciones)
            with open("medidores/mediciones.json", "w") as file:
                json.dump(mediciones, file, indent=4)
        else:
            raise ConnectionError(f"No se pudo conectar con el medidor en {IP}")
    except Exception as e:
        # --- Indicador de conexion --- #
        dataMedidores[medidor]["STATE"] = "OFF"
        with open("medidores/meters.json", "w") as file:
            json.dump(dataMedidores, file, indent=4)
        print(f"Error al conectar con {IP}: {e}")
    finally:
        client.close()
    
# ----- Lectura de valores ----- #
corrienteHR = 3009
tensionHR = 3035
fdpHR = 3083
activaHR = 3059
reactivaHR = 3067
aparenteHR = 3075


