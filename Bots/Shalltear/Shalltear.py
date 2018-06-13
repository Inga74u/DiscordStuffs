import requests
import asyncio
import discord
import time
import json
import os

from Bot import Permissions
from Bot import Youtube
from Bot import osuipy

Commands = {}
Token = ""
Prefix = ""
dPrefix = "!"
OsuCmds = False
OsuKey = None
OwnerId = ""

DataFile = ".\\Bot\\Data.json"
AudioData = {}

OsuBase = "https://osu.ppy.sh/api/"

Path = os.path.abspath(".\\External\\ffmpeg\\bin")
AppPath = os.path.join(Path)
os.environ["PATH"] += os.pathsep + AppPath

# Helper Functions

def cls():
    print("\n"*150)

def testInt(D):
    try:
        int(D)
        return True
    except:
        return False

def join(List, Spacer):
    String = ""

    for x in List:
        String += x
        if x != x[len(x)-1]:
            String += Spacer

    return String

def schedule_coroutine(target, loop = None):
    if asyncio.iscoroutine(target):
        return asyncio.ensure_future(target, loop = loop)
    raise TypeError("target must be a coroutine, "

                    "not {!r}".format(type(target)))
    
# Load Data

cls()

try:
    with open(DataFile, "r") as DF:
        Data = json.load(DF)

    Token = Data["BotConfig"]["Token"]
    Prefix = Data["BotConfig"]["Prefix"]
    OsuCmds = Data["BotConfig"]["OsuCmds"]
    OsuKey = Data["BotConfig"]["OsuKey"]
    OwnerId = Data["BotConfig"]["OwnerId"]
except:
    while len(Prefix.strip()) == 0:
        Prefix = input("Please enter bot prefix: ")
        cls()

    while len(Token.strip()) == 0:
        Token = input("Please enter bot token: ")
        cls()

    OwnerId = input("Please enter your user id (Optional): ")
    cls()

    Data = {
        "BotConfig": {
            "Token": Token,
            "Prefix": Prefix,
            "OsuCmds": False,
            "OsuKey": None,
            "OwnerId": OwnerId
        }
    }

    with open(DataFile, "w") as DF:
        json.dump(Data, DF, indent = 4)

# Create Command Stuffs

class _createCommand:
    def __init__(self, Call, Description, Function, Perms, PermMod, OId):
        self.Call = Call
        self.Description = Description
        self.Function = Function
        self.Perms = Perms

        self.PermMod = PermMod
        self.OwnerId = OId

    async def Do(self, Bot, Msg, Args):
        if self.PermCheck(Msg):
            await self.Function(Bot, Msg, Args)

    def PermCheck(self, Msg):
        Perms = self.PermMod.PermsList(Msg.author.server_permissions)

        if self.Perms == self.PermMod.Default or self.Perms in Perms or Msg.author.id == self.OwnerId:
            return True
        return False

def createCommand(Call, Description, Function, Perms):
    Commands[Call] = _createCommand(Call, Description, Function, Perms, Permissions, OwnerId)

# Command Functions

async def Repeat(Bot, Msg, Args):
    await Bot.send_message(Msg.channel, Msg.content)

async def Purge(Bot, Msg, Args):
    if len(Args) > 0:
        Limit = Args[0]
        isInt = True

        try:
            int(Limit)
        except:
            isInt = False

        if isInt:
            Limit = int(Limit)
            if Limit > 100:
                Limit = 100
            elif Limit < 0:
                Limit = 0

            Limit += 1 # Extra Messages

            await Bot.purge_from(Msg.channel, limit = Limit)
        else:
            await Bot.send_message(Msg.channel, Msg.author.mention + ", " + str(Limit) + " is not a number.")
    else: # Forgot to say how many? No problem.
        await Bot.send_message(Msg.channel, Msg.author.mention + ", How many messages do you want to try to delete?")
        Ans = await Bot.wait_for_message(timeout = 10, author = Msg.author, channel = Msg.channel)

        if Ans != None:
            Limit = Ans.content
            isInt = True

            try:
                int(Limit)
            except:
                isInt = False

            if isInt:
                Limit = int(Limit)
                if Limit > 100:
                    Limit = 100
                elif Limit < 0:
                    Limit = 0

                Limit += 3 # Extra Messages

                await Bot.purge_from(Msg.channel, limit = Limit)
            else:
                await Bot.send_message(Msg.channel, Msg.author.mention + ", " + str(Limit) + " is not a number.")

