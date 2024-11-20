import discord, datetime, random, string
from enum import Enum

class MonitorRequest():
    class MonitorType(Enum):
        ADD = 0,
        DELETE = 1

    def __init__(self, interaction:discord.Interaction, action:MonitorType, mention:discord.user.User, user:int, display:str):
        self.id:int = interaction.id
        self.active = True
        #self.interaction = interaction
        self.author:dict[str: int] = {"name" : interaction.user.name, "id" : interaction.user.id}
        self.mention:dict[str: int] = {"name" : mention.name, "id" : mention.id}
        self.timestamp:str = str(datetime.datetime.now())
        self.action:self.MonitorType = action.name
        self.user:int = int(user)
        self.display = display

    #refreshID = lambda self: random.choices(string.digits, k=16)
