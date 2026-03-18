# ⚠️ ADVERTENCIA IMPORTANTE: Vercel NO es Compatible

## 🚨 Problemas Críticos con Vercel

Esta aplicación **NO funcionará correctamente en Vercel** por las siguientes razones:

### 1. ❌ Playwright NO funciona en Vercel
- **Problema:** Playwright necesita instalar Chromium (~170MB)
- **Realidad:** Vercel no permite instalar navegadores en su entorno serverless
- **Resultado:** El scraping fallará completamente

### 2. ⏱️ Límites de Tiempo Muy Cortos
- **Plan Free:** 10 segundos máximo por request
- **Plan Pro:** 60 segundos máximo
- **Nuestra app:** Necesita 2-5 minutos para buscar 20 negocios
- **Resultado:** Timeout antes de completar la búsqueda

### 3. 🔄 Arquitectura Serverless
- **Vercel:** Diseñado para funciones rápidas sin estado
- **Nuestra app:** Necesita mantener estado durante la búsqueda
- **Resultado:** No puede guardar progreso o archivos CSV

### 4. 💾 Almacenamiento Efímero
- **Vercel:** Los archivos se borran después de cada ejecución
- **Nuestra app:** Guarda CSVs en el servidor
- **Resultado:** Pérdida de todos los archivos generados

---

## ✅ Plataformas Recomendadas

### **Opción 1: Render.com** (Mejor para esta app)
✅ Soporte completo para Playwright
✅ Sin límites de tiempo
✅ Almacenamiento persistente
✅ Completamente gratis
✅ Configuración incluida (`render.yaml`)

**[Ver guía completa en DEPLOYMENT.md](DEPLOYMENT.md#1️⃣-rendercom-recomendado---más-fácil)**

### **Opción 2: Railway.app**
✅ Soporta Playwright
✅ Muy rápido
✅ $5 USD gratis/mes
✅ No se duerme

**[Ver guía en DEPLOYMENT.md](DEPLOYMENT.md#2️⃣-railwayapp)**

### **Opción 3: Fly.io**
✅ Soporta Docker y Playwright
✅ Gratis para proyectos pequeños
✅ Buena performance

---

## 🔧 ¿Qué Hacer Ahora?

### Si ya desplegaste en Vercel:

1. **Elimina el deployment de Vercel:**
   - Ve a tu dashboard de Vercel
   - Selecciona el proyecto
   - Settings → Delete Project

2. **Despliega en Render.com:**
   ```bash
   # El código ya está listo en GitHub
   # Solo necesitas:
   1. Ir a https://render.com
   2. Conectar tu repositorio
   3. Render detectará automáticamente render.yaml
   4. Esperar 5-10 minutos
   ```

3. **Tu app funcionará perfectamente:**
   - URL: `https://tu-app.onrender.com`
   - Sin límites de tiempo
   - Scraping completo
   - Archivos CSV guardados

---

## 📊 Comparación

| Característica | Vercel ❌ | Render ✅ | Railway ✅ |
|---------------|----------|----------|-----------|
| Playwright | No | Sí | Sí |
| Tiempo límite | 10-60 seg | Sin límite | Sin límite |
| Costo | Gratis | Gratis | $5/mes gratis |
| Web Scraping | ❌ No funciona | ✅ Perfecto | ✅ Perfecto |
| Nuestra App | ❌ Incompatible | ✅ Compatible | ✅ Compatible |

---

## 💡 ¿Por qué el error 404 en Vercel?

El error 404 que ves es porque:
1. Vercel no puede instalar Playwright
2. La aplicación falla al iniciar
3. Las rutas no se registran correctamente
4. Vercel devuelve 404 por defecto

**Aunque arreglemos el 404, el scraping NO funcionará.**

---

## 🎯 Solución Rápida (5 minutos)

### Desplegar en Render:

1. **Ve a:** https://render.com
2. **Regístrate** con GitHub
3. **New +** → **Web Service**
4. **Selecciona:** `consultar-negocios` de tu GitHub
5. **Apply** (Render detecta `render.yaml` automáticamente)
6. **Espera 10 minutos** mientras instala todo
7. **¡Listo!** Tu app funciona perfectamente

---

## 📞 Soporte

Si tienes dudas sobre el deployment:
1. Lee [DEPLOYMENT.md](DEPLOYMENT.md) (guía completa)
2. Mira los logs en Render para ver el progreso
3. Abre un issue en GitHub si algo falla

---

## ✨ Resumen

```
❌ Vercel = NO funciona (serverless, sin Playwright)
✅ Render = Funciona perfectamente (gratis, con Playwright)
✅ Railway = Funciona perfectamente ($5 crédito/mes)

Recomendación: Usa Render.com
```

Tu código está perfecto, solo necesita la plataforma correcta. 🚀
