import asyncio
import discord
import json

from Bot import Permissions
from Bot import Youtube
from Bot import osuipy

Commands = {}
Token = ""
Prefix = ""
dPrefix = "!"
OsuCmds = False
OsuKey = None

DataFile = ".\\Bot\\Data.json"
AudioData = {}

# Helper Functions

def cls():
    print("\n"*150)

def testInt(D):
    try:
        int(D)
        return True
    except:
        return False

# Load Data

cls()

try:
    with open(DataFile, "r") as DF:
        Data = json.load(DF)
    
    Token = Data["BotConfig"]["Token"]
    Prefix = Data["BotConfig"]["Prefix"]
    OsuCmds = Data["BotConfig"]["OsuCmds"]
    OsuKey = Data["BotConfig"]["OsuKey"]
except:
    while len(Prefix.strip()) == 0:
        Prefix = input("Please enter bot prefix: ")
        cls()
    
    while len(Token.strip()) == 0:
        Token = input("Please enter bot token: ")
        cls()
    
    Data = {
        "BotConfig": {
            "Token": Token,
            "Prefix": Prefix,
            "OsuCmds": False,
            "OsuKey": None
        }
    }
    
    with open(DataFile, "w") as DF:
        json.dump(Data, DF, indent = 4)

# Create Command Stuffs

class _createCommand:
    def __init__(self, Call, Description, Function, Perms, PermMod):
        self.Call = Call
        self.Description = Description
        self.Function = Function
        self.Perms = Perms
        
        self.PermMod = PermMod
    
    async def Do(self, Bot, Msg, Args):
        if self.PermCheck(Msg):
            await self.Function(Bot, Msg, Args)
    
    def PermCheck(self, Msg):
        Perms = self.PermMod.PermsList(Msg.author.server_permissions)
        
        if self.Perms == self.PermMod.Default or self.Perms in Perms:
            return True
        return False

def createCommand(Call, Description, Function, Perms):
    Commands[Call] = __createCommand(Call, Description, Function, Perms)

# Command Functions

async def Repeat(Bot, Msg, Args):
    await Bot.send_message(Msg.channel, Msg)

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
            
            Limit += 1 # Users Messages
            
            await Bot.purge_from(Msg.channel, limit = Limit)
        else:
            await Bot.send_message(Msg.channel, Msg.author.mention + ", " + str(Limit) + " is not a number.")
    else: # Forgot to say how many? No problem.
        await tmp = Bot.send_message(Msg.channel, Msg.author.mention + ", How many messages do you want to try to delete?")
        await Ans = Bot.wait_for_message(timeout = 10, autor = Msg.author, channel = Msg.channel)
        
        await Bot.delete_message(tmp)
        if Ans != None:
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
                
                Limit += 2 # Users Messages

                await Bot.purge_from(Msg.channel, limit = Limit)
            else:
                await Bot.send_message(Msg.channel, Msg.author.mention + ", " + str(Limit) + " is not a number.")

async def ListCommands(Bot, Msg, Args):
    Cmds = "***Commands***\n"
    
    for x in Commands:
        Cmds += "\n**" + x + "** ```" + Commands[x].Description + "```"
    
    await Bot.send_message(Msg.channel, Msg.author.mention + ",\n" + Cmds)
     
async def Osu(Bot, Msg, Args):
    if OsuCmds:
        async def Best(Name, Mode):
            Best = osuipy.get_user_best(Name, Mode, 1)

            if Best != None:
                pass # Do stuff
            else:
                await Bot.send_message(Msg.channel, Msg.author.mention + ", Either user wasn't found, or they have not played this mode yet.")

        Type = "standard"
        Name = "WagwanPiftinWhatsYourBBMPinHitMeUp" # Idk, okie?
        Mode = osuipy.Modes.standard

        if Args > 0:
            Type = Args[0].lower()

        if Args == 3:
            Name = Args[1]
            Mode = Args[2].lower()

        if Mode == "standard":
            Mode = osuipy.Modes.standard()
        elif Mode == "mania":
            Mode = osuipy.Modes.mania()
        elif Mode == "ctb":
            Mode = osuipy.Modes.ctb()
        elif Mode == "taiko":
            Mode = osuipy.Modes.taiko()
        else:
            pass # Do stuff

        if Type = "best":
            await Best(Name, Mode)
        else:
            pass # Do stuff
    else:
        await Bot.send_message(Msg.channel, Msg.author.mention + ", Osu commands are currently disabled.")

