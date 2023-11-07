import os

from discord.ext import commands

from utilities import *


async def set_helper(ctx, option, value: str):
    configs = Config()

    # Check if the specified option exists as an attribute of the Config instance
    if hasattr(configs, option):
        # Use getattr() to dynamically access the attribute based on the option string
        old_value = getattr(configs, option)
        # Modify the attribute with the new value
        setattr(configs, option, value)

        conf_embed = make_embed(ctx,
                                title=f"{configs.bot_name}'s State",
                                descr=f"{option} is updated.")
        conf_embed.add_field(name="Old -> New", value=f"{old_value} -> {value}")
        await try_display_confirmation(ctx, conf_embed)

    else:
        await try_reply(ctx, f"{option} is not a valid option...")


async def command_prefix(ctx, value):
    ctx.bot.command_prefix = value
    await set_helper(ctx, 'command_prefix', value)


async def bot_name(ctx, value):
    server = ctx.bot.get_guild(ctx.guild.id)
    bot_member = server.get_member(ctx.bot.user.id)
    await bot_member.edit(nick=value)
    await set_helper(ctx, 'bot_name', value)


async def bot_activity(ctx, value):
    await ctx.bot.change_presence(activity=discord.CustomActivity(name=value))
    await set_helper(ctx, 'bot_activity', value)


class SetConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command(help=f"sets config.ini attributes: {Config().command_prefix}set example_attr new_value")
    async def set(self, ctx, option, *, value: str):
        switch_options = {
            'activity': bot_activity,
            'act': bot_activity,
            'bot_name': bot_name,
            'name': bot_name,
            'command_prefix': command_prefix,
            'prefix': command_prefix
        }

        set_function = switch_options.get(option, None)

        if set_function is not None:
            await set_function(ctx, value)
        else:
            await set_helper(ctx, option, value)


async def setup(bot):
    await bot.add_cog(SetConfig(bot))
