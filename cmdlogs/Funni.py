import discord, datetime, random, string
from enum import Enum

class Funni:
    def __init__(self, data, sender, senderID, display, senderGroup, senderGUID):
        self.id:int = int(senderID)
        self.data = data
        self.timestamp:str = str(datetime.datetime.now())
        self.player = sender
        self.display = display
        self.group = int(senderGroup)
        self.joins:int = 0
        self.guid:list = [senderGUID]

    #refreshID = lambda self: random.choices(string.digits, k=16)
