import os

import discord
from discord.ext import commands

from utilities import *


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command(aliases=['查成分'])
    async def userinfo(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        roles = [role for role in member.roles]
        try:
            msg_embed = make_embed(ctx,
                                   title=f"{Config().bot_name}'s Inspection",
                                   descr=f"User info on {member.mention}")
            msg_embed.set_thumbnail(url=member.avatar)
            msg_embed.add_field(name='ID', value=member.id)
            msg_embed.add_field(name='Name', value=member.name)
            msg_embed.add_field(name='Nickname', value=member.display_name)
            msg_embed.add_field(name='Status', value=member.status)
            msg_embed.add_field(name='Created At', value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"))
            msg_embed.add_field(name='Joined At', value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"))
            msg_embed.add_field(name=f'Roles ({len(roles)})', value=' '.join([role.mention for role in roles]))
            msg_embed.add_field(name='Top Role', value=member.top_role.mention)
            msg_embed.add_field(name='Bot?', value=member.bot)
            await try_reply(ctx, msg_embed)
        except Exception as e:
            print(f"An error occurred: {e}")

    @commands.command(help=f"deletes x messages from the current channel: {Config().command_prefix}clear x")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, count: int):
        def is_not_command_message(message):
            return message.id != ctx.message.id

        # +1 accounts for the clear command itself
        await ctx.channel.purge(limit=count + 1, check=is_not_command_message)

        conf_embed = make_embed(ctx,
                                title=f"{Config().bot_name}'s Purge",
                                descr=f"{count} message(s) cleared.")
        await try_display_confirmation(ctx, conf_embed)

    @commands.command(help=f"kicks an user from server: {Config().command_prefix}kick @member reason")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, mod_reason):
        await ctx.guild.kick(member)

        conf_embed = make_embed(ctx,
                                title=f"{Config().bot_name}'s Purge",
                                descr=f"{member.mention} has been kicked from the server.")
        conf_embed.add_field(name="Reason:", value=mod_reason)
        await try_display_confirmation(ctx, conf_embed)

    @commands.command(help=f"bans an user from server: {Config().command_prefix}ban @member reason")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, mod_reason):
        await ctx.guild.ban(member)

        conf_embed = make_embed(ctx,
                                title=f"{Config().bot_name}'s Purge",
                                descr=f"{member.mention} has been banned from the server.")
        conf_embed.add_field(name="Reason:", value=mod_reason)
        await try_display_confirmation(ctx, conf_embed)

    @commands.command(help=f"unbans an user from server: {Config().command_prefix}unban user_id")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id):
        user = discord.Object(id=user_id)
        await ctx.guild.unban(user)

        conf_embed = make_embed(ctx,
                                title=f"{Config().bot_name}'s Mercy",
                                descr=f"<@{user_id}> has been unbanned from the server.")
        await try_display_confirmation(ctx, conf_embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
