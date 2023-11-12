import os
import numexpr
from discord.ext import commands
from numpy import *
from utilities import *


class Calc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command(aliases=['calc', 'math'],
                      help="makes calculations of input: " +
                           f"{Config().command_prefix}calculator / " +
                           f"{Config().command_prefix}calc / " +
                           f"{Config().command_prefix}math example_expression")
    async def calculator(self, ctx, *, expression):
        try:
            answer = numexpr.evaluate(expression)

            msg_embed = make_embed(ctx,
                                   title=f"{Config().bot_name}'s Calculator",
                                   descr=f"{expression} = {answer}")
            await try_reply(ctx, msg_embed)
        except:
            await try_reply(ctx, f"'{expression}' is not a valid expression...")

    @commands.command(help="represents input integer in different representations: " +
                           f"{Config().command_prefix}convert example_num")
    async def represent(self, ctx, num):
        try:
            if '0b' in num:
                int_num = int(num[2:], 2)
            elif '0o' in num:
                int_num = int(num[2:], 8)
            elif '0x' in num:
                int_num = int(num[2:], 16)
            else:
                int_num = int(num)

            bin_num = bin(int_num)
            oct_num = oct(int_num)
            hex_num = hex(int_num)

            msg_embed = make_embed(ctx,
                                   title=f"{Config().bot_name}'s Calculator",
                                   descr=f"{int_num} = {bin_num} = {oct_num} = {hex_num}")
            await try_reply(ctx, msg_embed)
        except:
            await try_reply(ctx, f"'{num}' is not a valid representation of integer...")


async def setup(bot):
    await bot.add_cog(Calc(bot))