async def ListCommands(Bot, Msg, Args):
    Cmds = "***Commands***\n"

    for x in Commands:
        Cmds += "\n**" + x.capitalize() + "** ```" + Commands[x].Description + "```"

    await Bot.send_message(Msg.channel, Msg.author.mention + ",\n" + Cmds)

async def Osu(Bot, Msg, Args):
    if OsuCmds:
        tMsg = "What would you like to do?\n`1`. Lookup User\n`2`. Lookup User Best"
        tMsg = await Bot.send_message(Msg.channel, Msg.author.mention + ", " + tMsg)
        Resp = await Bot.wait_for_message(timeout = 10, author = Msg.author, channel = Msg.channel)
        
        await Bot.delete_message(tMsg)
        toSay = ""
        if Resp != None:
            if testInt(Resp.content):
                Ans = int(Resp.content)
                if Ans == 1:
                    tMsg = await Bot.send_message(Msg.channel, Msg.author.mention + ", What is the user's name?")
                    Resp = await Bot.wait_for_message(timeout = 10, author = Msg.author, channel = Msg.channel)
                    
                    await Bot.delete_message(tMsg)
                    if Resp != None:
                        Name = Resp.content
                        
                        tMsg = "What mode would you like to retrieve for?\n`1`. Standard\n`2`. Taiko\n`3`. Catch The Beat\n`4`. Mania"
                        tMsg = await Bot.send_message(Msg.channel, Msg.author.mention + tMsg)
                        Resp = await Bot.wait_for_message(timeout = 10, author = Msg.author, channel = Msg.channel)
                        
                        await Bot.delete_message(tMsg)
                        if Resp != None:
                            if testInt(Resp.content):
                                Mode = int(Resp.content) - 1
                                if Mode >= 0 and Mode <= 3:
                                    
                                    Headers = {"k": OsuKey,
                                               "u": Name,
                                               "m": Mode}
                                    
                                    OsuResp = requests.get(OsuBase + "get_user", Headers)
                                    if OsuResp.status_code == 200:
                                        UserData = json.loads(OsuResp.content.decode('utf-8'))
                                        if len(UserData) > 0:
                                            UserData = UserData[0]
                                            Name = UserData['username']
                                            c300 = UserData['count300']
                                            c100 = UserData['count100']
                                            c50 = UserData['count50']
                                            PlayCount = UserData['playcount']
                                            Rank = UserData['pp_rank']
                                            CountryRank = UserData['pp_country_rank']
                                            SS = UserData['count_rank_ss']
                                            S = UserData['count_rank_ss']
                                            Acc = UserData['accuracy']
                                            Level = UserData['level']
                                        else:
                                            toSay += "Could not find user data."
                                    else:
                                        toSay += "There was a problem accessing OsuApi."
                                else:
                                    toSay += "You selected an invalid mode!"
                            else:
                                toSay += "You selected an invalid mode!"
                        else:
                            toSay += "You did not respond, command timed out."
                    else:
                        toSay += "You did not respond, command timed out."
                elif Ans == 2:
                    tMsg = await Bot.send_message(Msg.channel, Msg.author.mention + ", What is the user's name?")
                    Resp = await Bot.wait_for_message(timeout = 10, author = Msg.author, channel = Msg.channel)
                    
                    await Bot.delete_message(tMsg)
                    if Resp != None:
                        Name = Resp.content
                        
                        tMsg = "What mode would you like to retrieve for?\n`1`. Standard\n`2`. Taiko\n`3`. Catch The Beat\n`4`. Mania"
                        tMsg = await Bot.send_message(Msg.channel, Msg.author.mention + tMsg)
                        Resp = await Bot.wait_for_message(timeout = 10, author = Msg.author, channel = Msg.channel)
                        
                        await Bot.delete_message(tMsg)
                        if Resp != None:
                            if testInt(Resp.content):
                                Mode = int(Resp.content) - 1
                                if Mode >= 0 and Mode <= 3:
                                    
                                    Headers = {"k": OsuKey,
                                               "u": Name,
                                               "m": Mode,
                                               "limit": 1}
                                    
                                    OsuResp = requests.get(OsuBase + "get_user_best", Headers)
                                    if OsuResp.status_code == 200:
                                        MapData = json.loads(OsuResp.content.decode('utf-8'))
                                        if len(MapData) > 0:
                                            MapData = MapData[0]
                                            Score = MapData['score']
                                            MaxCombo = MapData['maxcombo']
                                            c300 = MapData['count300']
                                            c100 = MapData['count100']
                                            c50 = MapData['count50']
                                            cMiss = MapData['countmiss']
                                            Rank = MapData['rank']
                                            PP = MapData['pp']
                                            Perfect = MapData['perfect']
                                            
                                            Embed = discord.Embed(title = "User Best", color = Msg.author.color) # Create Embed
                                            Embed.set_footer(text = "Osu")
                                            # Embed.set_image(url = Songs[0]["thumbnail"]) TODO:
                                            Embed.add_field(name = "Score", value = score)
                                            Embed.add_field(name = "PP", value = PP)
                                            Embed.add_field(name = "Combo", value = MaxCombo)
                                            Embed.add_field(name = "Rank", value = Rank)
                                            Embed.add_field(name = "300", value = c300)
                                            Embed.add_field(name = "100", value = c100)
                                            Embed.add_field(name = "50", value = c50)
                                            
                                            await Bot.send_message(Msg.channel, embed = Embed)
                                        else:
                                            toSay += "Could not find user data."
                                    else:
                                        toSay += "There was a problem accessing OsuApi."
                                else:
                                    toSay += "You selected an invalid mode!"
                            else:
                                toSay += "You selected an invalid mode!"
                        else:
                            toSay += "You did not respond, command timed out."
                    else:
                        toSay += "You did not respond, command timed out."
                else:
                    toSay += "You selected an invalid option!"
        else:
            toSay += "You did not respond, command timed out."
    else:
        toSay += "Osu commands are currently disabled."
    
    await Bot.send_message(Msg.channel, Msg.author.mention + ", " + toSay)

