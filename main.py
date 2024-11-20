import discord, os, re, aiohttp, time as timeStats, requests, threading, socket, asyncio #steam
#from datetime import datetime, timezone, time, timedelta
#sys.stdout = open(f"bruh\\{datetime.now().strftime('%H-%M-%S_%d-%m')}.log", 'a')
import retrieve, monitor
from consts import CONSTS
from utils import LOGGER
from discord.ext import commands, tasks
from inspect import stack
from cmdlogs.logs import logs
from cmdlogs.MonitorRequest import MonitorRequest
from random import randint

@CONSTS.bot.event
async def on_ready():
    print(f"Bot logged in as {CONSTS.bot.user.name}")
    activityType = discord.Streaming(platform="Twitch", twitch_name="cum", name="path traversal to rce lmao", game="confusing.wtf", url="https://twitch.tv/beamer")
    await CONSTS.bot.change_presence(activity=activityType)
    await CONSTS.bot.tree.sync()
    retrieveLog.start()
    #d = setup()
    
    #task = tasks.loop(seconds=1)(lmao2)
    #task.start(task)#*d)
    
    #threading.Thread(target=asyncio.run, args=(lmao2(),)).start()
    #threading.Thread(target=lmao).start()

# add back group shit list and the join idea per join group guid display session length
@CONSTS.bot.tree.command(name="status", description="uuhhh uh uhhhhh i wonder")
async def status(interaction: discord.Interaction):
    embed = discord.Embed(title="is he getting active doe", color=0x0084d1 if CONSTS.enabled else 0xFF0000)
    embed.description = f"```robert is {'GETTING ACTIVE $$$' if CONSTS.enabled else 'NOT getting active (bad robert)'}```"
    await interaction.response.send_message(embed=embed)

@CONSTS.bot.tree.command(name="start", description="robert get active lazy piece of shit")
async def start(interaction: discord.Interaction):
    CONSTS.enabled = True
    embed = discord.Embed(title="Start monit", color=0x0084d1)
    embed.description = "```robert is GETTING ACTIVE $$$```"
    await interaction.response.send_message(embed=embed)

@CONSTS.bot.tree.command(name="stop", description="robert go eeper")
async def stop(interaction: discord.Interaction):
    CONSTS.enabled = False
    embed = discord.Embed(title="Stop monit", color=0xFF)
    embed.description = f"```robert go eeper now {'z' * randint(1,6)}```"
    await interaction.response.send_message(embed=embed)

@tasks.loop(seconds=15)
async def retrieveLog():
    if not CONSTS.enabled: return
    await retrieve.retrieveLog(retrieveLog)


@CONSTS.bot.tree.command(name="update", description="retrieves new packets")
async def update(interaction: discord.Interaction):
    if interaction.user.id != 709547527334002829:
        await interaction.response.send_message("no.")
        return
    retrieveLog.restart()
    await interaction.response.send_message(".")
    #os.system('cd /home/reset/funni/output; wget --user-agent "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0" -e robots=off -r -np --page-requisites -nc https://logs.pandahut.net/PvpLogs/ExtLogs/')


@CONSTS.bot.tree.command(name="debug", description="no")
async def debug(interaction:discord.Interaction, level:int, ephemeral:bool = False):
    if interaction.user.id != 709547527334002829:
        interaction.response.send_message("no.")
    temp = LOGGER.level
    LOGGER.level = level
    await interaction.response.send_message(f"{temp} -> {LOGGER.level}", ephemeral=ephemeral)
    LOGGER.log(stack()[0][3], f"changed debug level from {temp} -> {LOGGER.level}", LOGGER.LogType.INFO)


@CONSTS.bot.tree.command(name="monitor", description="monitors steamid for actions performed (10 max)")
async def monitorUser(interaction:discord.Interaction, user:str, ephemeral:bool = False, mentionuser:discord.User = None, display:str = ""):
    await monitor.monitor(interaction, user, ephemeral, mentionuser, display)


