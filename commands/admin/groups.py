import discord
from discord.ext import commands

class GroupManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def createrole(self, ctx, *, name):
        """Create a new role"""
        try:
            role = await ctx.guild.create_role(name=name)
            embed = discord.Embed(
                title="Role Created",
                description=f"Created role {role.mention}",
                color=self.bot.colors['success']
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title="Error",
                description="I don't have permission to create roles",
                color=self.bot.colors['error']
            )
            await ctx.send(embed=embed)
            
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, member: discord.Member, *, role: discord.Role):
        """Add a role to a member"""
        if role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            embed = discord.Embed(
                title="Error",
                description="You can't assign roles higher than your top role",
                color=self.bot.colors['error']
            )
            await ctx.send(embed=embed)
            return
            
        try:
            await member.add_roles(role)
            embed = discord.Embed(
                title="Role Added",
                description=f"Added {role.mention} to {member.mention}",
                color=self.bot.colors['success']
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title="Error",
                description="I don't have permission to manage roles",
                color=self.bot.colors['error']
            )
            await ctx.send(embed=embed)
            
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, member: discord.Member, *, role: discord.Role):
        """Remove a role from a member"""
        if role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            embed = discord.Embed(
                title="Error",
                description="You can't remove roles higher than your top role",
                color=self.bot.colors['error']
            )
            await ctx.send(embed=embed)
            return
            
        try:
            await member.remove_roles(role)
            embed = discord.Embed(
                title="Role Removed",
                description=f"Removed {role.mention} from {member.mention}",
                color=self.bot.colors['success']
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title="Error",
                description="I don't have permission to manage roles",
                color=self.bot.colors['error']
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GroupManagement(bot))
