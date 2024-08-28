import bcrypt

# Contraseña en texto plano
password = "admin"

# Generación del hash
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Mostrar el hash generado
print(hashed_password)