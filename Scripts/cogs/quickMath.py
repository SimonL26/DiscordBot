import discord
from discord.ext import commands

class QuickMath(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print("Quick Math Cog has been added")

    @commands.command()
    async def add(self, ctx, a:float, b:float):
        """Adds two numbers together"""
        await ctx.send(a+b)
    
    @commands.command()
    async def subtract(self, ctx, a:float, b: float):
        """Subtracts b from a"""
        await ctx.send(a-b)

    @commands.command()
    async def multiply(self, ctx, a:float, b:float):
        """Multiply two numbers together, rounds up to two decimal numbers"""
        result = round(a*b, 2)
        await ctx.send(result)

    @commands.command()
    async def divide(self, ctx, a:float, b:float):
        """Divide b from a, rounds up to two decimal numbers"""
        if b == 0:
            await ctx.send(f"Oops... I cannot divide 0")
        result = round(a/b, 2)
        await ctx.send(result)

async def setup(bot: commands.Bot):
    await bot.add_cog(QuickMath(bot))