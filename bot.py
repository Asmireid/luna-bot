import os
import asyncio

import discord
from discord.ext import commands, tasks
from itertools import cycle
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)


async def update_status():
    await client.change_presence(activity=discord.CustomActivity(name="Eating tacos. 🌮"))


@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}.")
    await update_status()


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            # print(f"{filename[:-3]} is loaded.")


async def main():
    async with client:
        await load()
        await client.start(os.getenv("BOT_TOKEN"))


asyncio.run(main())