@CONSTS.bot.tree.command(name="cancel", description="cancels a monitor task on the specified steamid")
async def cancelMonitor(interaction:discord.Interaction, user:str, ephemeral:bool = False):
    await monitor.cancelMonitor(interaction, user, ephemeral)


@CONSTS.bot.tree.command(name="list", description="lists all active monitors")
async def listMonitors(interaction:discord.Interaction, ephemeral:bool = True):
    await monitor.listMonitors(interaction, ephemeral)

# @CONSTS.bot.tree.command(name="username", description="sets ingame username")
# async def listMonitors(interaction:discord.Interaction, ephemeral:bool = True):
#     await monitor.listMonitors(interaction, ephemeral)

@CONSTS.bot.tree.command(name="server", description="funni")
async def server(interaction:discord.Interaction, serverinput:str, ephemeral:bool = True):
    if requests.get("https://api.pandahut.net/api/ServerProxy/PublicList", headers=CONSTS.EXPANSEHEADER, proxies=CONSTS.getProxyDict(), timeout=30).status_code != 200: return
    servers = [server for server in requests.get("https://api.pandahut.net/api/ServerProxy/PublicList", headers=CONSTS.EXPANSEHEADER, proxies=CONSTS.getProxyDict(), timeout=30).json()]
    server = None
    for server in servers:
        if serverinput not in server["IP"].split(".")[0] or "ENTRY" in server["ServerName"]: continue
        server = server
        break
    
    resp = requests.get(f"https://api.pandahut.net/api/ServerProxy/PublicServerStatus/{server['_id']}", headers=CONSTS.EXPANSEHEADER, proxies=CONSTS.getProxyDict(), timeout=30)
    if resp.status_code != 200: return
    server = resp.json()
    embed = discord.Embed(title=f"Server {serverinput}", color=0x0084d1)
    # embed.description = "```\n"
    # for key, value in server.items():
    #     if key.lower() == "players": value = len(server["Players"])
    #     embed.description += f"{key} -> {value}\n"
    # embed.description += "\n```"
    for key, value in server.items():
        if key.lower() == "players": value = len(server["Players"])
        embed.add_field(name=f"```{key}```", value=f"```{value}```", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

@CONSTS.bot.tree.command(name="players", description="funni")
async def players(interaction:discord.Interaction, serverinput:str, ephemeral:bool = True):
    if requests.get("https://api.pandahut.net/api/ServerProxy/PublicList", headers=CONSTS.EXPANSEHEADER, proxies=CONSTS.getProxyDict(), timeout=30).status_code != 200: return
    servers = [server for server in requests.get("https://api.pandahut.net/api/ServerProxy/PublicList", headers=CONSTS.EXPANSEHEADER, proxies=CONSTS.getProxyDict(), timeout=30).json()]
    server = None
    for server in servers:
        if serverinput not in server["IP"].split(".")[0] or "ENTRY" in server["ServerName"]: continue
        server = server
        break
    
    resp = requests.get(f"https://api.pandahut.net/api/ServerProxy/PublicServerStatus/{server['_id']}", headers=CONSTS.EXPANSEHEADER, proxies=CONSTS.getProxyDict(), timeout=30)
    if resp.status_code != 200: return
    server = resp.json()
    truncated = False
    # if len(str(server["Players"])) > 4096:
    #     original = len(str(server["Players"]))
    #     truncated = True
    embed = discord.Embed(title=f"Server {serverinput}", color=0x0084d1)
    embed.description = "```\n"
    for player in server["Players"]:
        temp = f"{player['DisplayName']} -> {player}\n\n"

        if len(embed.description + temp + "\n```") > 4096:
            original = len(str(server["Players"]))
            truncated = True
            break

        embed.description += temp
    embed.description += "\n```"
    embed.set_footer(text=f"Response truncated from {original} to 4096 to stop discord bitching (not all players included cuz of discord)" if truncated else "")
    # for player in server["Players"]:
    #     embed.add_field(name=f"```{player['DisplayName']}```", value=f"```{player}```")
    await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

@CONSTS.bot.tree.command(name="player", description="funni")
async def player(interaction:discord.Interaction, serverinput:str, playerinput:str, ephemeral:bool = True):
    if requests.get("https://api.pandahut.net/api/ServerProxy/PublicList", headers=CONSTS.EXPANSEHEADER, timeout=30).status_code != 200: return
    servers = [server for server in requests.get("https://api.pandahut.net/api/ServerProxy/PublicList", headers=CONSTS.EXPANSEHEADER, proxies=CONSTS.getProxyDict(), timeout=30).json()]
    server = None
    for server in servers:
        if serverinput not in server["IP"].split(".")[0] or "ENTRY" in server["ServerName"]: continue
        server = server
        break
    
    resp = requests.get(f"https://api.pandahut.net/api/ServerProxy/PublicServerStatus/{server['_id']}", headers=CONSTS.EXPANSEHEADER, proxies=CONSTS.getProxyDict(), timeout=30)
    if resp.status_code != 200: return
    server = resp.json()
    truncated = False
    # if len(str(server["Players"])) > 4096:
    #     original = len(str(server["Players"]))
    #     truncated = True
    embed = discord.Embed(title=f"Server {serverinput}", color=0x0084d1)
    embed.description = "```\n"
    for player in server["Players"]:
        if playerinput not in player['DisplayName']: continue
        temp = f"{player['DisplayName']} -> {player}\n\n"

        if len(embed.description + temp + "\n```") > 4096:
            original = len(str(server["Players"]))
            truncated = True
            break

        embed.description += temp
    embed.description += "\n```"
    embed.set_footer(text=f"Response truncated from {original} to 4096 to stop discord bitching (not all players included cuz of discord)" if truncated else "")
    # for player in server["Players"]:
    #     embed.add_field(name=f"```{player['DisplayName']}```", value=f"```{player}```")
    await interaction.response.send_message(embed=embed, ephemeral=ephemeral)


@CONSTS.bot.tree.command(name="stats", description="lists all active monitors")
async def stats(interaction:discord.Interaction, ephemeral:bool = True):
    timer = timeStats.time()
    #stream=True,
    #resp = requests.get(f"{LOGDOMAIN}{LOGFILEURL}", headers={"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"}, timeout=30)
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{CONSTS.LOGDOMAIN}{CONSTS.LOGFILEURL}", headers=CONSTS.getHeaders(), proxy=CONSTS.getProxyFormatted(), timeout=30) as resp:
            if resp.status != 200: return

            with open(CONSTS.LOGFILE, "wb") as file:
                file.truncate(0)
                file.write(await resp.content.read())
                file.seek(0, os.SEEK_END)
                size = file.tell()

    embed = discord.Embed(title="Stats", color=0x0084d1)
    embed.add_field(name="```REQ```", value=f"```{size} | {timeStats.time() - timer}```")
    #embed.add_field(name="```PARSE```", value=f"```{size} | {timeStats.time() - timer}```")
    await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

def lmao():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(lmao2())
    loop.close()

def setup():
    CONSTS.loggedIN = False
    channel = CONSTS.bot.get_channel(1262774550538485812)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("proxy.m4sportelo.hu", 888))
        s.send("669787761736865726500".encode())
        CONSTS.socket, CONSTS.channel = s, channel
        return (s, channel)
    except Exception as e:
        s.close()
        print(f"[SOCKET] cum: {e}")
        return (False, "")


