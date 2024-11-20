import utils, re, hashlib, time as timeStats, discord
from cmdlogs.logs import logs
from enum import Enum
from utils import LOGGER, TIMEZONE, getTime, to_thread, getColor
from consts import CONSTS, monitors, sentHashes
from datetime import timezone, time, datetime, timedelta
from inspect import stack

from cmdlogs.Funni import Funni

DEFAULTTEXT = "staff \"{}\" has performed \"{}\" on \"{}\""

DEFAULTCOLOR = 0x0084d1
ORANGECOLOR = 0xffbf00
REDCOLOR = 0xff0000

class Action:
    def __init__(self, name:str, aliases:list = [], channel:tuple[str, str] = ("", "debug"), public:bool = True, text:str = DEFAULTTEXT, textArgs:list = [], autocomplete:bool = False, color:int = DEFAULTCOLOR):
        self.name = name
        self.aliases = aliases
        # yh fuck u, u think of better logic
        try: self.channel:int = CONSTS.CHANNELS[channel[0]][channel[1]]
        except: self.channel:int = CONSTS.CHANNELS[channel[1]]
        self.public = public
        self.text = text
        self.textArgs = textArgs
        self.autocomplete = autocomplete
        self.color = color

    def formatAction(self, *args):
        return self.text.format(*(args[0]))

    def check(self, data, sender, target=""):
        if self.name.lower() != "debug" and not (data == self.name.lower() or data in self.aliases): return False
        if self.name in CONSTS.STAFFONLY and not logs.isUserActive(target, self.autocomplete) and self.name.lower() != "connecting": return sender in str(CONSTS.STAFFLIST)
        return True


# todo add a "autocomplete" param bool for autocompleting target in logs eg /killfeed on target = on (autocompletes c"on"fusing)
class Actions:
    TP:Action = Action(name="TP", channel=("staff", "tp"), public=True, text="staff \"{}\" teleported to \"{}\"", textArgs=["sender", "target"], autocomplete=True, color=ORANGECOLOR)
    SC:Action = Action(name="SC", channel=("staff", "schat"), public=False, text="staff \"{}\" said \"{}\"", textArgs=["sender", "all"])
    STATS:Action = Action(name="STATS", aliases=["stat", "sstats", "pp"], channel=("staff", "stats"), public=True, text=DEFAULTTEXT, autocomplete=True, color=ORANGECOLOR)
    #aliases=["mod", "smod"]
    VANISH:Action = Action(name="VANISH", channel=("staff", "vanish"), public=False, text="staff \"{}\" went into vanish", textArgs=["sender"])
    SPY:Action = Action(name="SPY", channel=("staff", "spy"), public=False, text="staff \"{}\" has spied \"{}\"",  textArgs=("sender", "target"), autocomplete=True, color=REDCOLOR)
    APISPY:Action = Action(name="APISPY", channel=("staff", "spy"), public=False, text="api spied has been performed on \"{}\"",  textArgs=("target"), color=REDCOLOR)
    BAN:Action = Action(name="BAN", aliases=["globalban"], channel=("staff", "ban"), public=True, text="staff \"{}\" has {}banned \"{}\" get beamed bozo ur dtc for \"{}\"", textArgs=["sender", "global", "target", "reason"], color=REDCOLOR)
    UNBAN:Action = Action(name="UNBAN", channel=("staff", "ban"), public=True, text="staff \"{}\" has unbanned \"{}\"", textArgs=["sender", "target"])
    SERVER:Action = Action(name="SERVER", channel=("staff", "server"), public=False, text="staff \"{}\" has switched to server \"{}\" from \"19\"", textArgs=["sender", "target"])
    MSG:Action = Action(name="MSG", aliases=["pm"], channel=("staff", "msg"), public=False, text="player \"{}\" said \"{}\" to \"{}\"", autocomplete=True, textArgs=["sender", "params", "target"])
    REPLY:Action = Action(name="R", channel=("staff", "msg"), public=False, text="player \"{}\" said \"{}\"", autocomplete=True, textArgs=["sender", "all"])
    CHAT:Action = Action(name="CHAT", channel=("staff", "chat"), public=False, text="staff \"{}\" said \"{}\" in \"{}\" chat", textArgs=["sender", "chatMsg", "chatType"])
    CONNECTING:Action = Action(name="CONNECTING", channel=("staff", "connecting"), public=False, text="\"{}\" / \"{}\"  |  G: \"{}\" is connecting to server 19", textArgs=["sender", "senderid", "guid"])
    DISCONNECTING:Action = Action(name="DISCONNECTING", channel=("staff", "disconnecting"), public=False, text="staff \"{}\" disconnected from server 19 session length: {}", textArgs=["sender", "guid"])
    API:Action = Action(name="API", channel=("staff", "api"), public=False, text="api cmd \"{}\" ({}) performed on \"{}\"",  textArgs=("params", "target", "targetid"), color=REDCOLOR)
    DEBUG:Action = Action(name="DEBUG", channel=("", "debug"), public=False)

