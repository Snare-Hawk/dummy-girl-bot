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
    guildList = {}

    def __init__(self, guildID, guildChannels, guildStarboard, guildEmoji, guildLimit):
        guildID = {
            "channels": guildChannels,
            "starboard": guildStarboard,
            "emoji": guildEmoji,
            "limit": guildLimit
        }
        print(guildID)
        self.guildList.update(guildID)


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

            print(list(guilds))

            for guild in guilds:
                
                guildInfo(guild.id, list(guild.channels), None, '👍', 1)
                """WHEN INPUTTING A CHANNEL, IT MUST BE ITS ID OR THE JSON WILL ERROR"""
                # guildInfo.guildList.update(guildEntry)

            
            with open(filePath, 'w+', encoding="utf-8") as outfile: # create it, 
            # add info to dict, then dicttojson
                # outfile.write(json.dumps(guildInfo.getGuildList, indent=4))
                json.dump(guildInfo.guildList, outfile)

        # print(guildInfo.guildList)
        guildInfo.typeOf(guildInfo.guildList)

        return guildInfo.guildList

    # temporary testing tfunctions
    def disObjToID(channelList):
        """
        Parameters
        ----------
        channelList: list of discord.channel
        """
        channelIDs = []
        for channel in channelList:
            channelIDs.append(channel.id)
        return channelIDs

    def typeOf(whatever):
        print(f"{type(whatever)}")