import discord
from discord.ext import commands
from settings import Settings

import asyncio
import json
import random
import typing
import levelsystem
import Moderation
import minigames
import info
import music

ai_settings = Settings()
bot = commands.Bot(command_prefix = ai_settings.Token['prefix'], intents=discord.Intents.all())
cogs = [levelsystem, Moderation, minigames, info, music]


for i in range(len(cogs)):
    cogs[i].setup(bot)

bot.run(ai_settings.Token['token']) 