async def Join(Bot, Msg, Args):
    if Msg.author.voice.voice_channel != None:
        voice = AudioData[Msg.server.id]["voice"]

        if voice == None:
            voice = await Bot.join_voice_channel(Msg.author.voice.voice_channel)
            AudioData[Msg.server.id]["voice"] = voice
        elif voice.is_connected():
            if len(voice.channel.voice_members) == 0:
                await voice.move_to(Msg.author.voice.voice_channel)
                AudioData[Msg.server.id]["voice"] = voice
            else:
                await Bot.send_message(Msg.channel, Msg.author.mention + ", The bot is currently in another channel with users.")
    else:
        await Bot.send_message(Msg.channel, Msg.author.mention + ", You need to be in a voice channel to use this command.")

async def Leave(Bot, Msg, Args):
    voice = AudioData[Msg.server.id]["voice"]
    player = AudioData[Msg.server.id]["player"]

    if voice != None:
        if Msg.author.voice.voice_channel == voice.channel:
            if len(voice.channel.voice_members) == 1:
                if player != None:
                    player.stop()
                    AudioData[Msg.server.id]["player"] = None
                await voice.disconnect()
                AudioData[Msg.server.id]["voice"] = None
            elif Permissions.Administrator in Permissions.PermsList(Msg.author.server_permissions) or Msg.author.id == OwnerId:
                if player != None:
                    player.stop()
                    player = AudioData[Msg.server.id]["player"] = None
                await voice.disconnect()
                AudioData[Msg.server.id]["voice"] = None
            else:
                await Bot.send_message(Msg.channel, Msg.author.mention + ", You can not use this command when there are other people in the voice channel.")
        else:
            await Bot.send_message(Msg.channel, Msg.author.mention + ", You must be in the same channel as me to use this command.")
    else:
        await Bot.send_message(Msg.channel, Msg.author.mention + ", I'm not in a channel to leave!")

