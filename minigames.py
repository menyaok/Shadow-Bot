import discord
from discord.ext import commands
import random
import json

class minigames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("minigames ready!")

    @commands.command()
    async def roll(self, ctx, arg = 101):
        if arg < 2:
            embed = discord.Embed(title="__**ROLL THE DICE**__", description=f"**FAILED:** entered number must be at least 2", color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            return
        result = random.randint(1,arg)
        embed = discord.Embed(title="__**ROLL THE DICE**__", description=f"**{ctx.author.mention} rolled the dice and got:** {result}", color=discord.Color.blue())
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def coin(self, ctx):
        value = random.randint(1,2)
        if value == 1:
            embed = discord.Embed(title="__**COIN FLIP**__",description=f"**{ctx.author.mention}flipped the coin and got:** HEADS",   color=discord.Color.blue())
        else:
            embed = discord.Embed(title="__**COIN FLIP**__",description=f"**{ctx.author.mention} flipped the coin and got:** TAILS", color=discord.Color.blue())
        await ctx.channel.send(embed=embed)   

def setup(bot):
    bot.add_cog(minigames(bot))
