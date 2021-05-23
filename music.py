import discord
from discord.ext import commands
import youtube_dl
import os

client = commands.Bot(command_prefix="!")

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

            
    @commands.command()
    async def play(self, ctx, url : str):
        voice_state = ctx.message.author.voice
        if voice_state is None:
            embed = discord.Embed(title="__**MUSIC**__", description=f"**FAILED:** You need to be in a voice channel to use this command", color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            embed = discord.Embed(title="__**MUSIC**__", description=f"**FAILED:** Bot is already playing music, wait for the end or use the **'stop'** command", color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return
        embed = discord.Embed(title="__**MUSIC**__", description=f"**Bot is currently setting up his microphone, wait a few second...**", color=discord.Color.blue())
        await ctx.channel.send(embed=embed)
        channel = ctx.message.author.voice.channel
        await channel.connect()
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))


    @commands.command()
    async def leave(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
            embed = discord.Embed(title="__**MUSIC**__", description="*Bye!!! Hope you had a good time listening to tunes... See you!**", color=discord.Color.blue())
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(title="__**MUSIC**__", description=f"**FAILED:** Bot is not connected to any voice channel, use the **'play [url]'** command to add Bot to voice channel", color=discord.Color.red())
            await ctx.channel.send(embed=embed)


    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            embed = discord.Embed(title="__**MUSIC**__", description=f"**FAILED:** Bot don't playing any music to be paused.", color=discord.Color.red())
            await ctx.channel.send(embed=embed)



    @commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            embed = discord.Embed(title="__**MUSIC**__", description=f"**FAILED:** Music is not paused or played music has ended, try **'play [url]'**", color=discord.Color.red())
            await ctx.channel.send(embed=embed)


    @commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()
        embed = discord.Embed(title="__**MUSIC**__", description=f"**Music has been stopped, use **'play [url]'** to add another song**", color=discord.Color.blue())
        await ctx.channel.send(embed=embed)
def setup(client):
    client.add_cog(music(client))