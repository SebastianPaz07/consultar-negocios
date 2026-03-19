# 🚀 Guía de Despliegue en Render

## ✅ Archivos ya configurados:

- ✅ `requirements.txt` - Con todas las dependencias (Flask, Playwright, openpyxl, etc.)
- ✅ `runtime.txt` - Python 3.11.0
- ✅ `render.yaml` - Configuración completa de Render
- ✅ `Procfile` - Comando de inicio con Gunicorn
- ✅ `.gitignore` - Archivos excluidos del repositorio

---

## 📋 Configuración en la Interfaz de Render

Cuando estés en la página de configuración inicial de Render, configura lo siguiente:

### 1. **Nombre del Servicio**
```
consultar-negocios
```
(O el nombre que prefieras)

### 2. **Región**
```
Oregon (US West)
```
(Gratis y rápido)

### 3. **Branch**
```
master
```
(O `main` si ese es tu branch principal)

### 4. **Root Directory**
```
(dejar en blanco)
```

### 5. **Environment**
```
Python 3
```

### 6. **Build Command**
```
pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium
```

**⚠️ IMPORTANTE:** Este comando puede tardar 5-10 minutos en el primer deploy porque instala Chromium.

### 7. **Start Command**
```
gunicorn app:app --bind 0.0.0.0:$PORT
```

### 8. **Plan**
```
Free
```

### 9. **Variables de Entorno**

Agregar las siguientes variables (Add Environment Variable):

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `DEBUG` | `False` |

---

## ⚙️ Configuración Avanzada (Opcional pero Recomendada)

### **Disco Persistente para guardar archivos CSV/Excel:**

En la sección "Disks":
1. Click en "Add Disk"
2. Configurar:
   - **Name:** `data`
   - **Mount Path:** `/opt/render/project/src/data`
   - **Size:** `1 GB`

Esto permite que los archivos generados persistan entre deployments.

---

## 🔄 Pasos para Desplegar

### Paso 1: Commit y Push de los cambios recientes
```bash
git add .
git commit -m "Agregar soporte para Excel y mejoras en UI"
git push origin master
```

### Paso 2: En Render Dashboard
1. Selecciona tu repositorio (ya lo hiciste)
2. Configura todos los campos arriba mencionados
3. Click en **"Create Web Service"**

### Paso 3: Esperar el Deploy
- El build tomará entre 5-10 minutos (primera vez)
- Verás logs en tiempo real
- Cuando veas "Starting service..." significa que ya casi está listo

### Paso 4: Acceder a tu App
- Render te dará una URL como: `https://consultar-negocios.onrender.com`
- Copia esa URL y ábrela en tu navegador

---

## ⚠️ Limitaciones del Plan Free de Render

1. **Inactividad:** Si no recibe tráfico por 15 minutos, el servicio se "duerme"
   - Al acceder nuevamente, tardará ~30 segundos en despertar

2. **Horas mensuales:** 750 horas gratis al mes (suficiente para uso personal)

3. **Performance:** Playwright puede ser lento en el plan free
   - Las búsquedas tardarán más que en local
   - Límite de 100 negocios por búsqueda recomendado

---

## 🐛 Solución de Problemas

### Error: "Failed to install Chromium"
**Solución:** Verifica que el Build Command incluya:
```
playwright install-deps chromium
```

### Error: "Port already in use"
**Solución:** El Start Command debe ser:
```
gunicorn app:app --bind 0.0.0.0:$PORT
```
(La variable `$PORT` la asigna Render automáticamente)

### Error: "Module not found"
**Solución:** Verifica que `requirements.txt` tenga todas las dependencias:
```
playwright>=1.40.0
pandas>=2.0.0
flask>=3.0.0
gunicorn>=21.0.0
openpyxl>=3.1.0
```

### Los archivos CSV/Excel no persisten
**Solución:** Configura un disco persistente (ver sección "Configuración Avanzada")

---

## ✅ Verificación Post-Deploy

Una vez desplegado, prueba:

1. ✅ Acceder a la URL de Render
2. ✅ Hacer una búsqueda de prueba (máximo 10 negocios)
3. ✅ Verificar que se muestren los resultados
4. ✅ Hacer clic en una card → debe abrir la modal
5. ✅ Descargar Excel → debe funcionar
6. ✅ Marcar como contactado → debe persistir

---

## 🔐 Seguridad

El plan free de Render incluye:
- ✅ HTTPS automático
- ✅ SSL certificates
- ✅ DDoS protection básico

No necesitas configurar nada adicional.

---

## 📊 Monitoreo

En el Dashboard de Render puedes ver:
- Logs en tiempo real
- Uso de CPU y memoria
- Requests por minuto
- Tiempo de actividad

---

## 🚀 Siguientes Pasos Después del Deploy

1. **Personaliza el dominio** (opcional):
   - Render te permite usar tu propio dominio
   - Configuración en: Settings → Custom Domain

2. **Upgrade a plan pago** (si necesitas):
   - Más RAM (512 MB → 2 GB)
   - Sin "sleep" por inactividad
   - Builds más rápidos

3. **Configurar Auto-Deploy**:
   - Ya está activo por defecto
   - Cada push a master despliega automáticamente

---

## 📝 Notas Finales

- **Primera carga:** 30-60 segundos (plan free)
- **Búsquedas:** 2-3x más lentas que local
- **Archivos:** Usar disco persistente para no perderlos
- **Logs:** Siempre revisa los logs si algo falla

¿Listo para desplegar? Sigue los pasos y avísame si encuentras algún error! 🚀
