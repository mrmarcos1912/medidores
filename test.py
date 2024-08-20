from telegram import Bot
import requests

bot_token = "7088137376:AAHpQWzrkpr-FOEySK_ydr4Oqunw1BAXw0w"

# Obtencion del chat ID #
respuesta = requests.get(f"https://api.telegram.org/bot{bot_token}/getUpdates")
print(respuesta.json())
chat_id = respuesta.json()["result"][0]["message"]["chat"]["id"]

mensaje = "¡Hola, este es un mensaje enviado desde Python!"

url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={mensaje}"
response = requests.get(url)