async def Play(Bot, Msg, Args):
    if len(Args) > 0:
        q = join(Args, " ")
    else:
        await Bot.send_message(Msg.channel, Msg.author.mention + ", You need to tell me what song to play, to play one at all.")
        return

    if AudioData[Msg.server.id]['voice'] == None or AudioData[Msg.server.id]["voice"].channel != Msg.author.voice.voice_channel:
        await Join(Bot, Msg, Args)

    if AudioData[Msg.server.id]['voice'] != None and AudioData[Msg.server.id]['voice'].is_connected():
        Songs = Youtube.search_list(q)

        if len(Songs) == 1:
            #AudioData[Msg.server.id]['queue'].append(Songs[0]["id"]) # Add to queue
            player = AudioData[Msg.server.id]['player']

            if player != None:
                player.stop()
            
            player = await AudioData[Msg.server.id]['voice'].create_ytdl_player("https://www.youtube.com/watch?v="+Songs[0]["id"])
            player.volume = 0.5

            player.start()

            await asyncio.sleep(.5)

            AudioData[Msg.server.id]['player'] = player
            AudioData[Msg.server.id]['queue'].insert(0, Songs[0]) # For 'now playing' command
            del AudioData[Msg.server.id]['queue'][1] # Delete song overwritten

            await Bot.send_message(Msg.channel, Msg.author.mention + ",\n**Now Playing**\n```" + Songs[0]["title"] + "```\n" + "Uploaded by `" + Songs[0]["chantitle"] + "`\n" +Songs[0]["thumbnail"])
        else:
            await Bot.send_message(Msg.channel, Msg.author.mention + ", Nothing found.")
    else:
        return

async def Search(Bot, Msg, Args):
    if len(Args) > 0:
        q = join(Args, " ")
    else:
        await Bot.send_message(Msg.channel, Msg.author.mention + ", You need to tell me what song to play, to play one at all.")
        return

    if AudioData[Msg.server.id]['voice'] == None or AudioData[Msg.server.id]["voice"].channel != Msg.author.voice.voice_channel:
        await Join(Bot, Msg, Args)

    if AudioData[Msg.server.id]['voice'] != None and AudioData[Msg.server.id]['voice'].is_connected():
        Songs = Youtube.search_list(q)

        if len(Songs) == 1:
            AudioData[Msg.server.id]['queue'].append(Songs[0]) # Add to queue
            
            Embed = discord.Embed(title = "Song Added To Queue", color = Msg.author.color) # Create Embed
            Embed.set_footer(text = "Search")
            Embed.set_image(url = Songs[0]["thumbnail"])
            Embed.add_field(name = "Title", value = Songs[0]["title"])
            Embed.add_field(name = "Uploader", value = Songs[0]["chantitle"])
            
            # await Bot.send_message(Msg.channel, Msg.author.mention + ",\n**Added to Queue**\n```" + Songs[0]["title"] + "```\n" + "Uploaded by `" + Songs[0]["chantitle"] + "`\n" +Songs[0]["thumbnail"])
            await Bot.send_message(Msg.channel, embed = Embed)
        else:
            await Bot.send_message(Msg.channel, Msg.author.mention + ", Nothing found.")
    else:
        return

async def Ping(Bot, Msg, Args):
    if len(Args) == 0:
        await Bot.send_message(Msg.channel, "Pong!")

