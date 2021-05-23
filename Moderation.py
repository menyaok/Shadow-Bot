import discord
from discord.ext import commands

with open("badwords.txt", "r") as file:
    words = file.readlines()
filtered_words = [word.strip("\n") for word in words]

LIMIT = 10

f = open("rules.txt", "r")
rules = f.readlines()
f.close()


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation ready!")

    @commands.Cog.listener()
    async def on_message(self, message):
        for word in filtered_words:
            if word in message.content.lower().split(" "):
                await message.delete()
                await message.channel.send(f"{message.author.mention}, your message has been censored!")
                self.add_strike(str(message.author))

                if self.strike_count(str(message.author)) >= 10:
                    with open('Reminder_to_kick.txt', 'r') as f:
                        kick_dict = eval(f.readlines()[0])
                    if kick_dict[str(message.author)]['was_kicked']:
                        await message.author.ban()
                    else:
                        kick_dict[str(message.author)]['was_kicked'] = True
                        kick_dict[str(message.author)]['strike_count'] = 0
                        with open('Reminder_to_kick.txt', 'w') as f:
                            f.write(str(kick_dict))
                        await message.author.kick()

                elif self.strike_count(str(message.author)) >= 3:
                    await message.channel.send(f"{message.author.mention}, after writing {LIMIT - self.strike_count(str(message.author))} more swear words, you will be kicked from the server!")

    @commands.command()
    async def rules(self, ctx):
        embed = discord.Embed(title="Rules", color=discord.Color.blue())
        for i in range(len(rules)):
            embed.add_field(name=f"Rule №{i + 1}", value=f"{rules[i]}", inline=False)
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def clear(self, ctx, amount=10):
        if ctx.message.author.guild_permissions.administrator:
            embed = discord.Embed(title=f"{ctx.message.author} deleted {amount} messages in the chat ",
                                  color=discord.Color.blue())
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.channel.purge(limit=amount)
            await ctx.channel.send(embed=embed)
        else:
            embed = discord.Embed(description="**FAILED:** You don't have server administrator permission to use this command...",color=discord.Color.red())
            await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=" No reason provided"):
        if ctx.message.author.guild_permissions.administrator:
            embed = discord.Embed(description=f"**MODERATION:** {member.mention}has been kicked from the server, because: {reason}",color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            await member.kick(reason=reason)
        else:
            embed = discord.Embed(description="**FAILED:** You don't have server administrator permission to use this command...", color=discord.Color.red())
            await ctx.channel.send(embed=embed)


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=" No reason provided"):
        if ctx.message.author.guild_permissions.administrator:
            embed = discord.Embed(description=f"**MODERATION:** {member.mention}has been banned from the server, because: {reason}",color=discord.Color.red())
            await ctx.channel.send(embed=embed)
            await member.ban(reason=reason)
        else:
            embed = discord.Embed(description="**FAILED:** You don't have server administrator permission to use this command...", color=discord.Color.red())
            await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        if ctx.message.author.guild_permissions.administrator:
            banned_users = await ctx.guild.bans()
            member_name, member_disc = member.split('#')

            for banned_entry in banned_users:
                user = banned_entry.user

                if (user.name, user.discriminator) == (member_name, member_disc):
                    await ctx.guild.unban(user)
                    embed = discord.Embed(description=f"**MODERATION:** {user.name}has been unbanned",color=discord.Color.red())
                    await ctx.channel.send(embed=embed)

                    return

            await ctx.send(member + " was not found")
        else:
            embed = discord.Embed(description="**FAILED:** You don't have server administrator permission to use this command...", color=discord.Color.red())
            await ctx.channel.send(embed=embed)

    def add_strike(self, author):
        if self.is_empty():
            with open("Reminder_to_kick.txt", 'w') as file:
                file.write("{}")

        with open("Reminder_to_kick.txt", "r") as file:
            kick_dict = eval(file.readlines()[0])
        if author in kick_dict:
            kick_dict[author]['strike_count'] += 1
        else:
            kick_dict[author] = {'strike_count': 1, 'was_kicked': False}

        with open("Reminder_to_kick.txt", "w") as f:
            f.write(str(kick_dict))

    def strike_count(self, author):
        if self.is_empty():
            with open("Reminder_to_kick.txt", 'w') as file:
                file.write("{}")

        with open("Reminder_to_kick.txt", "r") as file:
            kick_dict = eval(file.readlines()[0])
        if author in kick_dict:
            return kick_dict[author]['strike_count']
        else:
            return 0

    def is_empty(self):
        with open("Reminder_to_kick.txt", 'r') as file:
            if len(file.readlines()) == 0:
                return True
            return False


def setup(bot):
    bot.add_cog(Moderation(bot))
