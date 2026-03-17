# -*- coding: utf-8 -*-
"""
Aplicación Web Flask para búsqueda de negocios en Google Maps
"""

import sys
import io

# Configurar UTF-8 para la salida en Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from flask import Flask, render_template, request, jsonify, send_file
from src.google_maps_scraper import GoogleMapsScraper
from src.data_exporter import DataExporter
import os
import glob
import pandas as pd
from datetime import datetime
import threading

app = Flask(__name__)

# Variable global para almacenar el estado de la búsqueda
search_status = {
    'running': False,
    'current': 0,
    'total': 0,
    'message': ''
}

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Endpoint para iniciar búsqueda de negocios"""
    global search_status

    if search_status['running']:
        return jsonify({'error': 'Ya hay una búsqueda en progreso'}), 400

    # Obtener parámetros del formulario
    city = request.form.get('city')
    business_type = request.form.get('type')
    max_results = int(request.form.get('max', 20))

    if not city or not business_type:
        return jsonify({'error': 'Ciudad y tipo de negocio son requeridos'}), 400

    # Iniciar búsqueda en un thread separado
    thread = threading.Thread(
        target=run_search,
        args=(city, business_type, max_results)
    )
    thread.start()

    return jsonify({
        'message': 'Búsqueda iniciada',
        'city': city,
        'type': business_type,
        'max': max_results
    })

def run_search(city, business_type, max_results):
    """Ejecuta la búsqueda en background"""
    global search_status

    search_status['running'] = True
    search_status['current'] = 0
    search_status['total'] = max_results
    search_status['message'] = 'Iniciando búsqueda...'

    try:
        with GoogleMapsScraper(headless=True) as scraper:
            search_status['message'] = 'Navegando a Google Maps...'
            businesses = scraper.search_businesses(city, business_type, max_results)

        if businesses:
            # Guardar a CSV
            search_status['message'] = 'Guardando resultados...'
            filepath = DataExporter.to_csv(businesses)
            search_status['message'] = f'Completado: {len(businesses)} negocios encontrados'
        else:
            search_status['message'] = 'No se encontraron resultados'

    except Exception as e:
        search_status['message'] = f'Error: {str(e)}'
    finally:
        search_status['running'] = False

@app.route('/status')
def status():
    """Obtener estado de la búsqueda actual"""
    return jsonify(search_status)

@app.route('/results')
def results():
    """Mostrar últimos resultados"""
    # Buscar el archivo CSV más reciente
    csv_files = glob.glob('data/*.csv')

    if not csv_files:
        return render_template('results.html', businesses=[], error='No hay resultados disponibles')

    latest_file = max(csv_files, key=os.path.getctime)

    try:
        # Leer CSV y reemplazar NaN con 'N/A'
        df = pd.read_csv(latest_file, encoding='utf-8-sig')
        df = df.fillna('N/A')  # Reemplazar valores vacíos con 'N/A'
        businesses = df.to_dict('records')

        # Limpiar y validar datos
        for business in businesses:
            for key in business:
                # Convertir todo a string y limpiar
                if not isinstance(business[key], str):
                    business[key] = str(business[key]) if business[key] != 'N/A' else 'N/A'
                business[key] = business[key].strip() if business[key] != 'N/A' else 'N/A'

        # Información adicional
        stats = {
            'total': len(businesses),
            'with_phone': sum(1 for b in businesses if b.get('telefono') and b['telefono'] != 'N/A'),
            'with_address': sum(1 for b in businesses if b.get('direccion') and b['direccion'] != 'N/A'),
            'with_website': sum(1 for b in businesses if b.get('website') and b['website'] != 'N/A'),
            'filename': os.path.basename(latest_file)
        }

        return render_template('results.html', businesses=businesses, stats=stats, error=None)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return render_template('results.html', businesses=[], error=f'Error al cargar resultados: {str(e)}')

@app.route('/download/<filename>')
def download(filename):
    """Descargar archivo CSV"""
    filepath = os.path.join('data', filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return 'Archivo no encontrado', 404

@app.route('/history')
def history():
    """Listar todos los archivos CSV generados"""
    csv_files = glob.glob('data/*.csv')

    files_info = []
    for filepath in csv_files:
        df = pd.read_csv(filepath, encoding='utf-8-sig')
        files_info.append({
            'filename': os.path.basename(filepath),
            'count': len(df),
            'date': datetime.fromtimestamp(os.path.getctime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
        })

    # Ordenar por fecha (más reciente primero)
    files_info.sort(key=lambda x: x['date'], reverse=True)

    return jsonify(files_info)

if __name__ == '__main__':
    # Crear directorio data si no existe
    os.makedirs('data', exist_ok=True)

    print("\n" + "="*70)
    print("🌐 SERVIDOR WEB - BÚSQUEDA DE NEGOCIOS EN GOOGLE MAPS")
    print("="*70)
    print("📍 Abre tu navegador en: http://localhost:5000")
    print("⌨  Presiona Ctrl+C para detener el servidor")
    print("="*70 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
