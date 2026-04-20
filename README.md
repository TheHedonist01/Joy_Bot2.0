# 🎬 Discord Movie Bot

Bot de Discord que publica información de películas en un canal de Foro de Discord usando la API de TMDB.

## Comando disponible

```
/pelicula <nombre>
```
Busca la película en TMDB y publica un embed con:
- 🖼️ Póster oficial
- 📝 Sinopsis
- ⭐ Calificación TMDB
- 📅 Fecha de estreno
- ⏱️ Duración
- 🎭 Géneros

---

## Setup paso a paso

### 1. Clonar / descargar el proyecto

Copiá los archivos en una carpeta y abrí una terminal ahí.

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar las variables de entorno

Copiá `.env.example` como `.env`:

```bash
cp .env.example .env
```

Luego editá `.env` con tus datos reales:

```
DISCORD_TOKEN=...
TMDB_API_KEY=...
BLOG_CHANNEL_ID=...
```

#### Cómo obtener cada valor:

**DISCORD_TOKEN**
1. Entrá a https://discord.com/developers/applications
2. Creá una nueva aplicación → sección "Bot"
3. Hacé clic en "Reset Token" y copiá el token
4. En la sección "Bot" activá los intents: `Message Content Intent`

**TMDB_API_KEY**
1. Registrate en https://www.themoviedb.org
2. Andá a https://www.themoviedb.org/settings/api
3. Solicitá una API Key (tipo "Developer", es gratis e inmediato)

**BLOG_CHANNEL_ID**
1. En Discord: Ajustes → Avanzado → activá **Modo desarrollador**
2. Clic derecho en el canal de blog → **Copiar ID del canal**

### 4. Invitar el bot al servidor

En Discord Developer Portal → OAuth2 → URL Generator:
- Scopes: `bot`, `applications.commands`
- Permisos: `Send Messages`, `Embed Links`, `View Channels`

Copiá la URL generada y abrila en el navegador para invitar el bot.

### 5. Ejecutar el bot

```bash
python bot.py
```

Deberías ver en consola:
```
🌍 Sync global: 1 comandos
```

---

## Uso

En cualquier canal del servidor donde el bot tenga acceso:

```
/pelicula Inception
/pelicula El Padrino
/pelicula Interstellar 2014
```

El bot responde de forma silenciosa (solo vos ves la confirmación) y publica el embed en el canal de blog configurado.

---

## Notas

- Los resultados se obtienen en **español (es-AR)** si TMDB tiene la traducción disponible.
- El color del embed varía según el rating: 🟢 ≥7.5 · 🟡 ≥5.5 · 🔴 <5.5
- Si hay múltiples películas con el mismo nombre, se toma el resultado más relevante de TMDB.
