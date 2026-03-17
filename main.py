#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicación CLI para buscar negocios en Google Maps
Autor: Claude
"""

import argparse
import sys
import os

# Configurar UTF-8 para la salida en Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from src.google_maps_scraper import GoogleMapsScraper
from src.data_exporter import DataExporter


def parse_arguments():
    """Parse argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(
        description='Busca negocios en Google Maps y guarda la información de contacto en CSV',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py --city "Bogotá" --type "lavadero de autos" --max 50
  python main.py --city "Medellín, Colombia" --type "restaurante" --max 20
  python main.py --city "Cali" --type "panadería" --max 30 --output panaderias_cali.csv
        """
    )

    parser.add_argument(
        '--city',
        type=str,
        required=True,
        help='Ciudad o localidad donde buscar (ej: "Bogotá", "Medellín, Colombia")'
    )

    parser.add_argument(
        '--type',
        type=str,
        required=True,
        help='Tipo de negocio a buscar (ej: "lavadero de autos", "restaurante", "panadería")'
    )

    parser.add_argument(
        '--max',
        type=int,
        default=20,
        help='Número máximo de resultados a extraer (default: 20)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Nombre del archivo CSV de salida (opcional, se genera automáticamente si no se especifica)'
    )

    parser.add_argument(
        '--show-browser',
        action='store_true',
        help='Mostrar el navegador mientras se ejecuta (útil para debug)'
    )

    return parser.parse_args()


def main():
    """Función principal"""
    # Parse argumentos
    args = parse_arguments()

    # Mostrar información de búsqueda
    print("\n" + "="*70)
    print("🔍 BÚSQUEDA DE NEGOCIOS EN GOOGLE MAPS")
    print("="*70)
    print(f"📍 Ciudad: {args.city}")
    print(f"🏪 Tipo de negocio: {args.type}")
    print(f"📊 Máximo de resultados: {args.max}")
    print("="*70 + "\n")

    businesses = []

    try:
        # Crear scraper con context manager para asegurar cierre del navegador
        with GoogleMapsScraper(headless=not args.show_browser) as scraper:
            # Buscar negocios
            businesses = scraper.search_businesses(
                city=args.city,
                business_type=args.type,
                max_results=args.max
            )

        # Verificar si se encontraron resultados
        if not businesses:
            print("❌ No se encontraron negocios. Intenta con otra búsqueda.")
            return 1

        # Mostrar resumen
        DataExporter.print_summary(businesses)

        # Exportar a CSV
        print("💾 Exportando resultados a CSV...")
        filepath = DataExporter.to_csv(businesses, filename=args.output)
        print(f"✅ Datos guardados exitosamente en: {filepath}")
        print(f"📝 Total de negocios exportados: {len(businesses)}\n")

        return 0

    except KeyboardInterrupt:
        print("\n⚠ Operación cancelada por el usuario")
        return 1

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
