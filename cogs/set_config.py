import codecs
import configparser
import json

from utilities import *


async def set_helper(ctx, section, option, value: str):
    old_value = config.configs.get(section, option)    # extract old option's value before updating file

    config.configs.set(section, option, value)
    with codecs.open('config/config.ini', 'w', encoding='utf-8') as f:
        config.configs.write(f)     # overwrite old file with new value(s)

    conf_embed = make_embed(ctx,
                            title=f"{config.bot_name()}'s State",
                            descr=f"{option} is updated.")
    conf_embed.add_field(name="Old -> New", value=f"{old_value} -> {value}")
    await try_display_confirmation(ctx, conf_embed)


async def command_prefix(ctx, value):
    ctx.bot.command_prefix = value
    await set_helper(ctx, 'settings', 'command_prefix', value)


async def bot_name(ctx, value):
    server = ctx.bot.get_guild(ctx.guild.id)
    bot_member = server.get_member(ctx.bot.user.id)
    await bot_member.edit(nick=value)
    await set_helper(ctx, 'customizations', 'bot_name', value)


async def bot_activity(ctx, value):
    await ctx.bot.change_presence(activity=discord.CustomActivity(name=value))
    await set_helper(ctx, 'customizations', 'bot_activity', value)


async def embed_footer(ctx, value):
    await set_helper(ctx, 'customizations', 'embed_footer', value)


class SetConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command()
    async def set(self, ctx, option, *, value: str):
        switch_options = {
            'activity': bot_activity,
            'act': bot_activity,
            'name': bot_name,
            'embed_footer': embed_footer,
            'footer': embed_footer,
            'command_prefix': command_prefix,
            'prefix': command_prefix
        }

        set_function = switch_options.get(option, None)

        if set_function is not None:
            await set_function(ctx, value)
        else:
            await try_display_confirmation(ctx, f"{option} is not a valid option...")


async def setup(bot):
    await bot.add_cog(SetConfig(bot))