async def lmao2(task: tasks.Loop):#s: socket.socket, channel: discord.TextChannel):
    s, channel = CONSTS.socket, CONSTS.channel
    if task.current_loop == 0: s, channel = setup()
    try:
        if s == False: raise BufferError
        await asyncio.sleep(5)
        data = s.recv(8192, socket.MSG_PEEK)
        if len(data) == 0: return
        data = data.decode()
        #if CONSTS.loggedIN: data = data.replace("Password :\x1b[0;38;2;0;0;0m ", "Password :\x1b[0;38;2;0;0;0m \n")
        temp = data
        data = data.replace(CONSTS.oldMSG, "")
        lmao3 = data
        #lmao3 = data.split("\n")[-1]
        if "Username" in lmao3 and "Password" not in lmao3:
            s.send("BOT".encode())
            print("[SOCKET] logged username")
        elif "Password" in lmao3 and "PING" not in lmao3: #and not CONSTS.loggedIN:
            CONSTS.loggedIN = True
            s.send("niggerasd".encode())
            print("[SOCKET] logged in")
        elif "PING" in data:#''.join(char for i, char in enumerate(lmao3) if i < 4):
            s.send("PONG".encode())
            # print("[SOCKET] sent pong")
        elif lmao3 != None and lmao3 != "" and CONSTS.loggedIN:
            await channel.send(content=lmao3)
        CONSTS.oldMSG = temp
    except Exception as e:
        print(f"[SOCKET] cum2: {e}")
        await asyncio.sleep(2)
        s, channel = setup()








