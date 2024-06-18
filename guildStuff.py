import discord
import json
import os
from pathlib import Path

# to be put into a dict of dicts
# to then be written to a json eventually
class guildInfo:
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
    def __init__(self, guildID, guildChannels, guildStarboard, guildEmoji, guildLimit):
        guildID = {
            "channels": guildChannels,
            "starboard": guildStarboard,
            "emoji": guildEmoji,
            "limit": guildLimit
        }
        # return guildID

    guildList = {}

    async def getGuildList(client):
        filePath = Path("guildList.json")

        if os.path.exists(filePath):
            with open(filePath, 'r', encoding="utf-8") as file:
                guildInfo.guildList = json.load(file)
        # best case scenario, this function should only trigger once
        else: # if it doesn't exist
            # get info from guilds bot is in
            # list of all the guilds bot is in 
            guilds = [guild async for guild in client.fetch_guilds(limit=150)]
            for guild in guilds:
                # channels = [channel async for channels in guild.fetch_channels()]
                # channels = guild.channels
                # for channel in guild.channels:
                guildEntry = guildInfo(guild.id, guild.channels, None, '👍', 1)
                guildInfo.guildList.update(guildEntry)

            with open(filePath, 'r', encoding="utf-8") as file: # create it, 
            # add info to dict, then dicttojson
                jsonObject = json.dumps(guildInfo.guildList)
                file.write(jsonObject)

        return guildInfo.guildList