import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv, dotenv_values 

load_dotenv()

token = os.getenv("token")


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


# @bot.on_reaction_add()
# async def yeahReactions(ctx, num: int):
#     if (num % 2 != 0):
#        await ctx.send("balls is odd")
#     else:
#        await ctx.send("balls is even")

@bot.command()
async def hi(ctx):
    await ctx.send("hiiiiii :3")

bot.run(token)