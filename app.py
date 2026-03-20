# -*- coding: utf-8 -*-
"""
Aplicación Web Flask para búsqueda de negocios en Google Maps
"""

import sys
import io
import logging

# Configurar UTF-8 para la salida en Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Configurar logging detallado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

from flask import Flask, render_template, request, jsonify, send_file
from src.google_maps_scraper import GoogleMapsScraper
from src.data_exporter import DataExporter
from src.message_strategies import get_message_for_business, personalize_message
import os
import glob
import pandas as pd
from datetime import datetime
import threading

app = Flask(__name__)

# Crear directorio data si no existe
os.makedirs('data', exist_ok=True)
logger.info(f"✅ Directorio 'data' verificado/creado en: {os.path.abspath('data')}")

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
        logger.warning("⚠️  Intento de búsqueda rechazado: ya hay una búsqueda en progreso")
        return jsonify({'error': 'Ya hay una búsqueda en progreso'}), 400

    # Obtener parámetros del formulario
    city = request.form.get('city')
    business_type = request.form.get('type')
    max_results = int(request.form.get('max', 20))

    logger.info(f"🔍 Nueva búsqueda solicitada: {business_type} en {city} (max: {max_results})")

    if not city or not business_type:
        logger.error("❌ Parámetros inválidos: ciudad o tipo de negocio faltante")
        return jsonify({'error': 'Ciudad y tipo de negocio son requeridos'}), 400

    # Iniciar búsqueda en un thread separado
    thread = threading.Thread(
        target=run_search,
        args=(city, business_type, max_results),
        name=f"SearchThread-{city}-{business_type}"
    )
    thread.start()
    logger.info(f"🚀 Thread de búsqueda iniciado: {thread.name}")

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

    logger.info(f"📊 Estado inicial: running={search_status['running']}, total={max_results}")

    try:
        logger.info("🌐 Iniciando GoogleMapsScraper (headless=True)...")
        with GoogleMapsScraper(headless=True) as scraper:
            logger.info("✅ GoogleMapsScraper inicializado correctamente")
            search_status['message'] = 'Navegando a Google Maps...'
            logger.info(f"🗺️  Buscando negocios: {business_type} en {city}")

            businesses = scraper.search_businesses(city, business_type, max_results)
            logger.info(f"✅ Búsqueda completada: {len(businesses)} negocios encontrados")

        if businesses:
            # Guardar a CSV
            search_status['message'] = 'Guardando resultados...'
            logger.info("💾 Guardando resultados en CSV...")
            filepath = DataExporter.to_csv(businesses)
            logger.info(f"✅ Archivo CSV guardado: {filepath}")
            search_status['message'] = f'Completado: {len(businesses)} negocios encontrados'
        else:
            logger.warning("⚠️  No se encontraron resultados")
            search_status['message'] = 'No se encontraron resultados'

    except Exception as e:
        logger.error(f"❌ Error durante la búsqueda: {str(e)}", exc_info=True)
        search_status['message'] = f'Error: {str(e)}'
    finally:
        search_status['running'] = False
        logger.info(f"🏁 Búsqueda finalizada. Estado final: running={search_status['running']}")

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

        # Asignar estrategia de mensaje a cada negocio
        for idx, business in enumerate(businesses):
            strategy = get_message_for_business(idx)
            personalized = personalize_message(strategy, business.get('nombre', 'N/A'))
            business['message_strategy'] = personalized
            business['business_index'] = idx

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

@app.route('/download-excel')
def download_excel():
    """Generar y descargar archivo Excel con mensajes y estrategias"""
    # Buscar el archivo CSV más reciente
    csv_files = glob.glob('data/*.csv')

    if not csv_files:
        return 'No hay resultados disponibles', 404

    latest_file = max(csv_files, key=os.path.getctime)

    try:
        # Leer CSV y reemplazar NaN con 'N/A'
        df = pd.read_csv(latest_file, encoding='utf-8-sig')
        df = df.fillna('N/A')
        businesses = df.to_dict('records')

        # Limpiar y validar datos
        for business in businesses:
            for key in business:
                if not isinstance(business[key], str):
                    business[key] = str(business[key]) if business[key] != 'N/A' else 'N/A'
                business[key] = business[key].strip() if business[key] != 'N/A' else 'N/A'

        # Asignar estrategia de mensaje a cada negocio
        for idx, business in enumerate(businesses):
            strategy = get_message_for_business(idx)
            personalized = personalize_message(strategy, business.get('nombre', 'N/A'))
            business['message_strategy'] = personalized
            business['business_index'] = idx

        # Generar Excel
        excel_filepath = DataExporter.to_excel(businesses)

        return send_file(excel_filepath, as_attachment=True, download_name=os.path.basename(excel_filepath))
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f'Error al generar Excel: {str(e)}', 500

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

    # Detectar si estamos en desarrollo o producción
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True') == 'True'

    # Información de diagnóstico de Playwright
    logger.info("="*70)
    logger.info("🚀 INICIANDO SERVIDOR - BÚSQUEDA DE NEGOCIOS EN GOOGLE MAPS")
    logger.info("="*70)
    logger.info(f"🐍 Python: {sys.version}")
    logger.info(f"🌐 Puerto: {port}")
    logger.info(f"🔧 Debug: {debug}")
    logger.info(f"📁 Directorio de trabajo: {os.getcwd()}")
    logger.info(f"💾 Directorio data: {os.path.abspath('data')}")

    # Verificar Playwright
    try:
        from playwright.sync_api import sync_playwright
        logger.info("✅ Playwright importado correctamente")
        try:
            with sync_playwright() as p:
                chromium_path = p.chromium.executable_path
                logger.info(f"✅ Chromium encontrado en: {chromium_path}")
        except Exception as e:
            logger.error(f"❌ Error al verificar Chromium: {str(e)}")
    except Exception as e:
        logger.error(f"❌ Error al importar Playwright: {str(e)}")

    # Verificar variables de entorno relacionadas con Playwright
    playwright_env_vars = ['PLAYWRIGHT_BROWSERS_PATH', 'PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH']
    for var in playwright_env_vars:
        value = os.environ.get(var)
        if value:
            logger.info(f"🔑 {var} = {value}")
        else:
            logger.info(f"🔑 {var} = (no configurada)")

    logger.info("="*70)

    if debug:
        print("\n" + "="*70)
        print("🌐 SERVIDOR WEB - BÚSQUEDA DE NEGOCIOS EN GOOGLE MAPS")
        print("="*70)
        print("📍 Abre tu navegador en: http://localhost:5000")
        print("⌨  Presiona Ctrl+C para detener el servidor")
        print("="*70 + "\n")

    app.run(debug=debug, host='0.0.0.0', port=port)
