from pymodbus.client import ModbusTcpClient
import json
import struct
import numpy as np

IP = "10.36.44.20"
ID = 4

# def int2float(b1, b2):
#     bin_number = f"{b1:016b}{b2:016b}"
#     return bin_number

# client = ModbusTcpClient(IP)
# if client.connect():
#     print(f"Conexión exitosa con el medidor en {IP}")
#     result = client.read_holding_registers(3059, 2, ID)
#     bin1 = result.registers[0]
#     bin2 = result.registers[1]
#     print(bin1)
#     print(bin2)
#     bin_number = int2float(bin1,bin2)
#     print(bin_number)
#     final = struct.unpack('f', struct.pack('I',int(bin_number, 2)))[0]
#     print(final)

####################################################

# --- Para pasar de enteros a decimales --- #
def int2float(b1, b2):
    bin_number = f"{b1:016b}{b2:016b}"
    return bin_number

# def read_float(client, register, ID):
#     # result = client.read_holding_registers(register, 2, ID)
#     try:
#         result = client.read_holding_registers(register, 2, ID)
#         if isinstance(result, Exception):
#             raise result  # Si el resultado es una excepción, lánzala.
#         if result is None or not hasattr(result, 'registers') or len(result.registers) < 2:
#             raise ValueError(f"Lectura de registros inválida en la dirección {register}.")
#         bin1 = result.registers[0]
#         bin2 = result.registers[1]
#         bin_number = int2float(bin1, bin2)
#         final = struct.unpack('f', struct.pack('I',int(bin_number, 2)))[0]
#         print(bin1)
#         return final, bin_number, bin1, bin2
#     except Exception as e:
#         st.error(f"Error al leer el registro {register}: {e}")
#         return None



client = ModbusTcpClient(IP)
try:
    if client.connect():
        # --- Indicador de conexión --- #
        print(f"Conexión exitosa con el medidor en {IP}")

        # --- Toma de valores de los HR --- #
        result = client.read_holding_registers(3059, 2, ID)
        bin1 = result.registers[0]
        bin2 = result.registers[1]
        bin_number = int2float(bin1, bin2)
        final = struct.unpack('f', struct.pack('I',int(bin_number, 2)))[0]
        print(final)

except Exception as e:
    print(f"Error al conectar con {IP}: {e}")
finally:
    client.close()