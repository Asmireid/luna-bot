import asyncio
import os

import discord
from discord.ext import commands

from config.config import Config

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=Config().command_prefix.split(' '), intents=intents)


# bot.remove_command('help')


async def update():
    for guild in bot.guilds:
        server = bot.get_guild(guild.id)
        bot_member = server.get_member(bot.user.id)
        await bot_member.edit(nick=Config().bot_name)

    activity = Config().bot_activity
    await bot.change_presence(activity=discord.CustomActivity(name=activity))


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}.")
    await update()


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load()
        await bot.start(Config().bot_token)


asyncio.run(main())
