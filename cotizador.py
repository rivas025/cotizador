###'6150990168:AAGTj2Aolk4VbRwUECJP5oRhn9Bit4mf7NQ'
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from reportlab.pdfgen import canvas
from flask import Flask, request

# Autenticar y autorizar el acceso del cliente
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/Hogar/cotizador/cotizadordeseguuros-c0d0d88a2383.json", scope)
client = gspread.authorize(creds)

# Abrir la hoja de cálculo y seleccionar la hoja llamada "Datos"
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1poc9IgO2a4F9eYSD949P1HNgGjo6oljmL20DF_XUrBI")
worksheet = spreadsheet.worksheet("Datos")

# Obtener los valores de las celdas
edad_titular = int(worksheet.acell('D3').value)
edad_conyugue = int(worksheet.acell('D7').value)
edad_hijo_1 = int(worksheet.acell('D9').value)
edad_hijo_2 = int(worksheet.acell('D11').value)
edad_hijo_3 = int(worksheet.acell('D13').value)
edad_hijo_4 = int(worksheet.acell('D15').value)

# Crear el objeto PDF
pdf_filename = "PRECIOS.pdf"
c = canvas.Canvas(pdf_filename)
c.setFont("Helvetica", 12)

# Agregar las filas a partir de la segunda fila en la hoja de cálculo
values = worksheet.get_all_values()
for row in values[1:]:
    producto = row[0]
    precio = row[1]
    c.drawString(40, c._y, producto)
    c.drawString(100, c._y, precio)
    c.showPage()

# Guardar el archivo PDF
c.save()

# Enviar el archivo PDF al usuario a través de Telegram utilizando Dialogflow
from google.protobuf.json_format import MessageToJson
import requests
import json

def enviar_documento(chat_id, pdf_filename):
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendDocument"
    files = {'document': open(pdf_filename, 'rb')}
    data = {
        'chat_id': chat_id
    }
    response = requests.post(url, files=files, data=data)
    return response.json()

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    chat_id = req['originalDetectIntentRequest']['payload']['chat']['id']
    enviar_documento(chat_id, pdf_filename)
    return '', 200

if __name__ == '__main__':
    app.run(debug=True)