async def Playlist(Bot, Msg, Args):
    if len(Args) > 0:
        q = join(Args, " ")
    else:
        await Bot.send_message(Msg.channel, Msg.author.mention + ", You need to tell me what playlist you want, for me to add its songs.")
        return
    
    if AudioData[Msg.server.id]['voice'] == None or AudioData[Msg.server.id]['voice'].channel != Msg.author.voice.voice_channel:
        await Join(Bot, Msg, Args)
    
    if AudioData[Msg.server.id]['voice'] != None and AudioData[Msg.server.id]['voice'].is_connected():
        Playlist = Youtube.search_playlist(q)
        
        if len(Playlist) == 1:
            Songs = Youtube.get_playlist_items(Playlist[0]['id'])
            
            if len(Songs) > 0:
                SongNum = str(len(Songs))
                
                for Song in Songs:
                    AudioData[Msg.server.id]['queue'].append(Song) # Add to queue
                
                Embed = discord.Embed(title = "Songs Added To Queue", color = Msg.author.color) # Create Embed
                Embed.set_footer(text = "Playlist")
                Embed.set_image(url = Playlist[0]["thumbnail"])
                Embed.add_field(name = "Playlist", value = Songs[0]["title"])
                Embed.add_field(name = "Songs Added", value = SongNum)
                
                await Bot.send_message(Msg.channel, Msg.author.mention + ",\nAdded `" + SongNum + "` songs from playlist:\n```" + Playlist[0]['title'] +"```\n\n" + Playlist[0]['thumbnail'])
            else:
                await Bot.send_message(Msg.channel, Msg.author.mention + ",\n Playlist was found, but no songs could be added.")
        else:
            await Bot.send_message(Msg.channel, Msg.author.mention + ",\nNo playlists were found.")

async def Playing(Bot, Msg, Args):
    
    def notPlaying():
        if AudioData[Msg.server.id]['voice'] == None:
            return True
        elif AudioData[Msg.server.id]['player'] == None:
            return True
        elif not AudioData[Msg.server.id]['voice'].is_connected():
            return True
        elif not AudioData[Msg.server.id]['player'].is_playing():
            return True
        return False
    
    if notPlaying():
        await Bot.send_message(Msg.channel, Msg.author.mention + ", Nothing is playing right now.")
    else:
        Song = AudioData[Msg.server.id]['queue'][0]
        
        Embed = discord.Embed(title = "Now Playing", color = Msg.author.color) # Create Embed
        Embed.set_footer(text = "Now Playing")
        Embed.set_image(url = Song["thumbnail"])
        Embed.add_field(name = "Title", value = Song["title"])
        Embed.add_field(name = "Uploader", value = Song["chantitle"])
    
        await Bot.send_message(Msg.channel, embed = Embed)

async def Skip(Bot, Msg, Args):
    def notPlaying():
        if AudioData[Msg.server.id]['voice'] == None:
            return True
        elif AudioData[Msg.server.id]['player'] == None:
            return True
        elif not AudioData[Msg.server.id]['voice'].is_connected():
            return True
        elif not AudioData[Msg.server.id]['player'].is_playing():
            return True
        return False

    if notPlaying():
        await Bot.send_message(Msg.channel, Msg.author.mention + ", I need to be playing something to skip!")
        return

    if len(AudioData[Msg.server.id]['queue']) == 1:
        await Bot.send_message(Msg.channel, Msg.author.mention + ", There is no songs in queue to skip to!")
        return

    player = AudioData[Msg.server.id]['player']
    player.stop()

async def Clear(Bot, Msg, Args):
    CSong = AudioData[Msg.server.id]['queue'][0]
    AudioData[Msg.server.id]['queue'] = [CSong]

    await Bot.send_message(Msg.channel, Msg.author.mention + ", Queue has been cleared.")

