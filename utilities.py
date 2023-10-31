import asyncio
import os
import discord
from discord.ext import commands
from config import config


async def try_delete(msg):
    if config.delete_confirmation:
        await asyncio.sleep(config.wait_secs)
        await msg.delete()
