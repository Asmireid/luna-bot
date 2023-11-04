import os
import asyncio

import discord
from discord.ext import commands
from config import config
from cogs import set_config

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config.command_prefix, intents=intents)


async def update_status():
    status = set_config.get_status()
    await bot.change_presence(activity=discord.CustomActivity(name=status))


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}.")
    await update_status()


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load()
        await bot.start(config.bot_token)


asyncio.run(main())
