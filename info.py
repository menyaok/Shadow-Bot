import discord
from discord import Member
from discord.ext import commands
from pymongo import MongoClient
import pymongo
cluster = MongoClient("mongodb+srv://tarkvarabot:tarkvarabot21@cluster0.2pybb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

levelling = cluster["discord"]["levelling"]

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("info ready!")

    @commands.command()
    async def server(self, ctx, guild: discord.Guild = None):
        guild = ctx.guild
        roles = str(len(guild.roles))
       
        channels = str(len(guild.channels))
         
        admins = 0
        for k in ctx.guild.members:
            if k.guild_permissions.administrator: 
                admins = admins + 1


        embed = discord.Embed(color=discord.Color.blue())
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name=f"__**{guild.name} - Server Info**__\n", value=f"\n\n**Created on:** {guild.created_at.strftime('%d %B %Y')}\n\n"
            f"**Server ID:** {guild.id}\n\n"
            f"**Owner:** {guild.owner.mention}\n\n"
            f"**Users on server:** {guild.member_count}\n\n"
            f"**Administrator count:** {admins}\n\n"
            f"**Administrators :** {' '.join([k.mention for k in ctx.guild.members if k.guild_permissions.administrator])}\n\n"
            f"**Location:** {guild.region}\n\n"
            f"**Role Count:** {roles}\n\n"
            f"**Roles:** {' '.join([r.mention for r in guild.roles[1:]])}\n\n"
            f"**Channel Count:** {channels}", inline=False)
        
        await ctx.channel.send(embed=embed) 

    @commands.command()
    async def userinfo(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.author
        embed = discord.Embed(color=discord.Color.blue(),title=f"**Information about user: {user.name}**")
        embed.set_footer(text=f"ID: {user.id}")
        embed.set_thumbnail(url=user.avatar_url_as(format="png"))
        embed.add_field(name="__**General information**__", value=f"\n\n**Discord Name:** {user}\n\n"
                                                                   f"**Account created:** {user.created_at.__format__('%A %d %B %Y')}\n\n"
                                                                   , inline=False)

        stats = levelling.find_one({"id" : user.id})
        if stats is None:
            embed = discord.Embed(description="**You haven't sent any messages, no rank!!!**")
            await ctx.channel.send(embed=embed)
        else:
            xp = stats["xp"]
            lvl = 0
            rank = 0
            while True:
                    if xp < ((50*(lvl**2))+(50*lvl)):
                        break
                    lvl += 1
            xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
            rankings = levelling.find().sort("xp", -1)
            for x in rankings:
                rank += 1
                if stats["id"] == x["id"]:
                    break
            admin = "No"
            if user.guild_permissions.administrator:      
                admin = "Yes"
            embed.add_field(name=f"__**Related information with server:**__ **{ctx.guild.name}**", value=f"**Nickname on this server:** {user.mention}\n\n"
                                                                              f"**Joined server:** {user.joined_at.__format__('%A %d %B %Y at %H:%M')}\n\n"
                                                                              f"**Roles:** {' '.join([r.mention for r in user.roles[1:]])}\n\n"
                                                                              f"**Administrator:** {admin}\n\n"
                                                                              f"**Rank:** {lvl} [{xp}/{int(200*((1/2)*lvl))}]")


            await ctx.channel.send(embed=embed) 

    @commands.command()
    async def avatar(self, ctx, *,  avamember : discord.Member=None):
        userAvatarUrl = avamember.avatar_url
        embed = discord.Embed(title="__**AVATAR**__", description=f"**{ctx.author.mention}'s profile picture**", color=discord.Color.blue())
        embed.set_image(url=userAvatarUrl)
        await ctx.channel.send(embed=embed) 


    @commands.command()
    async def cmdlist(self, ctx):
        embed = discord.Embed( color=discord.Color.blue())
        embed.add_field(name="__**AVAILABLE BOT COMMANDS**__", 
        value=
        "__**INFO**__\n"
        "!rules - _list of rules_\n"
        "!cmdlist - _list of available commands_\n"
        "!roles - _list of roles on this server_\n"
        "!server - _information about this server_\n"
        "!userinfo [Nickname/Mention] - _information about user_\n"
        "!avatar [Nickname/Mention] - _show user's avatar_\n"
        "!rank - _check your rank_\n"
        "!leaderboard - _check leaderboard table_\n"

        "__**MINI-GAMES**__\n"
        "!roll [amount] - _roll the dice_\n"
        "!coin - _roll the coin_\n"

        "__**MUSIC**__\n"
        "!play [url] - _play music in your voice channel_\n"
        "!stop - _skip current song_\n"
        "!pause - _pause current song_\n"
        "!resume - _unpause current song_\n"
        "!leave - _disconnect bot from voice channel_\n"

        "__**MODERATION [for admins only]**__\n"
        "!kick [user] [reason]\n"
        "!ban [user] [reason]\n"
        "!unban [user] [reason]\n"
        "!givelevel [user] [level]\n"
        "!clear [amount] - _dellet fixed amount of messages in the chat_\n", inline=True)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        await ctx.channel.send(embed=embed) 
    @commands.command()
    async def roles(self, ctx):
        i = 0
        embed = discord.Embed(color=discord.Color.blue())
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.add_field(name=f"__**ROLES**__", value=f"{' '.join([r.mention for r in ctx.guild.roles[1:]])}\n\n", inline=True)
        await ctx.channel.send(embed=embed)   

def setup(bot):
    bot.add_cog(info(bot))
