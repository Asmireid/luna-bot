import os
import random
import re

import discord
from discord.ext import commands


class Dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command(aliases=["dice", "d"])
    async def roll(self, ctx, *, cmd: str):
        parts = re.split(r"[d+]+", cmd)
        try:
            count, sides, offset = {
                1: lambda parts: (1, int(parts[0]), 0),  # "x"
                2: lambda parts: (int(parts[0]), int(parts[1]), 0),  # "xdy"
                3: lambda parts: (int(parts[0]), int(parts[1]), int(parts[2]))  # "xdy+z"
            }[len(parts)](parts)
        except ValueError:
            await ctx.send(f"'{cmd}' is not a valid input for my dice.")
            return

        rolls = [random.randint(1, sides) for _ in range(count)]

        msg_embed = discord.Embed(title=f"Dice for {count}d{sides}+{offset}")
        msg_embed.description = '\n'.join((f"#{i+1}: **{roll}**" for i, roll in enumerate(rolls)))
        msg_embed.add_field(name='sum', value=f'total = {sum(rolls)} + {offset} = {sum(rolls)+offset}', inline=True)

        await ctx.send(embed=msg_embed)


async def setup(bot):
    await bot.add_cog(Dice(bot))
