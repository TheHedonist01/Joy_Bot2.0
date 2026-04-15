import discord
from discord.ext import commands
from discord import app_commands
import aiohttp
import os
from dotenv import load_dotenv
import traceback

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BLOG_CHANNEL_ID = int(os.getenv("BLOG_CHANNEL_ID"))
print("API KEY:", TMDB_API_KEY)

GUILD_ID = 1399822549906620438  # ← PONÉ TU SERVER ID

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p/w500"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


# ─── Helpers ────────────────────────────────────────────────────────────────
async def buscar_pelicula(nombre: str):
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": nombre,
        "language": "es-AR",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                print("❌ Error TMDB:", resp.status)
                return None
            data = await resp.json()
            return data.get("results", [None])[0]


async def detalle_pelicula(movie_id: int):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "es-AR",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                print("❌ Error detalle:", resp.status)
                return None
            return await resp.json()


def formatear_duracion(minutos: int):
    if not minutos:
        return "Desconocida"
    h = minutos // 60
    m = minutos % 60
    return f"{h}h {m}m" if h else f"{m}m"


def construir_embed(pelicula):
    embed = discord.Embed(
        title=f"🎬 {pelicula.get('title')}",
        description=pelicula.get("overview", "Sin sinopsis")[:400],
        color=discord.Color.green(),
    )

    embed.add_field(name="⭐ Rating", value=str(pelicula.get("vote_average")), inline=True)
    embed.add_field(name="📅 Estreno", value=pelicula.get("release_date"), inline=True)
    embed.add_field(name="⏱️ Duración", value=formatear_duracion(pelicula.get("runtime")), inline=True)

    if pelicula.get("poster_path"):
        embed.set_image(url=f"{TMDB_IMAGE_BASE}{pelicula['poster_path']}")

    return embed


# ─── Slash Command ──────────────────────────────────────────────────────────
@bot.tree.command(
    name="pelicula",
    description="Publica una película"
)
@app_commands.describe(nombre="Nombre de la película")
async def pelicula(interaction: discord.Interaction, nombre: str):
    try:
        await interaction.response.defer(ephemeral=True)

        resultado = await buscar_pelicula(nombre)
        if not resultado:
            await interaction.followup.send("❌ No encontré la película.", ephemeral=True)
            return

        data = await detalle_pelicula(resultado["id"])
        if not data:
            await interaction.followup.send("❌ Error al obtener detalles.", ephemeral=True)
            return

        embed = construir_embed(data)

        # 🔥 fetch en vez de get (evita cache issues)
        blog_channel = await bot.fetch_channel(BLOG_CHANNEL_ID)

        if isinstance(blog_channel, discord.ForumChannel):
            await blog_channel.create_thread(
            name=data.get("title", "Película"),
            content=f"📌 {interaction.user.display_name} agregó:",
            embed=embed
            )
        else:
            await blog_channel.send(
            content=f"📌 {interaction.user.display_name} agregó:",
            embed=embed
        )

        await interaction.followup.send("✅ Publicado!", ephemeral=True)

    except Exception as e:
        print("💥 ERROR:", e)
        traceback.print_exc()

        await interaction.followup.send(
            "❌ Error interno. Mirá la consola.",
            ephemeral=True
        )


# ─── Ready ──────────────────────────────────────────────────────────────────
@bot.event
async def on_ready():
    synced = await bot.tree.sync()
    print(f"🌍 Sync global: {len(synced)} comandos")


bot.run(DISCORD_TOKEN)