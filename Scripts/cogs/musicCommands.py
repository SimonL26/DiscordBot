import discord
from discord.ext import commands
import wavelink
from wavelink.ext import spotify
import json
import typing
import asyncio

# adding spotify client ID
file = open("cogs/spotify.json")
jsonfile = json.load(file)
SECRET = jsonfile['spotify_secret']

class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.songqueue = []
        self.playingTextChannel = 0

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
        self.bot.loop.create_task(self.connect_nodes())

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        """Fired when node finished connecting"""
        print(f'Node: <{node.identifier}> is ready!')

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, player: wavelink.Player, track: wavelink.Track):
        try:
            self.songqueue.pop(0)
        except Exception:
            pass 

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player:wavelink.Player, track:wavelink.Track, reason):
        if str(reason) == "FINISHED":
            if not len(self.songqueue) == 0:
                next_track:wavelink.Track = self.songqueue[0]
                channel = self.bot.get_channel(self.playingTextChannel)

                try:
                    await player.play(next_track)
                except:
                    return await channel.send(f"Oops... Something went wrong while playing **{next_track.title}**")

                await channel.send(f"Now playing: {next_track.title}")
            else:
                pass
        else:
            print(reason)

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
        self.playingTextChannel = ctx.author.voice.channel.id
        return await ctx.send(f"Connected to {channel.name}")

    @commands.command(name="leave", aliases=['disconnect', 'dc'], description="Leave the voice channel")
    async def leave(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)
        
        if player is None:
            return await ctx.send("Bot is not connected to any voice channel")
        
        if player.is_playing():
            await player.stop()
            await player.disconnect()
            self.playingTextChannel = 0
            return await ctx.send(f"Disconnected from {ctx.author.voice.channel.name}")

        await player.disconnect()
        self.playingTextChannel = 0
        return await ctx.send(f"Disconnected from {ctx.author.voice.channel.name}")

    @commands.command(name="play", aliases=["p"], description='Play music from a url')
    async def play(self, ctx: commands.Context, *, query_url):
        # later update to play spotify
        try:
            track = await wavelink.YouTubeTrack.search(query=query_url, return_first=True)
        except:
            return await ctx.reply("Something went wrong while searching for this track")

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            self.playingTextChannel = ctx.author.voice.channel.id
        else:
            vc: wavelink.Player = ctx.voice_client

        if not vc.is_playing():
            try:
                await vc.play(track)
            except:
                return await ctx.reply("Something went wrong while trying to play this track.")
        else:
            self.songqueue.append(track)
    
        msg = discord.Embed(title=f"Added {track} to the queue")
        return await ctx.send(embed=msg)

    @commands.command(name="pause", description="Pause current playing music")
    async def pause(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.send("Bot is not connected to any voice channel")
        
        if not player.is_paused():
            if player.is_playing():
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
        
        self.songqueue.clear()

        if player.is_playing():
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
            if not len(self.songqueue) == 0:
                track: wavelink.Track = self.songqueue[0]
                player.play(track)
                return await ctx.reply(f"Now playing: {track.title}")
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

    @commands.command(name="playonly", description="Play a track without adding it to the song queue")
    async def playonly(self, ctx: commands.Context, *, search: str):
        try:
            track = await wavelink.YouTubeTrack.search(query=search, return_first=True)
        except: 
            return await ctx.reply(f"Something went wrong while searching for {search}")
        
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel(cls=wavelink.Player)
            self.playingTextChannel = ctx.author.voice.channel.id
            await player.connect(ctx.author.voice.channel)
        else:
            vc:wavelink.Player = ctx.voice_client

        try:
            await vc.play(track)
        except:
            return await ctx.reply("Something went wrong while playing this track")
        await ctx.reply(f"Playing **{track.title}** now")

    @commands.command(name="nowplaying")
    async def nowplaying(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if player is None:
            return await ctx.reply("Bot is not connected to any voice channel")

        if player.is_playing():
            t_sec = int(player.track.length)
            hour = int(t_sec/3600)
            minutes = int((t_sec%3600)/60)
            sec = int((t_sec%3600)%60)
            track_length = f"{hour}hr {minutes}min {sec}sec" if not hour == 0 else f"{minutes}min {sec}sec"
            
            embed = discord.Embed(
                title=f"Now playing: {player.track}"
            )
            embed.add_field(name="Artist", value=player.track.info['author'], inline=False)
            embed.add_field(name="Length", value=f"{track_length}", inline=False)

            return await ctx.reply(embed=embed)
        else:
            return await ctx.reply("Nothing is playing right now")
        
    @commands.command(name="search")
    async def search(self, ctx: commands.Context, *, query: str):
        try:
            tracks = await wavelink.YouTubeTrack.search(query=query)
        except:
            return await ctx.reply(f"Something went wrong while trying to search for {query}")

        if tracks is None:
            return await ctx.reply("I found nothing 😢")
        
        embed = discord.Embed(
            title="I found these tracks, select one!",
            description=("\n".join(f"**{i+1}. {t.title}**" for i, t in enumerate(tracks[:5])))
        )

        message = await ctx.reply(embed=embed)

        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "❌"]
        emoji_dict = {
            "1️⃣": 0,
            "2️⃣": 1,
            "3️⃣": 2,
            "4️⃣": 3,
            "5️⃣": 4,
            "❌": -1
        }

        for emoji in list(emojis[:min(len(tracks), len(emojis))]):
            await message.add_reaction(emoji)
    
        try:
            reaction, user = await self.bot.wait_for("reaction_add", 
                                                    timeout = 60.0, 
                                                    check=lambda r, u: r.emoji in emojis and u.id == ctx.author.id and r.message.id == message.id)
            await message.remove_reaction(reaction.emoji, user)
        except asyncio.TimeoutError:
            return await message.delete()
        else:   
            await message.delete()

        try:
            if emoji_dict[reaction.emoji] == -1: return
            chosen_track = tracks[emoji_dict[reaction.emoji]]
        except:
            return

        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            self.playingTextChannel = ctx.author.voice.channel.id
        else:
            vc: wavelink.Player = ctx.voice_client

        if not vc.is_playing():
            try:
                await vc.play(chosen_track)
            except:
                return await ctx.reply("Something went wrong while playing the track")
        else:
            self.songqueue.append(chosen_track)

        await ctx.reply(f"Added {chosen_track.title} to the queue")

    @commands.command(name="skip")
    async def skip(self, ctx: commands.Context):
        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild)

        if not len(self.songqueue) == 0:
            next_track: wavelink.Track  = self.songqueue[0]
            try:
                await player.play(next_track)
            except:
                return await ctx.reply("Something went wrong while trying to play this track")
            
            await ctx.reply(f"Now playing: {next_track.title}")
        else:
            await ctx.reply("Track list is empty!")

async def setup(bot):
    await bot.add_cog(MusicCommands(bot))