# class Actions(Enum):
#     TP = 0,
#     SC = 1,
#     STATS = 2,
#     VANISH = 3,
#     SPY = 4,
#     BAN = 5,
#     SERVER = 6,
#     DEBUG = 7

@to_thread
def staffParse(data: str, i: int, current_loop):
    #yw lxve <3 :3
    #data = "[2024-07-10 01:46:32.022 UTC] [Info] [Main] [Command] unk [I MISS HIM]: /msg unk LXVE IS ON THIS IS RESET"
    timer = timeStats.time()
    if current_loop == 1 and i == 0:
        LOGGER.log(stack()[0][3], f"CAUGHT UP TO LATEST {len(sentHashes)}", LOGGER.LogType.INFO)

    data = data.replace("//", "/")
    try:
        args = None
        target = ""
        targetID = ""
        # double check y not
        dataHash = hashlib.md5(data.encode("utf")).hexdigest()
        if dataHash in sentHashes: return (False, "exist")

        #timeThing = datetime.now(timezone.utc).time()
        #if time(8, 0) < timeThing < time(8, 5): sentHashes.clear()

        # add this logic in check and params
        if "- Teleported to " in data:
            regexResp = re.search(CONSTS.TPPATTERN, data, re.IGNORECASE)
            if regexResp == None: return (False, "tpPattern?")
            command = "tp"
            sender = regexResp.group(1)
            #if sender not in str(STAFFLIST): return (False, "notStaff")
            target = regexResp.group(3)
            targetID = regexResp.group(4)
            args = (sender, target)
        elif "Connecting: PlayerID:" in data or "Disconnecting: PlayerID:" in data:
            regexResp = re.search(CONSTS.CONNECTINGPATTERN, data, re.IGNORECASE)
            if regexResp == None: regexResp = re.search(CONSTS.DISCONNECTINGPATTERN, data, re.IGNORECASE)
            if regexResp == None: return (False, "connectingPattern")
            command = "connecting" if "Connecting: PlayerID:" in data else "disconnecting"
            sender = regexResp.group(2)
            senderID = regexResp.group(1)
            senderDisplay = regexResp.group(3)
            senderGroup = regexResp.group(4)
            senderGUID = regexResp.group(5)
            #if senderID not in str(CONSTS.STAFFLIST): return (False, "notStaff")
            #args = [sender, senderID, senderGUID, senderGroup]
            if command == "connecting":
                funni = Funni(data, sender, senderID, senderDisplay, senderGroup, senderGUID)
                logs.add(funni)
        elif "[Command]" in data:
            regexResp = re.search(CONSTS.COMMANDPATTERN, data, re.IGNORECASE)
            if regexResp == None: return (False, "commandPattern")
            command = regexResp.group(2).replace("/", "")
            sender = regexResp.group(1)
            # comment out if everyone but remember to check on debug or everything not just cmds will print
            #if sender not in str(CONSTS.STAFFLIST): return (False, "notStaff")
            target = regexResp.group(4)
            params = regexResp.group(6) if regexResp.group(5) != "\n" else ""
            #args = (sender, target, params)
        elif "[Global]" in data or "[Group]" in data:
            regexResp = re.search(CONSTS.CHATPATTERN, data, re.IGNORECASE)
            if regexResp == None: return (False, "commandPattern")
            command = "chat"
            sender = regexResp.group(2)
            chatType = regexResp.group(1)
            chatMsg = regexResp.group(3)
            args = [sender, chatMsg, chatType.upper()]

        elif "API Spy Request" in data:
            regexResp = re.search(CONSTS.APISPYPATTERN, data, re.IGNORECASE)
            if regexResp == None: return (False, "apiSpyPattern")
            command = "apispy"
            sender = "api"
            target = regexResp.group(1)
            targetID = regexResp.group(2)
            args = [target]
        # actionid cmd targetid
        #self.APIPATTERN = r"Dealt with Action (.*) with type \"(.*)\" for (\d*) on Pandahut"
        #Dealt with Action 7ba578c3a0a24dc2aae3e885d04da665 with type "Spy @" for 76561199732713785 on Pandahut #19 [Unturnov 1.0 Remastered] [US-East] at 7/10/2024 1:42:23 AM
        elif "Dealt with Action" in data:
            regexResp = re.search(CONSTS.APIPATTERN, data, re.IGNORECASE)
            if regexResp == None: return (False, "apiPattern")
            command = "api"
            sender = "api"
            target = regexResp.group(1)
            params = regexResp.group(2)
            targetID = regexResp.group(3)
            args = [params, target, targetID]
        else: return (False, "noPattern")
        
        sentHashes.append(dataHash)
        if current_loop == 0: #and command != "connecting":
            return (False, "first")
        
        if "/tp" in data: return (False, "alternative")
        timestamp, obf = getTime(data)

        #action = Actions.DEBUG
        action = None
        channel = CONSTS.CHANNELS["debug"]
        public = True
        text = DEFAULTTEXT

        for action in vars(Actions).values():
            if type(action) != Action: continue
            resp = action.check(command.lower(), sender, target if target else "")
            if resp:
                action = action
                break
        if not action: return (False, "notStaff?")
        if action.text == DEFAULTTEXT: args = [sender, action.name, target]
        elif not args:
            args = []
            for arg in action.textArgs:
                match arg:
                    case "sender": arg = sender
                    case "sender": arg = sender
                    case "target": arg = target.replace('"', '')
                    case "params": arg = params
                    case "all": arg = re.search(r"\/\w* (.*)", data, re.IGNORECASE).group(1).replace("\n", "")
                    #arg = data.split("/sc ")[-1].replace("\n", "")
                    case "global": arg = "global-" if "global" in data else ""
                    case "reason": arg = re.search(r'\/.* (".*"|.*) \"(.*)\"', data, re.IGNORECASE).group(2).replace('"', '')
                    case "senderid": arg = senderID
                    case "sendergroup": arg = senderGroup
                    case "guid": arg = senderGUID
                args.append(arg)

        if action == Actions.STATS:
            if not logs.isUserActive(target, action.autocomplete) and sender not in CONSTS.STAFFONLY: return (False, "activeOnly")

        text = action.formatAction(args)

        # if action.name in CONSTS.STAFFONLY:
        #     if sender not in str(CONSTS.STAFFLIST): return (False, "notStaff")
        
        public = action.public
        channel = action.channel
        if command.lower() in CONSTS.MISC:
            public = False
            if command.lower() != "connecting" and command.lower() != "disconnecting": channel = CONSTS.CHANNELS["staff"]["misc"]
        
        ##text = f"staff {sender} has performed {action.name} on {target}" if not text else text
        #ext = action.text if not text else text
        #text = action.text.format(str(sender), action.name, str(target)) if text == DEFAULTTEXT else text

        #await staffLog(channel, sender, target, text, data, action, timestamp, obf)
        return (True, channel, sender, target, targetID, text, data, action, timestamp, obf, public, timeStats.time() - timer, command)
    except Exception as e:
        LOGGER.log(stack()[0][3], f"error parsing {e} | {action.__dict__} | {data}", LOGGER.LogType.ERROR)
        return (False, "parser")

