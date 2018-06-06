import asyncio
import discord

Commands = {}

class _createCommand:
    def __init__(self, Call, Description, Function, Perms):
        self.Call = Call
        self.Description = Description
        self.Function = Function
        self.Perms = Perms
    
    async def Do(self, Bot, Msg):
        if self.PermCheck(Msg):
            await self.Function(Bot, Msg)
    
    def PermCheck(self, Msg):
        Perms = Msg.author.server_permissions
        
        if Perms.administrator or Perms >= self.Perms:
            return True
        return False

def createCommand(Call, Description, Function, Perms):
    return __createCommand(Call, Description, Function, Perms)
