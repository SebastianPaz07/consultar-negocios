# 🚀 Guía de Deployment - Consultar Negocios

Esta aplicación puede desplegarse en varios servicios de hosting gratuitos para que puedas acceder desde cualquier computador con internet.

## 🌐 Opciones de Hosting Gratuito

### 1️⃣ Render.com (Recomendado - Más Fácil)

**Ventajas:**
- ✅ Completamente gratis
- ✅ Soporte nativo para Playwright
- ✅ Configuración automática con render.yaml
- ✅ SSL/HTTPS incluido
- ✅ No requiere tarjeta de crédito

**Pasos:**

1. **Crear cuenta en Render:**
   - Ve a: https://render.com
   - Registrate gratis

2. **Conectar GitHub:**
   - Click en "New +" → "Web Service"
   - Conecta tu cuenta de GitHub
   - Selecciona el repositorio `consultar-negocios`

3. **Configuración automática:**
   - Render detectará automáticamente el `render.yaml`
   - Click en "Apply"
   - Espera 5-10 minutos mientras se instala Playwright

4. **¡Listo!**
   - Tu app estará en: `https://consultar-negocios.onrender.com`
   - Puedes cambiar el nombre en la configuración

**Nota:** El servicio gratuito se "duerme" después de 15 minutos de inactividad, y tarda ~30 segundos en despertar.

---

### 2️⃣ Railway.app

**Ventajas:**
- ✅ $5 USD de crédito gratis al mes
- ✅ Muy rápido
- ✅ No se duerme
- ✅ Fácil de usar

**Pasos:**

1. **Crear cuenta:**
   - Ve a: https://railway.app
   - Registrate con GitHub

2. **Nuevo proyecto:**
   - Click en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Elige `consultar-negocios`

3. **Configurar variables:**
   - Ve a Settings → Variables
   - Agrega:
     ```
     DEBUG=False
     ```

4. **Configurar build:**
   - En Settings → Build
   - Custom Build Command:
     ```bash
     pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium
     ```
   - Start Command:
     ```bash
     gunicorn app:app
     ```

5. **Generar dominio:**
   - Ve a Settings → Networking
   - Click en "Generate Domain"

---

### 3️⃣ PythonAnywhere (Alternativa)

**Ventajas:**
- ✅ Gratis permanente
- ✅ Buen para aprender
- ✅ Soporte de Python

**Desventajas:**
- ⚠️ Configuración más manual
- ⚠️ Playwright puede tener problemas

**Pasos:**

1. **Crear cuenta:**
   - Ve a: https://www.pythonanywhere.com
   - Registrate gratis

2. **Clonar repositorio:**
   - Ve a "Consoles" → "Bash"
   - Ejecuta:
     ```bash
     git clone https://github.com/SebastianPaz07/consultar-negocios.git
     cd consultar-negocios
     pip install -r requirements.txt --user
     ```

3. **Configurar Web App:**
   - Ve a "Web" → "Add a new web app"
   - Selecciona "Manual configuration" → Python 3.10
   - En "Code" → Source code: `/home/tuusuario/consultar-negocios`
   - En "WSGI configuration file", edita y pega:
     ```python
     import sys
     path = '/home/tuusuario/consultar-negocios'
     if path not in sys.path:
         sys.path.append(path)

     from app import app as application
     ```

4. **Reload:**
   - Click en "Reload" en la web app
   - Tu app estará en: `https://tuusuario.pythonanywhere.com`

---

## 🔧 Configuración Post-Deployment

### Verificar que funciona:

1. **Abre tu URL** (ejemplo: https://consultar-negocios.onrender.com)
2. **Haz una búsqueda de prueba:**
   - Ciudad: "Bogotá"
   - Tipo: "restaurante"
   - Máximo: 5

3. **Espera el resultado** (puede tardar 1-2 minutos en la primera búsqueda)

### Solución de Problemas:

**❌ Error: "Application Error"**
- Revisa los logs en el dashboard de Render/Railway
- Verifica que Playwright se instaló correctamente
- Puede necesitar más RAM (usa plan de pago o reduce max_results)

**❌ Búsqueda muy lenta**
- Es normal en servicios gratuitos
- El scraping toma tiempo (~5 segundos por negocio)
- Reduce el número máximo de resultados

**❌ "Service Unavailable"**
- El servicio se durmió (Render free tier)
- Espera 30 segundos y recarga
- La primera carga después de dormir es lenta

---

## 🌍 Acceso desde Cualquier Computador

Una vez desplegado:

1. **Guarda la URL** de tu aplicación
2. **Compártela** con quien quieras
3. **Accede desde cualquier lugar:**
   - Móvil
   - Tablet
   - Otra computadora
   - Cualquier navegador

**Ejemplo de URL:**
```
https://consultar-negocios.onrender.com
```

---

## 💾 Almacenamiento de Datos

Los archivos CSV generados se guardan en el servidor:
- ✅ Persistentes entre búsquedas
- ✅ Accesibles desde el historial
- ✅ Descargables directamente

**Nota:** En servicios gratuitos, los archivos pueden perderse si el servidor se reinicia. Para almacenamiento permanente, considera usar:
- Amazon S3
- Google Cloud Storage
- Cloudinary

---

## 🔐 Seguridad

**Recomendaciones:**
- No compartas información sensible en búsquedas
- Los datos son visibles para quien tenga la URL
- Para aplicaciones privadas, agrega autenticación

---

## 📊 Monitoreo

**Render:**
- Dashboard → Logs (ver actividad en tiempo real)
- Metrics (ver uso de recursos)

**Railway:**
- Dashboard → Deployments → Ver logs
- Observability (métricas)

---

## 🆘 Soporte

Si tienes problemas:

1. **Revisa los logs** en el dashboard del servicio
2. **Verifica el README.md** del proyecto
3. **Abre un issue** en GitHub: https://github.com/SebastianPaz07/consultar-negocios/issues

---

## 🎉 ¡Listo!

Tu aplicación está ahora en la nube y accesible desde cualquier computador con internet. Solo necesitas compartir la URL.