async def staffLog(success, channel, sender:str, target:str, targetID:str, text:str, data:str, action:Action, timestamp, obf:str, public, timer, command:str):
    try:
        # if action.public != public:
        #     print(f"RIP EVCERYTHING IS GOING TO SHIT {action.name}")
        #     return
        
        data, sender = data.replace("\n", ""), sender.replace("\n", "")
        if target != None: target.replace("\n", "").replace('"', '')

        fake = command.lower() in CONSTS.MISC and (not ((command.lower() == "connecting" or command.lower() == "disconnecting") and sender in str(CONSTS.STAFFLIST)))

        channel = CONSTS.bot.get_channel(channel)
        embed = discord.Embed(title=f"{action.name}", color=action.color)
        embed.description = text if action != Actions.DEBUG else data
        embed.set_footer(text=f"Action performed at {timestamp} EST by {sender} (timestamp may not be accurate/within 10 seconds) {obf} {timer} {public}")

        target = targetID if targetID else target
        logs.getActive()
        doMention = len(target) > 2 and logs.isUserActive(target, action.autocomplete)
        if doMention: mention = logs.getMention(target, action.autocomplete)

        if not fake: await channel.send(content=f"<@!{mention}>" if doMention else "", embed=embed)

        if (command.lower() == "connecting" or command.lower() == "disconnecting") and sender not in str(CONSTS.STAFFLIST): return
        # timestamp
        encrypted, key = int(obf.replace("\n", "").split(" ")[0]), int(obf.replace("\n", "").split(" ")[1])
        unencrypted = encrypted ^ (key ^ 1337) ^ 420691337
        LOGGER.log(stack()[0][3], f"{(datetime.now(timezone.utc) - timedelta(hours=TIMEZONE)).strftime('%H:%M:%S')}/{timestamp}({unencrypted}) {'fake' if fake else ''}logged {action.name} in {channel}{' mentioned ' + str(mention) if doMention else ''}: {data}", LOGGER.LogType.DEBUG, 1)
    except: pass



