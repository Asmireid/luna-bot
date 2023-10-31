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

        if config.display_confirmation:
            conf = await ctx.send(f"{count} message(s) cleared.")
            await try_delete(conf)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, mod_reason):
        await ctx.guild.kick(member)

        if config.display_confirmation:
            conf_embed = discord.Embed(title="Success", color=discord.Color.green())
            conf_embed.add_field(name="Kicked:",
                                 value=f"{member.mention} has been kicked from the server by {ctx.author.mention}.")
            conf_embed.add_field(name="Reason:", value=mod_reason)
            conf = await ctx.send(conf_embed)
            await try_delete(conf)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, mod_reason):
        await ctx.guild.ban(member)

        if config.display_confirmation:
            conf_embed = discord.Embed(title="Success", color=discord.Color.green())
            conf_embed.add_field(name="Banned:",
                                 value=f"{member.mention} has been banned from the server by {ctx.author.mention}.")
            conf_embed.add_field(name="Reason:", value=mod_reason)
            conf = await ctx.send(conf_embed)
            await try_delete(conf)

    @commands.command(name="unban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user_id):
        user = discord.Object(id=user_id)
        await ctx.guild.unban(user)

        if config.display_confirmation:
            conf_embed = discord.Embed(title="Success", color=discord.Color.green())
            conf_embed.add_field(name="Unbanned:",
                                 value=f"<@{user_id}> has been banned from the server by {ctx.author.mention}.")
            conf = await ctx.send(conf_embed)
            await try_delete(conf)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
