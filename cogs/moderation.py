from utilities import *


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{os.path.basename(__file__)} is ready.")

    @commands.command()
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

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, mod_reason):
        await ctx.guild.kick(member)

        conf_embed = make_embed(ctx,
                                title=f"{Config().bot_name}'s Purge",
                                descr=f"{member.mention} has been kicked from the server.")
        conf_embed.add_field(name="Reason:", value=mod_reason)
        await try_display_confirmation(ctx, conf_embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, mod_reason):
        await ctx.guild.ban(member)

        conf_embed = make_embed(ctx,
                                title=f"{Config().bot_name}'s Purge",
                                descr=f"{member.mention} has been banned from the server.")
        conf_embed.add_field(name="Reason:", value=mod_reason)
        await try_display_confirmation(ctx, conf_embed)

    @commands.command(name="unban")
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
