import discord
from discord.ext import commands
from utils.db import init_db
import json
import os
import asyncio
import wavelink

intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Utile per debug e pannelli

bot = commands.Bot(command_prefix="!", intents=intents)


# ---------------------------------------------------------
# CARICA I COGS
# ---------------------------------------------------------
async def load_cogs():
    # Carica tutti i cogs nella cartella /cogs
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Caricato cog: {filename}")

    # Carica il listener dei ruoli
    await bot.load_extension("listeners.role_listener")
    print("Caricato listener: role_listener")


# ---------------------------------------------------------
# EVENTO ON_READY
# ---------------------------------------------------------
@bot.event
async def on_ready():
    print(f"AstraCore è online come {bot.user}")
    await bot.tree.sync()

    # Connessione a Lavalink
    if not getattr(bot, "wavelink_ready", False):
        bot.wavelink_ready = True

        node = wavelink.Node(
            uri="http://127.0.0.1:2333",
            password="astracore"
        )

        await wavelink.Pool.connect(
            client=bot,
            nodes=[node]
        )

        print("Lavalink 4 connesso tramite Wavelink 3!")


# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
with open("config.json") as f:
    config = json.load(f)


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
async def main():
    async with bot:
        await load_cogs()
        await bot.start(config["TOKEN"])


asyncio.run(main())
