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
        await ctx.channel.purge(limit=count + 1)  # +1 accounts for the clear command itself

        await try_display_confirmation(ctx, f"{count} message(s) cleared.")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, mod_reason):
        await ctx.guild.kick(member)

        conf_embed = discord.Embed(title="Success", color=discord.Color.green())
        conf_embed.add_field(name="Kicked:",
                             value=f"{member.mention} has been kicked from the server by {ctx.author.mention}.")
        conf_embed.add_field(name="Reason:", value=mod_reason)
        await try_display_confirmation(ctx, conf_embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, mod_reason):
        await ctx.guild.ban(member)

        conf_embed = discord.Embed(title="Success", color=discord.Color.green())
        conf_embed.add_field(name="Banned:",
                             value=f"{member.mention} has been banned from the server by {ctx.author.mention}.")
        conf_embed.add_field(name="Reason:", value=mod_reason)
        await try_display_confirmation(ctx, conf_embed)

    @commands.command(name="unban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id):
        user = discord.Object(id=user_id)
        await ctx.guild.unban(user)

        conf_embed = discord.Embed(title="Success", color=discord.Color.green())
        conf_embed.add_field(name="Unbanned:",
                             value=f"<@{user_id}> has been banned from the server by {ctx.author.mention}.")
        await try_display_confirmation(ctx, conf_embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
