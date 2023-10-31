import discord
import os
import random
from discord.ext import commands


class Magic8ball(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command(aliases=["8ball", "eightball"])
    async def magic_eightball(self, ctx, *, question):
        with open("cogs/magic8ball_responses.txt", "r") as f:
            responses = f.readlines()
            response = random.choice(responses)

            user_message = " ".join(ctx.message.content.split(" ")[1:])

            embed_message = discord.Embed(title="Luna's Magic 8 Ball",
                                          description=user_message,
                                          color=discord.Color.dark_embed())

            embed_message.set_author(name=f"Requested by {ctx.author.nick}", icon_url=ctx.author.avatar)
            embed_message.set_thumbnail(url="https://static.thenounproject.com/png/371802-200.png")
            embed_message.add_field(name="Ball's Insight: ", value=response, inline=True)
            embed_message.set_footer(text="Don't trust Luna.",
                                     icon_url="https://static-00.iconduck.com/assets.00/new-moon-face-emoji-2048x2048-95mgz2k9.png")

            await ctx.send(embed=embed_message)


async def setup(client):
    await client.add_cog(Magic8ball(client))
