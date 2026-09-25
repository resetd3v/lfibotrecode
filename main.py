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
    if not CONSTS.bot.user: return
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
        await interaction.response.send_message("no.")
        return
    temp = LOGGER.level
    LOGGER.level = level
    await interaction.response.send_message(f"{temp} -> {LOGGER.level}", ephemeral=ephemeral)
    LOGGER.log(stack()[0][3], f"changed debug level from {temp} -> {LOGGER.level}", LOGGER.LogType.INFO)


@CONSTS.bot.tree.command(name="monitor", description="monitors steamid for actions performed (10 max)")
async def monitorUser(interaction:discord.Interaction, user:str, ephemeral:bool = False, mentionuser:discord.User|None = None, display:str = ""):
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
    if requests.get("https://api.pandahut.net/api/ServerProxy/PublicList", headers=CONSTS.getHeaders(), proxies=CONSTS.getProxyDict(), timeout=30).status_code != 200: return
    servers = [server for server in requests.get("https://api.pandahut.net/api/ServerProxy/PublicList", headers=CONSTS.getHeaders(), proxies=CONSTS.getProxyDict(), timeout=30).json()]
    server = None
    for server in servers:
        if serverinput not in server["IP"].split(".")[0] or "ENTRY" in server["ServerName"]: continue
        server = server
        break
    
    if not server: return
    resp = requests.get(f"https://api.pandahut.net/api/ServerProxy/PublicServerStatus/{server['_id']}", headers=CONSTS.getHeaders(), proxies=CONSTS.getProxyDict(), timeout=30)
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
    if requests.get("https://api.pandahut.net/api/ServerProxy/PublicList", headers=CONSTS.getHeaders(), proxies=CONSTS.getProxyDict(), timeout=30).status_code != 200: return
    servers = [server for server in requests.get("https://api.pandahut.net/api/ServerProxy/PublicList", headers=CONSTS.getHeaders(), proxies=CONSTS.getProxyDict(), timeout=30).json()]
    server = None
    for server in servers:
        if serverinput not in server["IP"].split(".")[0] or "ENTRY" in server["ServerName"]: continue
        server = server
        break
    
    if not server: return
    resp = requests.get(f"https://api.pandahut.net/api/ServerProxy/PublicServerStatus/{server['_id']}", headers=CONSTS.getHeaders(), proxies=CONSTS.getProxyDict(), timeout=30)
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
    if requests.get("https://api.pandahut.net/api/ServerProxy/PublicList", headers=CONSTS.getHeaders(), timeout=30).status_code != 200: return
    servers = [server for server in requests.get("https://api.pandahut.net/api/ServerProxy/PublicList", headers=CONSTS.getHeaders(), proxies=CONSTS.getProxyDict(), timeout=30).json()]
    server = None
    for server in servers:
        if serverinput not in server["IP"].split(".")[0] or "ENTRY" in server["ServerName"]: continue
        server = server
        break

    if not server: return
    resp = requests.get(f"https://api.pandahut.net/api/ServerProxy/PublicServerStatus/{server['_id']}", headers=CONSTS.getHeaders(), proxies=CONSTS.getProxyDict(), timeout=30)
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
        async with session.get(f"{CONSTS.LOGDOMAIN}{CONSTS.LOGFILEURL}", headers=CONSTS.getHeaders(), proxy=CONSTS.getProxyFormatted(), timeout=aiohttp.ClientTimeout(connect=5, sock_read=15)) as resp:
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

try:
    CONSTS.bot.run(CONSTS.token)
except Exception as e:
    print(f"[CRITICAL] Failed to get config file / bot token | {e}")