from utilities import *


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command()
    async def ping(self, ctx):
        try:
            latency = round(self.bot.latency * 1000)
            msg_embed = make_embed(ctx,
                                   title=f"{Config().bot_name}'s Clock",
                                   descr=f"Current latency is {latency} ms.")
            await try_reply(ctx, msg_embed)
        except Exception as e:
            print(f"An error occurred: {e}")


async def setup(bot):
    await bot.add_cog(Ping(bot))
