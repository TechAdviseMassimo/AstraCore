import discord
from discord.ext import commands
import json
import os
import asyncio
import wavelink

# ---------------------------------------------------------
# INTENTS
# ---------------------------------------------------------
intents = discord.Intents.default()
intents.members = True
intents.message_content = False  # Non serve più per pannelli ruoli moderni

bot = commands.Bot(command_prefix="!", intents=intents)


# ---------------------------------------------------------
# CARICA SOLO I COGS NECESSARI
# ---------------------------------------------------------
async def load_cogs():
    cogs_to_load = [
        "cogs.music",
        "cogs.welcome",
        "cogs.role_panel"
    ]

    for cog in cogs_to_load:
        await bot.load_extension(cog)
        print(f"Caricato cog: {cog}")


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

        print("Lavalink connesso tramite Wavelink!")


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