thing = [2420749, 2420756, 2420745, 2420849, 2420750, 2420778, 2420737, 2420851, 2420750, 2420794, 2420761, 2420791, 2420751, 2420756, 2420779, 2420849, 2420750, 2420778, 2420741, 2420849, 2420749, 2420756, 2420749, 2420794, 2420750, 2420775, 2420846, 2420743, 2420742, 2420772, 2420845, 2420791, 2420761, 2420846, 2420738, 2420771, 2420742, 2420747, 2420787, 2420757, 2420780, 2420771, 2420754, 2420853, 2420775, 2420845, 2420756, 2420749, 2420776, 2420744, 2420756, 2420776, 2420754, 2420748, 2420741, 2420780, 2420771, 2420753, 2420749, 2420776, 2420778, 2420792, 2420750, 2420789, 2420759, 2420853, 2420777, 2420748, 2420791, 2420760, 2420849, 2420779]
token = "".join(chr(char ^ 1513 * 40 ** 2) for char in thing)
CONSTS.bot.run(token)


"""
if "- Teleported to " in data:
        regexResp = re.search(TPPATTERN, data, re.IGNORECASE)
        if regexResp == None: return (False, "tpPattern?")
        sender = regexResp.group(1)
        target = regexResp.group(3)
    else:
        regexResp = re.search(FINDSTAFFPATTERN, data, re.IGNORECASE)
        if regexResp == None: return (False, "staffPattern")
        sender = regexResp.group(1)
        target = regexResp.group(2).split(" ")[0]

    #if "/tp" in data: action = Actions.TP
    if "- Teleported to " in data: Actions.TP
    elif "/vanish" in data: action = Actions.VANISH
    elif "/stats" in data or "/sstats" in data: action = Actions.STATS
    elif "/sc" in data: action = Actions.SC
    elif "/spy" in data: action = Actions.SPY
    elif "/ban" in data: action = Actions.BAN

    match action:
        # case Actions.TP:
        #     channel = CHANNELS["staff"]["tp"]
        case Actions.SC:
            channel = CHANNELS["staff"]["chats"]
            text = f"staff {sender} said {data.split('/sc ')[-1]}"
        case Actions.SPY:
            channel = CHANNELS["staff"]["spy"]
        # case Actions.VANISH:
        #     channel = CHANNELS["staff"]["vanish"]
        #     text = f"staff {sender} went into vanish"
        # case Actions.STATS:
        #     channel = CHANNELS["staff"]["stats"]
        # case Actions.BAN:
        #     channel = CHANNELS["staff"]["bans"]
        #     reason = re.search(r'/ban (.*) \"(.*)\"', data, re.IGNORECASE).group(2)
        #     # length = data.split(' ')[-1] # {reason if reason != 0 else 'perma'}
        #     text = f"staff {sender} has banned {target} get beamed bozo ur dtc for {reason}"
        case _:
            channel = CHANNELS["debug"]
"""
