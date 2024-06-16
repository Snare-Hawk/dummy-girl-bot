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

# global variables
bot.starEmoji = '⭐'
bot.starLimit = 1
invite = "https://discord.com/oauth2/authorize?client_id=1251546997132099654"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_reaction_add(reaction, user):
    sameChannel = reaction.message.channel

    # must check to see if reaction is the desired emoji
    if bot.starEmoji == reaction.emoji and bot.starLimit == reaction.count:
        await sameChannel.send(f"\"{reaction.message.content}\" was the funny")

    # if type(reaction.emoji) == str:
    #     await sameChannel.send("this is a unicode emoji")
    # elif type(reaction.emoji) == discord.partial_emoji:
    #     await sameChannel.send("what the fuck")
    # else:
    #     await sameChannel.send("this is a custom emoji")

@bot.hybrid_command()
async def channel(ctx: commands.Context, channel: discord.abc.GuildChannel, emoji: str):
    """
    sets up starboard channel
    
    Parameters
    ----------
    ctx: commands.Context
        the context of the command invocation
    channel: discord.abc.GuildChannel
        the channel where dummy girl will post

    """
    boardChannel = channel
    await ctx.send(f"{channel.mention} set as the starboard channel!")

@bot.hybrid_command()
async def emoji(ctx: commands.Context, emoji: str):
    """
    sets up starboard emoji
    
    Parameters
    ----------
    ctx: commands.Context
        the context of the command invocation
    emoji: str
        emoji that's used to determine when something goes on the starboard

    """
    if emoji.startswith('<:') and emoji.endswith('>'):
            # extract the emoji name and ID
            emoji_name = emoji.split(':')[1]
            emoji_id = int(emoji.split(':')[2][:-1])
            
            # fetch the emoji from the guild
            bot.starEmoji = discord.utils.get(ctx.guild.emojis, id=emoji_id)
            await ctx.send(f"type of bot.starEmoji: {type(bot.starEmoji)}")
            
            if bot.starEmoji:
                await ctx.send(f'{bot.starEmoji} set as emoji!')
            else:
                await ctx.send("emoji not found or the bot does not have access to it")
    else:
        await ctx.send("please input a proper emoji!")

@bot.hybrid_command()
async def limit(ctx: commands.Context, limit: int):
    """
    sets up how many emojis are required for a post in the starboard channel
    
    Parameters
    ----------
    ctx: commands.Context
        the context of the command invocation
    limit: int
        minimum number of reactions on a message for it to be posted in the starboard channel
    """
    bot.starLimit = limit
    await ctx.send(f"{bot.starEmoji} limit set to {limit}!")

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

@bot.hybrid_command()
async def invite(ctx: commands.Context) -> None:
    """
    sets up how many emojis are required for a post in the starboard channel
    
    Parameters
    ----------
    ctx: commands.Context
        the context of the command invocation
    """
    await ctx.send(f"invite me to other servers: {invite}")


@bot.hybrid_command()
@commands.is_owner()
async def sync(ctx: commands.Context) -> None:
    """sync commands"""
    synced = await ctx.bot.tree.sync()
    await ctx.send(f"Synced {len(synced)} commands globally")

bot.run(token)