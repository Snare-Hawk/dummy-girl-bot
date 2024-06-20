import discord
import json
import os
from pathlib import Path

"""
holds required guild information

Variables
---------
channels: list of discord.TextChannel objects
    holds every channel that can be seen
starboard: discord.TextChannel
    the starboard channel
emoji: str or discord.Emoji
    emoji that is used for posts to go onto the starboard
limit: int
    minimum number of reactions on a message for it to be posted to starboard
"""
guildList = {}
filePath = Path("guildList.json")

def __init__(guildID, guildChannels, guildStarboard, guildEmoji, guildLimit):
    singleGuildInfo = {
        f"{guildID}":{
            "channels": guildChannels,
            "starboard": guildStarboard,
            "emoji": guildEmoji,
            "limit": guildLimit
            }
        }

    guildList.update(singleGuildInfo)

def getGuildList(bot):
    if os.path.exists(filePath):
        with open(filePath, 'r', encoding="utf-8") as file:
            guildList = json.load(file)
    # best case scenario, this function should only trigger once
    else: # if it doesn't exist get info from the guilds that the bot is in
        for guild in bot.guilds: # list of all the guilds bot is in
            textChannelIDs = [textChannel.id for textChannel in guild.text_channels]
            __init__(guild.id, textChannelIDs, None, '👍', 1)
            
        updateJSON()

def updateJSON():
    with open(filePath, 'w+', encoding="utf-8") as outfile:
        json.dump(guildList, outfile, indent=4)
