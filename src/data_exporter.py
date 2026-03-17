"""
Data Exporter para guardar información de negocios en archivos CSV
"""

import pandas as pd
import os
from datetime import datetime
from typing import List, Dict


class DataExporter:
    """Clase para exportar datos de negocios a diferentes formatos"""

    @staticmethod
    def to_csv(data: List[Dict[str, str]], filename: str = None, directory: str = "data") -> str:
        """
        Exporta datos de negocios a un archivo CSV

        Args:
            data: Lista de diccionarios con información de negocios
            filename: Nombre del archivo (si es None, se genera automáticamente)
            directory: Directorio donde guardar el archivo

        Returns:
            Ruta completa del archivo generado
        """
        if not data:
            raise ValueError("No hay datos para exportar")

        # Crear directorio si no existe
        os.makedirs(directory, exist_ok=True)

        # Generar nombre de archivo si no se proporciona
        if filename is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"negocios_{timestamp}.csv"

        # Asegurar que termine en .csv
        if not filename.endswith('.csv'):
            filename += '.csv'

        # Ruta completa
        filepath = os.path.join(directory, filename)

        # Crear DataFrame
        df = pd.DataFrame(data)

        # Reordenar columnas en un orden lógico
        column_order = ['nombre', 'telefono', 'direccion', 'website', 'google_maps_url']
        # Mantener solo las columnas que existen
        available_columns = [col for col in column_order if col in df.columns]
        # Agregar columnas adicionales que no estén en el orden predefinido
        remaining_columns = [col for col in df.columns if col not in available_columns]
        df = df[available_columns + remaining_columns]

        # Guardar a CSV con codificación UTF-8 (para caracteres especiales como ñ, tildes)
        df.to_csv(filepath, index=False, encoding='utf-8-sig')  # utf-8-sig para Excel

        return filepath

    @staticmethod
    def print_summary(data: List[Dict[str, str]]):
        """
        Imprime un resumen de los datos extraídos

        Args:
            data: Lista de diccionarios con información de negocios
        """
        if not data:
            print("No hay datos para mostrar")
            return

        print("\n" + "="*60)
        print(f"📊 RESUMEN DE RESULTADOS")
        print("="*60)
        print(f"Total de negocios encontrados: {len(data)}")

        # Contar cuántos tienen cada tipo de información
        with_phone = sum(1 for b in data if b.get('telefono') and b['telefono'] != 'N/A')
        with_address = sum(1 for b in data if b.get('direccion') and b['direccion'] != 'N/A')
        with_website = sum(1 for b in data if b.get('website') and b['website'] != 'N/A')

        print(f"Con teléfono: {with_phone} ({with_phone/len(data)*100:.1f}%)")
        print(f"Con dirección: {with_address} ({with_address/len(data)*100:.1f}%)")
        print(f"Con sitio web: {with_website} ({with_website/len(data)*100:.1f}%)")
        print("="*60 + "\n")
