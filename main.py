import discord
from discord import app_commands
from discord.ext import commands
from discord import utils
import os
import re
from emoji import is_emoji
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
[X] figure out database situation
[X] configure database things for when it joins a new server
[ ] add help, source, and emoji/channel/limit checks command
[ ] on addition of any new information, update json as we update dict
[ ] PERMISSIONS
"""

# try discord.ext.commands.errors.MissingRequiredArgument

bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    # await bot.tree.sync()
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    guildStuff.getGuildList(bot)

# get data from database
# store guild info

@bot.event
async def on_reaction_add(reaction, user):
    currentGuildID = reaction.message.guild.id
    starEmoji = guildStuff.guildList[f"{currentGuildID}"]["emoji"]
    starLimit = guildStuff.guildList[f"{currentGuildID}"]["limit"]

    if starEmoji == str(reaction.emoji) and starLimit == reaction.count:
        await makeEmbed(reaction)

@bot.event
async def on_guild_join(guild):
    textChannelIDs = [textChannel.id for textChannel in guild.text_channels]
    guildStuff(guild.id, textChannelIDs, None, '👍', 1)
    guildStuff.updateJSON()

async def makeEmbed(reaction):
    """
    message: discord.Message
    """

    message = reaction.message

    currentGuildID = reaction.message.guild.id

    starboardChannel = bot.get_channel(guildStuff.guildList[f"{currentGuildID}"]["starboard"])
    starEmoji = guildStuff.guildList[f"{currentGuildID}"]["emoji"]
    
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

    if starboardChannel == None:
        starboardChannel = reaction.message.channel
        await starboardChannel.send("there is no starboard channel set, so i'll just send it here :3")

    # TODO: if any message in the starboard channel has the same message jump_url, edit the message with different star count

    await starboardChannel.send(f"{starEmoji} **{reaction.count}** {message.jump_url}", embed=embed)

@bot.hybrid_group()
async def set(ctx: commands.Context) -> None:
    """
    configure starboard
    """
    await ctx.send("guh!")

@set.command(name="channel")
async def channel(ctx: commands.Context, channel: discord.abc.GuildChannel or int) -> None:
    """
    sets up starboard channel
    
    Parameters
    ----------
    ctx: commands.Context
        the context of the command invocation
    channel: discord.abc.GuildChannel
        the channel where dummy girl will post
    """

    # if channel is int:
    #     guildStuff.guildList[f"{ctx.guild.id}"]["starboard"] = channel

    guildStuff.guildList[f"{ctx.guild.id}"]["starboard"] = channel.id
    guildStuff.updateJSON()

    await ctx.send(f"{channel.mention} set as the starboard channel!")

@set.command(name="emoji")
async def emoji(ctx: commands.Context, emoji: str) -> None:
    """
    sets up starboard emoji
    
    Parameters
    ----------
    ctx: commands.Context
        the context of the command invocation
    emoji: str
        emoji that's used to determine when something goes on the starboard

    """

    if is_emoji(emoji):
        guildStuff.guildList[f"{ctx.guild.id}"]["emoji"] = emoji
        await ctx.send(f'{emoji} set as emoji!')
    elif re.match(r'<a?:\w+:\d+>', emoji):
            # extract the emoji name and ID
            emojiName = emoji.split(':')[1]
            emojiID = int(emoji.split(':')[2][:-1])
            
            # checks if the emoji is in the given guild
            starEmoji = discord.utils.get(ctx.guild.emojis, id=emojiID)
            
            if starEmoji:
                guildStuff.guildList[f"{ctx.guild.id}"]["emoji"] = emoji
                await ctx.send(f'{emoji} set as emoji!')
            else:
                await ctx.send("emoji not found or the bot does not have access to it")
    else:
        await ctx.send("please input a proper emoji!")
        return
    
    guildStuff.updateJSON()

@set.command(name="limit")
async def limit(ctx: commands.Context, limit: int) -> None:
    """
    sets up how many emojis are required for a post in the starboard channel
    
    Parameters
    ----------
    ctx: commands.Context
        the context of the command invocation
    limit: int
        minimum number of reactions on a message for it to be posted in the starboard channel
    """
    
    guildStuff.guildList[f"{ctx.guild.id}"]["limit"] = limit
    guildStuff.updateJSON()

    await ctx.send(f"{"star emoji"} limit set to {limit}!")

# @set.command(name="quicksetup")
# async def quickSetup(ctx: commands.Context, channel: discord.abc.GuildChannel, emoji: str, limit: int):
#     guh = channel.id
#     await channel(ctx, guh)
#     await emoji(ctx, emoji)
#     await limit(ctx, limit)
#     await ctx.channel.send("set up everything!")

@bot.hybrid_command()
async def echo(ctx: commands.Context, message: str):
    """
    echoes a message

    Parameters
    ----------
    ctx: commands.Context
        the context of the command invocation
    message: str
        the message to echo
    """
    await ctx.send(message)

@bot.hybrid_command()
async def invite(ctx: commands.Context) -> None:
    """
    sends bot invite link
    
    Parameters
    ----------
    ctx: commands.Context
        the context of the command invocation
    """
    await ctx.send(f"invite me to other servers with [this link](https://discord.com/oauth2/authorize?client_id={bot.user.id}) :3")

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