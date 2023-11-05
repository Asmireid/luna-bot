import asyncio
import os
import discord
from discord.ext import commands
from config import config


async def try_delete_invocation(msg):
    if config.delete_invocation:
        await msg.delete()


async def try_delete_confirmation(msg):
    if config.delete_confirmation:
        await asyncio.sleep(config.wait_time)
        await msg.delete()


async def try_reply(ctx, msg):
    await try_delete_invocation(ctx.message)
    if isinstance(msg, discord.Embed):
        return await ctx.reply(embed=msg,
                               mention_author=config.mention_author,
                               ephemeral=config.ephemeral) if config.reply else await ctx.send(embed=msg)
    return await ctx.reply(msg,
                           mention_author=config.mention_author,
                           ephemeral=config.ephemeral) if config.reply else await ctx.send(msg)


async def try_display_confirmation(ctx, msg):
    if config.display_confirmation:
        conf = await try_reply(ctx, msg)
        await try_delete_confirmation(conf)


def make_embed(ctx, title, descr, color=discord.Color.dark_embed()) -> discord.Embed:
    msg_embed = discord.Embed(title=title,
                              description=descr,
                              color=color)
    msg_embed.set_author(name=f"Requested by {ctx.author.nick or ctx.author.name}",
                         icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
    msg_embed.set_footer(text=config.embed_footer)

    return msg_embed
