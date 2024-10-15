# app.py
from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
# Cargar las variables del archivo .env
load_dotenv()

app = Flask(__name__)

# Ruta que actúa como intermediaria
@app.route('/get_curp_data', methods=['GET'])
def get_curp_data():

    curp = request.args.get('curp')  # Obtenemos la CURP desde los parámetros


 # Obtener el token Bearer desde los encabezados de la solicitud
    bearer_token = request.headers.get('Authorization')

    # Si el token no está en los encabezados, intentamos obtenerlo como parámetro
    if not bearer_token:
        bearer_token = request.args.get('token')

    if not bearer_token:
        return jsonify({"error": "Token de autorización no proporcionado"}), 401

    # Definir la URL de la API de Semovioaxaca
    url = os.getenv('API_URL')

    # Encabezados (incluye el token de autorización y el tipo de contenido)
    headers = {
        "Authorization": bearer_token,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*"
        }

    # El cuerpo de la solicitud (payload) se envía como parámetros de la solicitud GET
    payload = {'curp': curp}

    try:
        # Hacemos la solicitud GET a la API externa con el token Bearer y el parámetro CURP
        response = requests.get(url, headers=headers, data=payload)

        # Verificamos si la solicitud fue exitosa
        if response.status_code == 200:
            return jsonify(response.json())  # Devolvemos la respuesta en formato JSON
        else:
            return jsonify({"error": "Error en la solicitud", "status_code": response.status_code, "response": response.text}), response.status_code

    except requests.exceptions.RequestException as e:
        # Capturamos errores en caso de que la solicitud falle
        return jsonify({"error": str(e)})

# Aseguramos que la aplicación corra en modo debug
if __name__ == '__main__':
    app.run(debug=True)
