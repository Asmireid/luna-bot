import os
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command()
    async def ping(self, ctx):
        latency = round(self.client.latency * 1000)
        await ctx.send(f"Current latency is {latency} ms.")


async def setup(client):
    await client.add_cog(Ping(client))
