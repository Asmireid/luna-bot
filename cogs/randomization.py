import random
import re

from utilities import *
from config import config


class Randomization(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command(aliases=['8ball', 'eightball'])
    async def magic_eightball(self, ctx, *, question):
        with open("cogs/magic8ball_responses.txt", "r") as f:
            responses = f.readlines()
            response = random.choice(responses)

            msg_embed = discord.Embed(title=f"{config.bot_name}'s Magic 8 Ball",
                                      description=question,
                                      color=discord.Color.dark_embed())

            msg_embed.set_author(name=f"Requested by {ctx.author.nick}", icon_url=ctx.author.avatar)
            msg_embed.set_thumbnail(url="https://static.thenounproject.com/png/371802-200.png")
            msg_embed.add_field(name="Ball's Insight: ", value=response, inline=True)
            msg_embed.set_footer(text=f"***{config.eightball_footer}***")

            await try_reply(ctx, msg_embed)

    @commands.command(aliases=['r', 'dice', 'd'])
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
        msg_embed.description = '\n'.join((f"#{i + 1}: **{roll}**" for i, roll in enumerate(rolls)))
        msg_embed.add_field(name='sum', value=f'total = {sum(rolls)} + {offset} = {sum(rolls) + offset}', inline=True)

        await try_reply(ctx, msg_embed)


async def setup(bot):
    await bot.add_cog(Randomization(bot))
