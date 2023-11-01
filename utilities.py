import asyncio
import os
import discord
from discord.ext import commands
from config import config


async def try_delete(msg):
    if config.delete_confirmation:
        await asyncio.sleep(config.wait_secs)
        await msg.delete()


async def try_reply(ctx, msg):
    if isinstance(msg, discord.Embed):
        await ctx.reply(embed=msg, mention_author=True) if config.reply else await ctx.send(embed=msg)
        return
    await ctx.reply(msg, mention_author=True) if config.reply else await ctx.send(msg)
