import discord
from discord import Member
from discord.ext import commands
from pymongo import MongoClient
import pymongo


level = ["Junior", "Mid-Level", "Senior"]
levelnum = [4,10,15]

cluster = MongoClient("mongodb+srv://tarkvarabot:tarkvarabot21@cluster0.2pybb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

levelling = cluster["discord"]["levelling"]



class levelsystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("level system ready!")
    

    @commands.Cog.listener()
    async def on_message(self, message):
            stats = levelling.find_one({"id" : message.author.id})
            if not message.author.bot:
                if stats is None:
                    newuser = {"id" : message.author.id, "xp" : 0}
                    levelling.insert_one(newuser)
                else:
                    xp = stats["xp"] + 5
                    levelling.update_one({"id" : message.author.id}, {"$set":{"xp":xp}})
                    lvl = 0
                    while True:
                        if xp < ((50*(lvl**2))+(50*lvl)):
                            break
                        lvl += 1
                    xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                    if xp == 0:
                        await message.channel.send(f"Well done {message.author.mention}! You leveled up to **level: {lvl}**!")
                        for i in range(len(level)):
                            if lvl == levelnum[i]:
                                await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level[i]))
                                embed = discord.Embed(description=f"{message.author.mention} you have gotten role **{level[i]}**!!!")
                                embed.set_thumbnail(url=message.author.avatar_url)
                                await message.channel.send(embed=embed)
                    
    @commands.command()
    async def rank(self, ctx):
            stats = levelling.find_one({"id" : ctx.author.id})
            if stats is None:
                embed = discord.Embed(description="**FAILED:** You haven't sent any messages, no rank!!!", color=discord.Color.red())
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
                boxes = int((xp/(200*((1/2) * lvl)))*20)
                rankings = levelling.find().sort("xp", -1)
                for x in rankings:
                    rank += 1
                    if stats["id"] == x["id"]:
                        break
                embed = discord.Embed(color=discord.Color.blue())
                embed.add_field(name="__**USER's RANK**__", value=f"**Nickname: {ctx.author.mention}**\n" f"**Rank:** {lvl} [{xp}/{int(200*((1/2)*lvl))}]", inline=False) 

                embed.add_field(name="**Progress Bar [lvl]**", value=boxes*":blue_square:" + (20-boxes) * ":white_large_square:" , inline=False) 
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def givelevel(self, ctx,   member: Member , arg = 0):
        if ctx.message.author.guild_permissions.administrator:
            if arg == 0:
                embed = discord.Embed(description="**FAILED:** You did not enter level you want to give... Try again using 'givelevel [Nick/Mention] [Level]' ",color=discord.Color.red())
                await ctx.channel.send(embed=embed)
                return
            lvl = arg
            stats = levelling.find_one({"id" :member.id})
            xp = int(((50*((lvl-1)**2))+(50*(lvl-1))))
            levelling.update_one({"id" : member.id}, {"$set":{"xp":xp}})
            await ctx.channel.send(f"Well done {member.mention}! You leveled up to **level: {lvl}**!")
        else:
            embed = discord.Embed(description="You don't have server administrator permission to use this command...")
            await ctx.channel.send(embed=embed)    

    @commands.command()
    async def leaderboard(self, ctx):
            rankings = levelling.find().sort("xp",-1)
            i = 1
            embed = discord.Embed(title="**Rankings:**", color=discord.Color.blue())
            for x in rankings:
                try:
                    tempxp = x["xp"]
                    xp = tempxp
                    lvl = 0
                    while True:
                            if xp < ((50*(lvl**2))+(50*lvl)):
                                break
                            lvl += 1
                    xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                    temp = ctx.guild.get_member(x["id"])
                    embed.add_field(name=f"**{i}:** {temp}", value=f"**Rank:** {lvl} [{xp}/{int(200*((1/2)*lvl))}] **Total XP:**{tempxp}", inline=False)

                    i += 1
                except:
                    pass
                if i == 11:
                    break
            await ctx.channel.send(embed=embed)
def setup(bot):
    bot.add_cog(levelsystem(bot))