import codecs
import configparser
import json

from utilities import *


def get_status():
    return config.bot_status


def update_status(new_status):
    config.configs.set('customizations', 'bot_status', new_status)
    with codecs.open('config/config.ini', 'w', encoding='utf-8') as f:
        config.configs.write(f)


class SetConf(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command()
    async def set(self, ctx, conf, *, new_conf: str):
        if conf == 'status':
            await self.set_status(ctx, new_conf)

    async def set_status(self, ctx, new_status: str):
        update_status(new_status)
        await self.bot.change_presence(activity=discord.CustomActivity(name=new_status))
        if config.display_confirmation:
            msg = f"My new status is: {new_status}."
            conf = await try_reply(ctx, msg)
            await try_delete_confirmation(conf)
        await try_delete_invocation(ctx.message)


async def setup(bot):
    await bot.add_cog(SetConf(bot))
