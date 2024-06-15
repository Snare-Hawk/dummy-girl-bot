import discord
from discord import app_commands
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

bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.emoji.id == 1232554847711006774:
        await reaction.message.channel.send("hi :3")
    else:
        return

@bot.hybrid_command()
async def setup(ctx: commands.Context, channel: discord.abc.GuildChannel):
    """
    sets up starboard channel
    
    Parameters
    ----------
    ctx: commands.Context
        The context of the command invocation
    channel: discord.abc.GuildChannel
        the channel where dummy girl will post

    """
    await ctx.send(channel.mention)

@bot.hybrid_command()
async def echo(ctx: commands.Context, message: str):
    """
    echoes a message

    Parameters
    ----------
    ctx: commands.Context
        The context of the command invocation
    message: str
        The message to echo
    """
    await ctx.send(message)

bot.run(token)