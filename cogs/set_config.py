import codecs
import configparser
import json

from utilities import *


def get_status():
    return config.bot_status


async def set_helper(ctx, section, option, value: str):
    config.configs.set(section, option, value)
    with codecs.open('config/config.ini', 'w', encoding='utf-8') as f:
        config.configs.write(f)
    await try_display_confirmation(ctx, f"My new {option} is: {value}.")


async def command_prefix(ctx, value):
    ctx.bot.command_prefix = value
    await set_helper(ctx, 'settings', 'command_prefix', value)


async def bot_status(ctx, value):
    await ctx.bot.change_presence(activity=discord.CustomActivity(name=value))
    await set_helper(ctx, 'customizations', 'bot_status', value)


class SetConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command()
    async def set(self, ctx, option, *, value: str):
        switch_options = {
            'status': bot_status,
            'command_prefix': command_prefix
        }

        set_function = switch_options.get(option, None)

        if set_function is not None:
            await set_function(ctx, value)
        else:
            await try_display_confirmation(ctx, f"{option} is an invalid option...")


async def setup(bot):
    await bot.add_cog(SetConfig(bot))
