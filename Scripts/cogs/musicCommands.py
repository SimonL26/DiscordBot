import discord
from discord.ext import commands
import wavelink
from wavelink.ext import spotify
import json
import typing

# adding spotify client ID
file = open("spotify.json")
jsonfile = json.load(file)
SECRET = jsonfile['spotify_secret']

class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        """Connect to Lavalink nodes"""
        await self.bot.wait_until_ready()

        await wavelink.NodePool.create_node(
                            bot=self.bot, 
                            host="127.0.0.1", 
                            port="2333",
                            password="protectedpassword",
                            region="europe",
                            spotify_client=spotify.SpotifyClient(client_id="b7958513cb5e4939923ae9691944182f",
                                                                client_secret=SECRET))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music Commands Cog has been added")

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        """Fired when node finished connecting"""
        print(f'Node: <{node.identifier}> is ready!')
    
    @commands.command(name="join", aliases=['connect', 'c'], description="Join in a voice channel")
    async def join(self, ctx: commands.Context, channel:typing.Optional[discord.VoiceChannel]):
        if channel is None:
            channel = ctx.author.voice.channel
        
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is not None:
            if player.is_connected():
                return await ctx.send("Bot is connected to a voice channel")
            
        await channel.connect(cls=wavelink.Player)
        return await ctx.send(f"Connected to {channel.name}")

    @commands.command(name="leave", aliases=['disconnect', 'dc'], description="Leave the voice channel")
    async def leave(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        
        if player is None:
            return await ctx.send("Bot is not connected to any voice channel")
        
        await player.disconnect()
        return await ctx.send(f"Disconnected from {ctx.author.voice.channel.name}")

    @commands.command(name="play", aliases=["p"], description='Play music from a url')
    async def play(self, ctx: commands.Context, *, query_url):
        # later update to play spotify
        track = await wavelink.YouTubeTrack.search(query=query_url, return_first=True)

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            vc: wavelink.Player = ctx.voice_client

        await vc.play(track)

        msg = discord.Embed(title=f"Playing {query_url}")
        return await ctx.send(embed=msg)

    @commands.command(name="pause", aliases=['p'], description="Pause current playing music")
    async def pause(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.send("Bot is not connected to any voice channel")
        
        if not player.is_paused:
            if player.is_playing:
                await player.pause()
                return await ctx.send("Playback paused")
            else:
                return await ctx.send("Nothing is playing right now")
        else:
            return await ctx.send("Playback is already pasued")

    @commands.command(name="stop", description="Stop current playing music")
    async def stop(self, ctx:commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.send("Bot is not connected to any voice channel")

        if player.is_playing:
            await player.stop()
            return await ctx.send("Playback stopped")
        else:
            return await ctx.send("Nothing is playing right now")

    @commands.command(name="resume", description="resume playing music")
    async def resume(self, ctx:commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.send("Bot is not connected to any voice channel")
        
        if player.is_paused():
            await player.resume()
            return await ctx.send("Playback resumed")
        else:
            return await ctx.send("Playback is already playing")

    @commands.command(name="volume", description="Set the volume of the player")
    async def volume(self, ctx:commands.Context, vol: int):
        if vol > 100:
            return await ctx.send("Volume should be between 0 and 100")
        elif vol < 1:
            return await ctx.send("Volume should be between 0 and 100")

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        await player.set_volume(vol)
        return ctx.send(f"Volume set to {vol}%")


async def setup(bot):
    await bot.add_cog(MusicCommands(bot))