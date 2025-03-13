import discord
from discord.ext import commands

class Lookup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases=['uid'])
    async def userid(self, ctx, member: discord.Member = None):
        """Get user ID"""
        member = member or ctx.author
        embed = discord.Embed(
            title="User ID",
            description=f"ID for {member.name}: `{member.id}`",
            color=self.bot.colors['primary']
        )
        await ctx.send(embed=embed)
        
    @commands.command(aliases=['sid', 'gid'])
    async def serverid(self, ctx):
        """Get server/guild ID"""
        embed = discord.Embed(
            title="Server ID",
            description=f"ID for {ctx.guild.name}: `{ctx.guild.id}`",
            color=self.bot.colors['primary']
        )
        await ctx.send(embed=embed)
        
    @commands.command(aliases=['cid'])
    async def channelid(self, ctx, channel: discord.TextChannel = None):
        """Get channel ID"""
        channel = channel or ctx.channel
        embed = discord.Embed(
            title="Channel ID",
            description=f"ID for #{channel.name}: `{channel.id}`",
            color=self.bot.colors['primary']
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Lookup(bot))
