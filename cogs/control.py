import os
import sys
from discord.ext import commands
from utilities import *


class Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command(help=f"shuts down the bot: {Config().command_prefix}shutdown")
    async def shutdown(self, ctx):
        try:
            msg_embed = make_embed(ctx,
                                   title=f"{Config().bot_name}'s Control",
                                   descr=f"Shutting down...")
            await try_display_confirmation(ctx, msg_embed)
            await ctx.bot.close()
        except Exception as e:
            print(f"An error occurred: {e}")

    # @commands.command(help=f"restarts the bot: {Config().command_prefix}restart")
    # async def restart(self, ctx):
    #     try:
    #         msg_embed = make_embed(ctx,
    #                                title=f"{Config().bot_name}'s Control",
    #                                descr=f"Restarting...")
    #         await try_display_confirmation(ctx, msg_embed)
    #         await ctx.bot.close()
    # 
    #         # Restart the bot by running the script again
    #         python = sys.executable
    #         os.execl(python, python, *sys.argv)
    #     except Exception as e:
    #         print(f"An error occurred: {e}")


async def setup(bot):
    await bot.add_cog(Control(bot))
