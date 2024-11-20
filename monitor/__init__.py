import discord, re
from consts import CONSTS, monitors
from utils import roleCheck, LOGGER
from cmdlogs.MonitorRequest import MonitorRequest
from cmdlogs.logs import logs
from inspect import stack


async def monitor(interaction:discord.Interaction, user:str, ephemeral:bool = False, mentionuser:discord.User = None, display:str = ""):
    if not await roleCheck(interaction, CONSTS.LMAO): return
    if not mentionuser: mentionuser = interaction.user

    user = re.search(r"(\d{17})", user).group()
    if user == "":
        await interaction.response.send_message(f"id {user} does not match a valid steam64 id")
        return
    
    user = int(user)
    if len(logs.activeLogs) > 10 and interaction.user.id not in CONSTS.LMAO:
        await interaction.response.send_message(f"too many monitors are currently being monitored cancel a monitor to continue")
        return

    if logs.isUserActive(user):
        await interaction.response.send_message(f"user {user} is already monitored")
        return
    
    #monitors[steamID] = interaction.user.mention
    
    logs.addm(MonitorRequest(interaction, MonitorRequest.MonitorType.ADD, mentionuser, user, display))
    await interaction.response.send_message(f"succesfully monitoring {user} for user {mentionuser.mention}", ephemeral=ephemeral)
    LOGGER.log(stack()[0][3], f"succesfully monitoring {user} for user {mentionuser.id}", LOGGER.LogType.INFO)


async def cancelMonitor(interaction:discord.Interaction, user:str, ephemeral:bool = False):

    user = int(re.search(r"(\d*)", user).group())
    if user == "":
        await interaction.response.send_message(f"id {user} does not match a valid steam64 id")
        return
    
    user = int(user)
    if not logs.isUserActive(user):
        await interaction.response.send_message(f"user {user} is not monitored")
        return
    
    mention = logs.getMention(user)
    if mention != interaction.user.id and interaction.user.id not in CONSTS.LMAO:
        await interaction.response.send_message(f"nice try retard {interaction.user.name} does not have valid permissions to cancel this monitor")
        return
    
    #del monitors[steamID]
    for log in logs.activeLogs:
        for key, value in log.items():
            if value["user"] != user: continue
            logs.logsData["logs"][key]["active"] = False
    logs.save()
    await interaction.response.send_message(f"succesfully deleted monitor {user} for user <@!{mention}>", ephemeral=ephemeral)
    LOGGER.log(stack()[0][3], f"succesfully deleted monitor {user} for user {mention}", LOGGER.LogType.INFO)


async def listMonitors(interaction:discord.Interaction, ephemeral:bool = True):
    if not await roleCheck(interaction, CONSTS.LMAO): return
    if interaction.channel_id != 1256265181214801992:
        await interaction.response.send_message(content="wrong channel")
        return

    logs.getActive()
    activeMonitors = logs.activeLogs
    if len(activeMonitors) == 0:
        await interaction.response.send_message(content="no current active monitors", ephemeral=ephemeral)
        return
    
    embed = embed = discord.Embed(title=f"{len(activeMonitors)} MONITORED ACCOUNT{'S' if len(activeMonitors) > 1 else ''}", color=0x0084d1)
    for log in activeMonitors:
        for key, monitor in log.items():
            embed.add_field(name=f"```{key}```", value=f"```{monitor}```", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
    LOGGER.log(stack()[0][3], f"succesfully listed {len(activeMonitors)} monitor{'s' if len(activeMonitors) > 1 else ''} for user {interaction.user.name}", LOGGER.LogType.INFO)