"""
        # for loop over all actions and aliases call function to format with params
        match command.lower():
            case "chat":
                action = Actions.CHAT
                public = False
                text = action.text.format(sender, chatMsg, chatType)
            case "connecting":
                action = Actions.CONNECTING
                public = False
                text = action.text.format(sender)
            case "disconnecting":
                action = Actions.DISCONNECTING
                public = False
                text = action.text.format(sender)
            case "tp":
                action = Actions.TP
                target = targetID
                text = action.text.format(sender, target)
            case "sc":
                action = Actions.SC
                public = False
                # channel = CONSTS.CHANNELS["staff"]["chat"]
                text = action.text.format(sender, data.split('/sc ')[-1].replace("\n", ""))
                ##text = f"staff {sender} said {data.split('/sc ')[-1]}"
            case "spy":
                action = Actions.SPY
                public = False
                # channel = CONSTS.CHANNELS["staff"]["spy"]
                text = action.text.format(sender, target)
            case "vanish":
                action = Actions.VANISH
                public = False
            #     channel = CONSTS.CHANNELS["staff"]["vanish"]
                text = action.text.format(sender)
            case "mod":
                action = Actions.VANISH
                public = False
                text = action.text.format(sender)
            case "smod":
                action = Actions.VANISH
                public = False
                text = action.text.format(sender)
            # add normal player category and only print stats/other commands on monitored ids not just ping
            case "stat":
                action = Actions.STATS
            case "stats":
                action = Actions.STATS
            case "sstats":
                action = Actions.STATS
            case "ban":
                action = Actions.BAN
                reason = re.search(r'/ban (".*"|.*) \"(.*)\"', data, re.IGNORECASE)
                # length = data.split(' ')[-1] # {reason if reason != 0 else 'perma'}
                ##text = f"staff {sender} has banned {target} get beamed bozo ur dtc for {reason}"
                text = action.text.format(sender, target, reason.group(2))
            case "server":
                action = Actions.SERVER
                public = False
                ##text = f"staff {sender} has switched to server {target}"
                text = action.text.format(sender, target)
            case "msg":
                action = Actions.MSG
                public = False
                text = action.text.format(sender, params, target)
            case "pm":
                action = Actions.MSG
                public = False
                text = action.text.format(sender, params, target)
            case "r":
                action = Actions.MSG
                public = False
                text = action.text.format(sender, data.split("/r ")[-1], "N/A").replace("\n", "")

            case _: public = False
"""


"""
#lmao = [CONSTS.bot.get_guild(1256018198483046514).get_member(740952396259262486), CONSTS.bot.get_guild(1256018198483046514).get_member(670266215528398858)]
lmao = [CONSTS.bot.get_guild(1256018198483046514).get_member(709547527334002829)]
embed = discord.Embed(title=f"no", color=0x0084d1)
embed.description = "we have reason to believe u guys are federal so u have been revoked access to the #1 developer's cheat and funni exploit server"
embed.set_footer(text="cry to staff if u want prove ur federal")
for member in lmao:
    member.send(embed=embed)
"""



# match command.lower():
#             case "tp":
#                 action = Actions.TP
#             #     channel = CONSTS.CHANNELS["staff"]["tp"]
#                 text = f"staff {sender} teleported to {target}"
#             case "sc":
#                 action = Actions.SC
#                 public = False
#                 channel = CONSTS.CHANNELS["staff"]["chat"]
#                 text = f"staff {sender} said {data.split('/sc ')[-1]}"
#             case "spy":
#                 action = Actions.SPY
#                 public = False
#                 channel = CONSTS.CHANNELS["staff"]["spy"]
#             case "vanish":
#                 action = Actions.VANISH
#             #     channel = CONSTS.CHANNELS["staff"]["vanish"]
#                 text = f"staff {sender} went into vanish"
#             # add normal player category and only print stats/other commands on monitored ids not just ping
#             case "stats":
#                 action = Actions.STATS
#             #     channel = CONSTS.CHANNELS["staff"]["stats"]
#             case "sstats":
#                 action = Actions.STATS
#             #     channel = CONSTS.CHANNELS["staff"]["stats"]
#             case "ban":
#                 action = Actions.BAN
#             #     channel = CONSTS.CHANNELS["staff"]["ban"]
#                 reason = re.search(r'\/ban (.*) \"(.*)\"', data, re.IGNORECASE).group(2)
#                 # length = data.split(' ')[-1] # {reason if reason != 0 else 'perma'}
#                 text = f"staff {sender} has banned {target} get beamed bozo ur dtc for {reason}"
#             case "server":
#                 action = Actions.SERVER
#                 channel = CONSTS.CHANNELS["staff"]["server"]
#                 text = f"staff {sender} has switched to server {target}"
#             case "vault":
#                 channel = CONSTS.CHANNELS["staff"]["vault"]

#             case _:
#                 if sender not in str(CONSTS.STAFFLIST): return (False, "notStaff")
#                 public = False
