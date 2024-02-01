import os

from discord.ext import commands

from utilities import *


async def set_helper(ctx, option, value: str):
    configs = Config()

    # Check if the specified option exists as an attribute of the Config instance
    if hasattr(configs, option):

        # makes sure user cannot alter credentials in Discord
        if configs.is_sensitive(option):
            await try_reply(ctx, f"{option} is sensitive information. Please set it in the config.ini file.")
            return

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
    ctx.bot.command_prefix = value.split(' ')
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

    @commands.command(help="sets config.ini attributes")
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

    @commands.command(help="gets config.ini attributes")
    async def get(self, ctx, option):
        configs = Config()

        # Check if the specified option exists as an attribute of the Config instance
        if hasattr(configs, option):

            if configs.is_sensitive(option):
                await try_reply(ctx, f"{option} is sensitive information. I cannot get it to you.")
                return

            # Use getattr() to dynamically access the attribute based on the option string
            value = getattr(configs, option)

            msg_embed = make_embed(ctx,
                                   title=f"{configs.bot_name}'s State",
                                   descr=f"{option} is retrieved.")
            msg_embed.add_field(name=option, value=value)
            await try_reply(ctx, msg_embed)
        else:
            await try_reply(ctx, f"{option} is not a valid option...")

    @commands.command(aliases=['list_conf', 'lsc'], help="lists all config.ini attributes")
    async def list_config(self, ctx):
        configs = Config()

        msg_embed = make_embed(ctx,
                               title=f"{configs.bot_name}'s State",
                               descr="Configs are retrieved.")

        try:
            options_and_values = {str(prop): getattr(configs, str(prop)) for prop in dir(configs) if
                                  isinstance(getattr(type(configs), str(prop), None), property)}
            for option, value in options_and_values.items():
                # only list non-sensitive configs
                if not configs.is_sensitive(option):
                    msg_embed.add_field(name=option, value=value)

            await try_reply(ctx, msg_embed)
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")


async def setup(bot):
    await bot.add_cog(SetConfig(bot))
