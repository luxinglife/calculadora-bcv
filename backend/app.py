from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Permite que tu frontend en GitHub Pages pueda llamar a esta API

@app.route('/api/tasas', methods=['GET'])
def obtener_tasas():
    try:
        # Consultar la API de dolarapi.com
        response = requests.get('https://ve.dolarapi.com/v1/dolares', timeout=5)
        data = response.json()

        # Buscar tasas: oficial (BCV) y la que usaremos para USDT (paralelo)
        oficial = next((item for item in data if item['tipo'] == 'oficial'), None)
        usdt_ref = next((item for item in data if item['tipo'] == 'paralelo'), None)

        if not oficial:
            return jsonify({'error': 'No se encontró tasa oficial'}), 500

        tasa_bcv = oficial.get('promedio') or oficial.get('venta')
        tasa_usdt = usdt_ref.get('promedio') or usdt_ref.get('venta') if usdt_ref else tasa_bcv * 1.1

        return jsonify({
            'bcv': round(tasa_bcv, 2),
            'usdt': round(tasa_usdt, 2)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
