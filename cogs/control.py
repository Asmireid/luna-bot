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

    @commands.command(help="connects the bot to a voice channel")
    async def connect(self, ctx):
        if ctx.author.voice:
            msg_embed = make_embed(ctx,
                                   title=f"{Config().bot_name}'s Control",
                                   descr=f"Connecting to {ctx.author.voice.channel.name}.")
            await try_display_confirmation(ctx, msg_embed)

            if ctx.voice_client:
                # move to the author's current channel if bot is already in a channel
                await ctx.voice_client.move_to(ctx.author.voice.channel)
            else:
                await ctx.author.voice.channel.connect()
        else:
            await try_display_confirmation(ctx, "You're not connected to a voice channel.")

    @commands.command(help="disconnects the bot from a voice channel")
    async def disconnect(self, ctx):
        if ctx.voice_client:
            msg_embed = make_embed(ctx,
                                   title=f"{Config().bot_name}'s Control",
                                   descr=f"Disconnecting from {ctx.voice_client.channel.name}.")
            await try_display_confirmation(ctx, msg_embed)

            await ctx.voice_client.disconnect()
        else:
            await try_display_confirmation(ctx, "I'm not connected to a voice channel.")


async def setup(bot):
    await bot.add_cog(Control(bot))
