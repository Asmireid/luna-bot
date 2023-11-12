import os
import time
from discord.ext import commands

from utilities import *


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command(help=f"returns the current latency of the bot: {Config().command_prefix}ping")
    async def ping(self, ctx):
        try:
            latency = round(self.bot.latency * 1000)
            msg_embed = make_embed(ctx,
                                   title=f"{Config().bot_name}'s Clock",
                                   descr=f"Current latency is {latency} ms.")
            await try_reply(ctx, msg_embed)
        except Exception as e:
            print(f"An error occurred: {e}")

    @commands.command(help=f"returns the server's current time: {Config().command_prefix}time")
    async def server_time(self, ctx):
        try:
            server_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            msg_embed = make_embed(ctx,
                                   title=f"{Config().bot_name}'s Clock",
                                   descr=f"Server's current time is {server_time}.")
            await try_reply(ctx, msg_embed)
        except Exception as e:
            print(f"An error occurred: {e}")

    @commands.command(help=f"returns the current time of user: {Config().command_prefix}time")
    async def time(self, ctx):
        try:
            user_time = ctx.message.created_at.strftime("%Y-%m-%d %H:%M:%S")
            msg_embed = make_embed(ctx,
                                   title=f"{Config().bot_name}'s Clock",
                                   descr=f"Current GMT time is {user_time}.")
            await try_reply(ctx, msg_embed)
        except Exception as e:
            print(f"An error occurred: {e}")


async def setup(bot):
    await bot.add_cog(Ping(bot))
