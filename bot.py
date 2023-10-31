import os
import asyncio

import discord
from discord.ext import commands, tasks
from itertools import cycle
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


async def update_status():
    await bot.change_presence(activity=discord.CustomActivity(name="Eating tacos. 🌮"))


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}.")
    await update_status()


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            # print(f"{filename[:-3]} is loaded.")


async def main():
    async with bot:
        await load()
        await bot.start(os.getenv("BOT_TOKEN"))


asyncio.run(main())
