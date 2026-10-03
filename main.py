import os
import discord
from discord.ext import commands
import requests
import edge_tts

TOKEN = "Aquí va tu token"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def traducir_a_espanol(texto):
    try:
        r = requests.get(f"https://api.mymemory.translated.net/get?q={requests.utils.quote(texto)}&langpair=en|es", timeout=5)
        return r.json()["responseData"]["translatedText"] if r.status_code == 200 else texto
    except Exception:
        return texto

def get_random_fact():
    try:
        r = requests.get("https://uselessfacts.jsph.pl/random.json", timeout=5)
        if r.status_code == 200:
            print(r.json())
            return traducir_a_espanol(r.json().get("text", ""))
    except Exception:
        pass
    return "No pude obtener un dato interesante en este momento."

async def text_to_audio(text, filename):
    await edge_tts.Communicate(text, "es-MX-DaliaNeural").save(filename)

@bot.command()
async def start(ctx):
    await ctx.send(f"Hola {ctx.author.name}, bienvenido al bot. Usa !fact para recibir un dato curioso.")

@bot.command()
async def fact(ctx):
    fact_text = get_random_fact()
    file = f"fact_{ctx.author.id}.mp3"
    try:
        await text_to_audio(fact_text, file)
        await ctx.send(f"**Dato curioso:** {fact_text}", file=discord.File(file))
    finally:
        if os.path.exists(file):
            os.remove(file)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

bot.run(TOKEN)
