import discord 
from discord.ext import commands

class VoiceCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Voice Commands Cog has been added")

    @commands.command(pass_context = True)
    async def join(self, ctx):
        if(ctx.author.voice):
            channel = ctx.message.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("You are not in a voice channel, join a channel and run this command! I'll be joining you once you are in a voice channel!")
        
    @commands.command(pass_context = True)
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.guild.voice_client.disconnect()
            await ctx.send("I left the voice channel")
        else:
            await ctx.send("I'm not in a voice channel!")
    
async def setup(bot):
    await bot.add_cog(VoiceCommands(bot))