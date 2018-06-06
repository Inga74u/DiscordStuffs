import asyncio
import discord

Commands = {}
Token = None
Prefix = ""

class _createCommand:
    def __init__(self, Call, Description, Function, Perms):
        self.Call = Call
        self.Description = Description
        self.Function = Function
        self.Perms = Perms
    
    async def Do(self, Bot, Msg, Args):
        if self.PermCheck(Msg):
            await self.Function(Bot, Msg, Args)
    
    def PermCheck(self, Msg):
        Perms = Msg.author.server_permissions
        
        if Perms.administrator or Perms >= self.Perms:
            return True
        return False

def createCommand(Call, Description, Function, Perms):
    Commands[Call] = __createCommand(Call, Description, Function, Perms)

# Command Functions

async def Repeat(Bot, Msg, Args):
    await Bot.send_message(Msg.channel, Msg)

# Create Command Statements

createCommand("repeat", "Repeats what the user says after command.", Repeat, None)

# Main Bot Bit

bot = discord.Client()

@client.event
async def on_message(Msg):
    if not Msg.author.bot: # Is author of msg a bot?
        if Msg.content.startswith(Prefix): # Did msg start with [defined prefix]?
            Msg.content = Msg.content[len(Prefix):]
            Data = Msg.content.split(" ")
            
            Cmd = Data[0]
            rem Data[0]
            if Cmd in Commands: # Is the message a real command?
                Commands[Cmd].Do(bot, Msg, Data)

# await bot.run('email', 'password')
await bot.run(Token)
