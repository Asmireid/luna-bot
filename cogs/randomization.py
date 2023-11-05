import random
import re
import requests
import json

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
        try:
            with open("cogs/magic8ball_responses.txt", "r") as f:
                responses = f.readlines()
                response = random.choice(responses)

            msg_embed = make_embed(ctx,
                                   title=f"{config.bot_name()}'s Magic 8 Ball",
                                   descr=question)
            msg_embed.set_thumbnail(url="https://static.thenounproject.com/png/371802-200.png")
            msg_embed.add_field(name="Ball's Insight: ", value=response, inline=True)

            await try_reply(ctx, msg_embed)

        except FileNotFoundError:
            print("File not found. Make sure the file path is correct.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @commands.command(aliases=['r', 'dice', 'd'])
    async def roll(self, ctx, *, cmd: str):
        parts = re.split(r"[d+]+", cmd)
        try:
            count, sides, offset = {
                1: lambda cmds: (1, int(cmds[0]), 0),  # "x"
                2: lambda cmds: (int(cmds[0]), int(cmds[1]), 0),  # "xdy"
                3: lambda cmds: (int(cmds[0]), int(cmds[1]), int(cmds[2]))  # "xdy+z"
            }[len(parts)](parts)
        except ValueError:
            await ctx.send(f"'{cmd}' is not a valid input for my dice.")
            return

        rolls = [random.randint(1, sides) for _ in range(count)]

        msg_embed = make_embed(ctx,
                               title=f"{config.bot_name()}'s Dice",
                               descr=f"{count}d{sides}+{offset}")
        msg_embed.description = '\n'.join((f"#{i + 1}: **{roll}**" for i, roll in enumerate(rolls)))
        msg_embed.add_field(name='sum', value=f'total = {sum(rolls)} + {offset} = {sum(rolls) + offset}', inline=True)

        await try_reply(ctx, msg_embed)

    @commands.command()
    async def joke(self, ctx):
        try:
            with open("cogs/jokes.txt", "r", encoding='utf-8') as f:
                jokes = f.readlines()
                joke = random.choice(jokes)
                # Parse the random line using "<>" as the delimiter
                question, answer = joke.strip().split('<>')

            msg_embed = make_embed(ctx,
                                   title=f"{config.configs.get('customizations', 'bot_name')}'s Joke",
                                   descr=question)
            msg_embed.add_field(name="", value=answer, inline=True)

            await try_reply(ctx, msg_embed)

        except FileNotFoundError:
            print("File not found. Make sure the file path is correct.")
        except Exception as e:
            print(f"An error occurred: {e}")


async def setup(bot):
    await bot.add_cog(Randomization(bot))
