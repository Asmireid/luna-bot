import os
from discord.ext import commands
from utilities import *


class Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command(help="shuts down the bot")
    async def shutdown(self, ctx):
        try:
            msg_embed = make_embed(ctx,
                                   title=f"{Config().bot_name}'s Control",
                                   descr=f"Shutting down...")
            await try_display_confirmation(ctx, msg_embed)
            await ctx.bot.close()
        except Exception as e:
            print(f"An error occurred: {e}")


async def setup(bot):
    await bot.add_cog(Control(bot))
