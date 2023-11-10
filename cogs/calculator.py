import os
import numexpr
import re
from discord.ext import commands
from numpy import *
from utilities import *


class Calc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command(aliases=['calc'],
                      help="makes calculations of input: " +
                           f"{Config().command_prefix}calculator / " +
                           f"{Config().command_prefix}calc example_expression")
    async def calculator(self, ctx, *, expression):
        try:
            answer = numexpr.evaluate(expression)

            msg_embed = make_embed(ctx,
                                   title=f"{Config().bot_name}'s Calculator",
                                   descr=f"{expression} = {answer}")
            await try_reply(ctx, msg_embed)
        except:
            await try_reply(ctx, f"'{expression}' is not a valid expression...")


async def setup(bot):
    await bot.add_cog(Calc(bot))
