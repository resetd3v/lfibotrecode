import discord, random
from discord.ext import commands

global monitors, sentHashes
monitors = {}
sentHashes = []

class Consts():
    def __init__(self):
        self.bot = commands.Bot(command_prefix=">", intents=discord.Intents.all(), help_command=None)
        self.tree = self.bot.tree
        self.enabled = False
        self.EXPANSEHEADER = {"User-Agent" : "Expanse, a Palo Alto Networks company, searches across the global IPv4 space multiple times per day to identify customers; presences on the Internet. If you would like to be excluded from our scans, please send IP addresses/domains to: scaninfo@paloaltonetworks.com"}
        self.LOGDOMAIN = "https://logs.pandahut.net/"
        self.LOGFILEURL = "PvpLogs/NA1Servers/Server19Rocket.log"
        self.LOGPATH = f"{__file__.replace('consts.py', '')}temp"
        self.LOGFILE = f"{self.LOGPATH}/latest.log"
        self.MISC = ["vault", "addshop", "buyfrom", "i", "stuck", "doortp", "mc", "trash", "connecting", "disconnecting"]
        self.STAFFONLY = ["DEBUG", "SERVER", "CONNECTING", "DISCONNECTING", "CHAT", "TP"]
        self.PROXYFILEPATH = f"{__file__.replace('consts.py', '')}proxies.txt"
        self.UALIST = [
            #"Mozlila/5.0 (Linux; Android 7.0; SM-G892A Bulid/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.107 Moblie Safari/537.36",
            "Expanse, a Palo Alto Networks company, searches across the global IPv4 space multiple times per day to identify customers; presences on the Internet. If you would like to be excluded from our scans, please send IP addresses/domains to: scaninfo@paloaltonetworks.com",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 11.6; rv:92.0) Gecko/20100101 Firefox/92.0",
            "Mozilla/5.0 (compatible; CensysInspect/1.1; +https://about.censys.io/)"
        ]

        self.headers = {"User-Agent" : self.getUA()}
        self.proxy = {"http" : self.getProxy()}

        self.LMAO = [709547527334002829, 1218944589994659850, 846641395581190155, 837703090345214022]
        self.TIMEZONE = -5

        #.*\[(.*)\]: \/(\S*) (.*)(\b|.*)
        #FINDSTAFFPATTERN = r".*\[(.*)\]: \/.* (.*)\b"
        # sender command target params
        self.COMMANDPATTERN = r"\[Command\].* \[(.*)\]: \/(\S*)( (\S*)( (.*)|\n)|\b)"

        # sender sendertargetid target targetid
        self.TPPATTERN = r".*>> (.*) \((\d*)\) - .* to (.*) \((\d*) at"
        # targetid name display groupid guid
        self.CONNECTINGPATTERN = r"Connecting: PlayerID: (\d*) Steam Name: (.*) Character name: (.*) Nick.* Group: (.*) Join GUID: (.*) C"
        self.DISCONNECTINGPATTERN = r"Disconnecting: PlayerID: (\d*) Steam Name: (.*) Character name: (.*) Nick.* Group: (.*) Session Length (.*)"
        # chattype sender chat/all
        self.CHATPATTERN = r"\[(Group|Global)\].* \[(.*)\]: (.*)"
        # target targetid
        self.APISPYPATTERN = r"API Spy Request Received: \((.*)\)\[(.*)\]"
        # actionid cmd targetid
        self.APIPATTERN = r"Dealt with Action (.*) with type \"(.*)\" for (\d*) on Pandahut"
        #"display" : "", "steam" : "", "id" : ""
        self.STAFFLIST = {
            "godly" : [{"display" : "Godly", "steam" : "Godly", "id" : "76561199183989090"}],
            "vampie" : [{"display" : "Vampie A.", "steam" : "Vampie", "id" : "76561198259451520"}],
            "fake vampie vampie c" : [{"display" : "ttaM", "steam" : "ItzJayJay=)", "id" : "76561199612445730"}],
            "jack" : [{"display" : "sdf", "steam" : "superb91", "id" : "76561198210222663"}],
            "dsod" : [{"display" : "dsod", "steam" : "dsod", "id" : "76561199078055336"}],
            "v0rtex" : [{"display" : "Fisherman v0rtex", "steam" : "v0rtex", "id" : "76561198844615074"}],
            "coil" : [{"display" : "call me a good boy", "steam" : "coil", "id" : "76561198301760563"}],
            #Scrypto
            "what" : [{"display" : "What", "steam" : "yes62844", "id" : "76561199496074995"}],
            "alastor" : [{"display" : "Ghost", "steam" : "Foxbro37", "id" : "76561198397021503"}],
            "silly" : [{"display" : "Silly Person :3", "steam" : "Angel_Abov3", "id" : "76561198856241780"}],
            "猫猫糕" : [{"display" : "猫猫糕", "steam" : "stacey", "id" : "76561198878832149"}],
            "Andre" : [{"display" : "drakos", "steam" : "Andre", "id" : "76561199531161985"}],
            "okbinoutube" : [{"display" : "okbinoutube", "steam" : "okbinoutube", "id" : "76561198843696538"}]
        }
        self.CHANNELS = {
            "debug" : 1256018442784608287,
            "staff" : {
                "vanish" : 1256023689368047680,
                "tp" : 1256023714525347890,
                "stats" : 1256037339398934528,
                "spy" : 1256057797154705550,
                "ban" : 1256125540268769311,
                "schat" : 1256036383538024469,
                "misc" : 1256454678582005810,
                "server" : 1256465626562822215,
                "msg" : 1256769061791072317,
                "chat" : 1257094197287321670,
                "connecting" : 1260393478186078219,
                "disconnecting" : 1257084697352077525,
                "api" : 1260415492368367738
            }
        }
        self.socket = None
        self.channel = ""
        self.loggedIN = False
        self.oldMSG = ""
    
    getUA = lambda self: random.choice(self.UALIST)
    getHeaders = lambda self: {"User-Agent" : self.getUA()}

    def getProxy(self):
        try:
            with open(self.PROXYFILEPATH, "r") as file:
                data = file.read()
            lines = data.split("\n")
            return random.choice(lines).replace("\n", "")
        except Exception as e: pass
    
    def getProxyFormatted(self):
        return ""
        #return f"http://127.0.0.1:8080"
        #return f"http://{self.getProxy()}"
    
    def getProxyDict(self):
        return {"User-Agent" : self.getProxy()}

    # def getUA(self):
    #     return random.choice(self.UALIST)

CONSTS = Consts()
