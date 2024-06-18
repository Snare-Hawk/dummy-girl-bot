import discord
from discord import app_commands
from discord.ext import commands
from discord import utils
import random
import os
import re
from dotenv import load_dotenv, dotenv_values
import guildStuff

load_dotenv()
token = os.getenv("token")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.reactions = True

"""
TODO:
[ ] make it so bot edits messages upon more stars
[ ] figure out how to use a mosiac for multiple images (max of 4?)
[ ] make quick setup command
[ ] figure out database situation
[ ] add help, source, and emoji/channel/limit checks command
[ ] on addition of any new information, update json as we update dict
[ ] PERMISSIONS
"""

# try discord.ext.commands.errors.MissingRequiredArgument

bot = commands.Bot(command_prefix='?', intents=intents)

# global variables
bot.star_emoji = '👍'
bot.star_limit = 1
bot.star_channel = None

botID = 1251546997132099654
invite = f"https://discord.com/oauth2/authorize?client_id={botID}"

guildDict = {}

@bot.event
async def on_ready():
    bot.tree.sync()
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    guildDict = await guildStuff.guildInfo.getGuildList(bot)

    print(guildDict)


# get data from database
# store guild info

@bot.event
async def on_reaction_add(reaction, user):
    # sameChannel = reaction.message.channel
    
    if bot.star_channel is None:
        print("no channel setup")
    # if  bot.star_channel is reaction.message.channel:
    #     print("stop starring in the starboard channel fool")
    #     return
    # must check to see if reaction is the desired emoji
    if bot.star_emoji == reaction.emoji and bot.star_limit == reaction.count:
        # await sameChannel.send(f"\"{reaction.message.content}\" was the funny")
        await makeEmbed(reaction)

async def make_embed(reaction):
    """
    message: discord.Message
    """

    message = reaction.message

    bot.star_channel = message.channel
    # someUrl = "https://fallendeity.github.io/discord.py-masterclass/"
    author = message.author # discord.Member
    embed = discord.Embed(color=discord.Color.from_str("#00c900"), description=message.content)
    embed.set_author(name=author.display_name, icon_url=author.display_avatar.url)


    if message.attachments:
        # print("message has attachments")
        # print(message.attachments[0].content_type)
        # print(re.match("image",message.attachments[0].content_type))
        if re.search("image", message.attachments[0].content_type):
            # print("message has image")
            embed.set_image(url=message.attachments[0].url)
            # embed.set_image(url=message.attachments[0].url)

    # embed.add_field(name="Source", value=f"[jump to message]({message.jump_url})")
    # formatting = "%m/%d/%Y %I:%M %p"
    # embed.add_field(name="the jumper", value=f"[jump to message]({message.jump_url})")

    # messageTime = message.created_at
    # uniqueTime = utils.format_dt(messageTime, "t")
    embed.set_footer(text=f"{message.created_at.strftime('%x %I:%M %p')}")
    # embed.set_footer(text=f"{messageTime.strftime(f'%x {uniqueTime} %p')}")
    await bot.star_channel.send(f"{bot.star_emoji} **{reaction.count}** {message.jump_url}", embed=embed)

@bot.hybrid_command()
async def channel(ctx: commands.Context, channel: discord.abc.GuildChannel):
    """
    sets up starboard channel
    
    Parameters
    ----------
    ctx: commands.Context
        the context of the command invocation
    channel: discord.abc.GuildChannel
        the channel where dummy girl will post

    """
    bot.star_channel = channel
    await ctx.send(f"{bot.star_channel.mention} set as the starboard channel!")

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
            bot.star_emoji = discord.utils.get(ctx.guild.emojis, id=emoji_id)
            
            if bot.star_emoji:
                await ctx.send(f'{bot.star_emoji} set as emoji!')
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
    bot.star_limit = limit
    await ctx.send(f"{bot.star_emoji} limit set to {limit}!")

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
    await ctx.send(f"synced {len(synced)} commands globally :3")

@bot.hybrid_command()
@commands.is_owner()
async def shutdown(ctx: commands.Context):
    print("logging out...")
    await ctx.send("logging out...")
    await ctx.bot.close()


bot.run(token)