async def Queue(Bot, Msg, Args):
    Q = AudioData[Msg.server.id]['queue']
    RMsg = Msg.author.mention+","

    if len(Q) == 1:
        RMsg += " There are no songs in the queue!"

    elif len(Q) <= 11:
        RMsg += "\n"
        for x in range(len(Q)):
            if x == 0:
                continue
            RMsg += "\n" + str(x) + ". " + Q[x]['title']

    elif len(Q) > 10:
        RMsg += " There are `" + str(len(Q)) + "` songs in the queue.\nThe first ten are:\n"
        for x in range(len(Q)):
            if x == 0:
                continue
            if x > 11:
                break

            RMsg += "\n" + str(x) + ". " + Q[x]['title']

    await Bot.send_message(Msg.channel, RMsg)

## Create Command Statements

# General

createCommand("repeat", "Repeats what the user says after command.", Repeat, Permissions.Default)
createCommand("purge", "Try and purge x amount of messages.", Purge, Permissions.Administrator)
createCommand("commands", "List all commands.", ListCommands, Permissions.Default)
createCommand("osu", "Get osu data.", Osu, Permissions.Default)
createCommand("ping", "Pong!", Ping, Permissions.Default)

# Voice

createCommand("join", "Joins the voice channel the caller is currently in.", Join, Permissions.Default)
createCommand("leave", "Leaves the voice channel the bot is currently in.", Leave, Permissions.Default)
createCommand("play", "Plays the requested video in a voice channel, if found.", Play, Permissions.Administrator)
createCommand("search", "Adds requested video to queue to be played.", Search, Permissions.Default)
createCommand("playlist", "Adds songs from requested playlist to queue to be played.", Playlist, Permissions.Administrator)
createCommand("nowplaying", "Lists what song is currently playing on the bot.", Playing, Permissions.Default)
createCommand("skip", "Skips currently playing song.", Skip, Permissions.Administrator)
createCommand("clear", "Clears queue.", Clear, Permissions.Administrator)
createCommand("queue", "Details queue.", Queue, Permissions.Default)

## Main Bot Bit

bot = discord.Client()

@bot.event
async def MusicLoop():
    for Server in bot.servers:
        if len(AudioData[Server.id]["queue"]) > 1:
            if AudioData[Server.id]["voice"] != None:
                if AudioData[Server.id]["voice"].is_connected():
                    if AudioData[Server.id]["player"] == None or AudioData[Server.id]["player"].is_done():
                        del AudioData[Server.id]["queue"][0]
                        player = await AudioData[Server.id]["voice"].create_ytdl_player("http://www.youtube.com/watch?v="+AudioData[Server.id]["queue"][0]["id"])
                        player.volume = .25
                        player.start()

                        AudioData[Server.id]["player"] = player
        await asyncio.sleep(.1)


    schedule_coroutine(MusicLoop())


@bot.event
async def on_ready():
    time.sleep(.5)

    for Server in bot.servers:
        AudioData[Server.id] = {}
        AudioData[Server.id]["voice"] = None
        AudioData[Server.id]["player"] = None
        AudioData[Server.id]["queue"] = [None]

    schedule_coroutine(MusicLoop())

@bot.event
async def on_server_join(Server):
    AudioData[Server.id] = {}
    AudioData[Server.id]["voice"] = None
    AudioData[Server.id]["player"] = None
    AudioData[Server.id]["queue"] = [None]

@bot.event
async def on_server_remove(Server):
    del AudioData[Server.id]

@bot.event
async def on_message(Msg):
    if not Msg.author.bot: # Is author of msg a bot?
        if Msg.content.startswith(Prefix): # Did msg start with [defined prefix]?
            Msg.content = Msg.content[len(Prefix):]
            Data = Msg.content.split(" ")

            Cmd = Data[0]
            del Data[0]
            if Cmd.lower() in Commands: # Is the message a real command?
                Msg.content = Msg.content[len(Cmd)+1:]
                await Commands[Cmd].Do(bot, Msg, Data)

# bot.run('email', 'password')
bot.run(Token)
