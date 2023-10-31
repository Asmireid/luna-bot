import os
import asyncio

import discord
from discord.ext import commands, tasks
from itertools import cycle
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
client = commands.Bot(command_prefix="!", intents=intents)

status = cycle(["song 1", "song 2", "song 3"])


@tasks.loop(seconds=7)
async def change_status():
    await client.change_presence(activity=discord.Activity(name=next(status), type=discord.ActivityType.listening))


@client.event
async def on_ready():
    print("Luna logs into Discord.")
    change_status.start()


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