async def Join(Bot, Msg, Args):
    if Msg.author.voice.voice_channel != None:
    
        try:
            AData = AudioData[Msg.server.id]
        except:
            AudioData[Msg.server.id] = {}
            AData = AudioData[Msg.server.id]

        try:
            voice = AData["voice"]
        except:
            AudioData[Msg.server.id]["voice"] = None
            voice = None
        
        if voice == None:
            voice = await client.join_voice_channel(Msg.author.voice.voice_channel)
        
        elif voice.is_connected():
            if len(voice.channel.voice_members) == 0:
                await voice.move_to(Msg.author.voice.voice_channel)
            else:
                await Bot.send_message(Msg.channel, Msg.author.mention + ", The bot is currently in another channel with users.")
    else:
        await Bot.send_message(Msg.channel, Msg.author.mention + ", You need to be in a voice channel to use this command.")

async def Leave(Bot, Msg, Args):
    try:
        AData = AudioData[Msg.server.id]
    except:
        AudioData[Msg.server.id] = {}
        AData = AudioData[Msg.server.id]

    try:
        voice = AData["voice"]
    except:
        AudioData[Msg.server.id]["voice"] = None
        voice = None
    
    if voice != None:
        if Msg.author.voice.voice_channel == voice.channel:
            if len(voice.channel.voice_members) == 1:
                await voice.disconnect()
            elif Permissions.Administrator in Permissions.PermList(Msg.author.server_permissions):
                await voice.disconnect()
            else:
                await Bot.send_message(Msg.channel, Msg.author.mention + ", You can not use this command when there are other people in the voice channel.")
        else:
            await Bot.send_message(Msg.channel, Msg.author.mention + ", You must be in the same channel as me to use this command.")
    else:
        await Bot.send_message(Msg.channel, Msg.author.mention + ", I'm not in a channel to leave!")
        
async def Play(Bot, Msg, Args):
    if Args > 0:
        q = Args.join(" ")
    else:
        await Bot.send_message(Msg.channel, Msg.author.mention + ", You need to tell me what song to play, to play one at all.")
        return
    
    await Join(Bot, Msg, Args)
    
    if AudioData[Msg.server.id]['voice'] != None and AudioData[Msg.server.id]['voice'].is_connected():
        Songs = Youtube.search_list(q)
        
        if len(Songs) == 1:
            player = AudioData[Msg.server.id]['player']

            if player != None:
                player.stop()

            player = await AudioData[Msg.server.id]['voice'].create_ytdl_player("https://www.youtube.com/watch?v="+Songs[0]["id"])
            player.volume = 0.5
            
            player.start()
            
            await Bot.send_message(Msg.channel, Msg.author.mention + ", **Now Playing**\n" + Songs[0]["title"] + "\n\n" + Songs[0]["thumbnail"] + "\nUploaded by " + Songs[0]["chantitle"])
        else:
            await Bot.send_message(Msg.channel, Msg.author.mention + ", Nothing found.")
    else:
        return
        
## Create Command Statements

# General

createCommand("repeat", "Repeats what the user says after command.", Repeat, Permissions.Default)
createCommand("purge", "Try and purge x amount of messages.", Purge, Permissions.Administrator)
createCommand("commands", "List all commands.", ListCommands, Permissions.Default)
createCommand("osu", "Get osu data.", Osu, Permissions.Default)

# Voice

createCommand("join", "Joins the voice channel the caller is currently in.", Join, Permissions.Default)
createCommand("leave", "Leaves the voice channel the bot is currently in.", Leave, Permissions.Default)
createCommand("play", "Plays the requested video in a voice channel, if found.", Play, Permissions.Administrator)

## Main Bot Bit

bot = discord.Client()

@client.event
async def on_message(Msg):
    if not Msg.author.bot: # Is author of msg a bot?
        if Msg.content.startswith(Prefix): # Did msg start with [defined prefix]?
            Msg.content = Msg.content[len(Prefix):]
            Data = Msg.content.split(" ")
            
            Cmd = Data[0]
            rem Data[0]
            if Cmd.lower() in Commands: # Is the message a real command?
                Msg.content = Mg.content[len(Cmd)+1:]
                Commands[Cmd].Do(bot, Msg, Data)

# await bot.run('email', 'password')
await bot.run(Token)
