# 🔍 Búsqueda de Clientes - Google Maps Scraper

Aplicación con **interfaz web** y **CLI** para buscar negocios en Google Maps y extraer su información de contacto automáticamente.

## 📋 Características

- ✅ **Interfaz Web Moderna** - Navegador intuitivo con diseño responsive
- ✅ **Visualización en Tiempo Real** - Progreso de búsqueda en vivo
- ✅ **Búsqueda automática** de negocios en Google Maps
- ✅ **Extracción de información de contacto**:
  - Nombre del negocio
  - Número de teléfono
  - Dirección
  - Sitio web
  - URL de Google Maps
- ✅ **Exportación a CSV** compatible con Excel
- ✅ **Historial de búsquedas** con descarga directa
- ✅ **Sin necesidad de API keys o cuentas**
- ✅ **Completamente GRATIS**

## 🚀 Requisitos Previos

- Python 3.8 o superior
- Conexión a Internet
- Sistema operativo: Windows, macOS o Linux

## 📦 Instalación

### 1. Clonar o descargar este proyecto

```bash
cd "Busqueda de clientes app"
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Instalar navegadores de Playwright (solo primera vez)

```bash
playwright install chromium
```

Este comando descarga el navegador Chromium necesario para el web scraping.

## 💻 Uso

Puedes usar esta aplicación de dos formas:

### 🌐 Opción 1: Interfaz Web (Recomendado)

**Iniciar el servidor web:**

```bash
python app.py
```

Luego abre tu navegador en: **http://localhost:5000**

**Características de la interfaz web:**
- 📝 Formulario intuitivo para nueva búsqueda
- ⏳ Progreso en tiempo real con barra de carga
- 📊 Estadísticas visuales de resultados
- 🗂️ Visualización en tarjetas de cada negocio
- 🔍 Búsqueda/filtrado de negocios en resultados
- 📥 Descarga directa de archivos CSV
- 📜 Historial completo de búsquedas anteriores
- 📱 Diseño responsive (funciona en móviles)

**Pasos para buscar:**
1. Ingresa la ciudad (ej: "Bogotá")
2. Ingresa el tipo de negocio (ej: "lavadero de autos")
3. Selecciona máximo de resultados (1-100)
4. Click en "Iniciar Búsqueda"
5. Observa el progreso en tiempo real
6. Automáticamente se mostrará la página de resultados
7. Filtra, visualiza o descarga los datos

### ⌨️ Opción 2: Línea de Comandos (CLI)

**Comando básico:**

```bash
python main.py --city "CIUDAD" --type "TIPO_DE_NEGOCIO" --max NÚMERO
```

### Ejemplos

#### Buscar 50 lavaderos de autos en Bogotá

```bash
python main.py --city "Bogotá" --type "lavadero de autos" --max 50
```

#### Buscar 30 restaurantes en Medellín

```bash
python main.py --city "Medellín, Colombia" --type "restaurante" --max 30
```

#### Buscar 20 panaderías en Cali con nombre de archivo personalizado

```bash
python main.py --city "Cali" --type "panadería" --max 20 --output panaderias_cali.csv
```

### Parámetros

| Parámetro | Descripción | Requerido | Default |
|-----------|-------------|-----------|---------|
| `--city` | Ciudad o localidad donde buscar | ✅ Sí | - |
| `--type` | Tipo de negocio a buscar | ✅ Sí | - |
| `--max` | Número máximo de resultados | ❌ No | 20 |
| `--output` | Nombre del archivo CSV de salida | ❌ No | Auto-generado |
| `--show-browser` | Mostrar navegador durante ejecución | ❌ No | false |

## 📊 Salida

### Archivo CSV

Los datos se guardan en la carpeta `data/` con el formato:

```
data/negocios_2026-03-17_14-30-45.csv
```

### Estructura del CSV

| nombre | telefono | direccion | website | google_maps_url |
|--------|----------|-----------|---------|-----------------|
| Lavadero Auto Spa | +57 1 234 5678 | Calle 123 #45-67, Bogotá | www.autospa.com | https://maps.google.com/... |

El archivo CSV:
- Está codificado en UTF-8 (soporta tildes, ñ, etc.)
- Es compatible con Excel, Google Sheets y otras herramientas
- Campos vacíos ("N/A") cuando la información no está disponible

## ⚙️ Cómo Funciona

1. **Navegación**: Abre Google Maps automáticamente usando Playwright
2. **Búsqueda**: Busca el tipo de negocio en la ciudad especificada
3. **Scroll**: Hace scroll para cargar más resultados
4. **Extracción**: Visita cada negocio y extrae:
   - Información visible en el panel de detalles
   - Datos de contacto disponibles públicamente
5. **Exportación**: Guarda todo en un archivo CSV

## ⏱️ Rendimiento

- **Velocidad**: ~2-5 segundos por negocio
- **Tiempo estimado**:
  - 20 negocios: ~1-2 minutos
  - 50 negocios: ~3-5 minutos
  - 100 negocios: ~7-10 minutos

## ⚠️ Limitaciones

1. **Velocidad**: El web scraping es más lento que una API oficial
2. **Disponibilidad de datos**: No todos los negocios tienen toda la información
3. **Estructura HTML**: Si Google cambia su interfaz, puede requerir actualizaciones
4. **Límite práctico**: Recomendado máximo 100-200 negocios por búsqueda

## 🔧 Solución de Problemas

### Error: "playwright: command not found"

```bash
# Reinstalar playwright
pip install playwright
playwright install chromium
```

### Error: "No se encontraron resultados"

- Verifica la ortografía de la ciudad y tipo de negocio
- Prueba con nombres más generales (ej: "lavadero" en vez de "lavadero de autos premium")
- Asegúrate de tener conexión a Internet

### Error: "Timeout" o "Page crashed"

- Verifica tu conexión a Internet
- Reduce el número de resultados (--max 20)
- Cierra otros programas que usen mucha memoria

### El navegador se abre pero no se cierra

```bash
# Usar Ctrl+C para cancelar
# El navegador se cerrará automáticamente
```

## 📝 Notas Importantes

### Uso Responsable

- No realizar búsquedas masivas (miles de negocios) de forma frecuente
- Respetar los términos de servicio de Google
- Usar delays entre requests (ya implementado automáticamente)

### Datos Personales

- Esta herramienta solo extrae información pública disponible en Google Maps
- Los datos son proporcionados por los dueños de los negocios
- Usa la información de forma responsable y legal

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje de programación
- **Playwright**: Automatización de navegador
- **Pandas**: Manejo y exportación de datos

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso personal y educativo.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si encuentras bugs o tienes sugerencias:

1. Reporta el issue
2. Propone mejoras
3. Comparte tus casos de uso

## 📞 Soporte

Si tienes problemas:

1. Revisa la sección de "Solución de Problemas"
2. Verifica que tienes la última versión de las dependencias
3. Asegúrate de haber instalado Playwright correctamente

---

**Hecho con ❤️ para facilitar la búsqueda de clientes en Colombia**
