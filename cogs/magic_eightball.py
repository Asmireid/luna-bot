import random

from utilities import *


class Magic8ball(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command(aliases=["8ball", "eightball"])
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


async def setup(bot):
    await bot.add_cog(Magic8ball(bot))
