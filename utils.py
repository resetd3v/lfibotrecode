import asyncio, typing, functools, discord, re, random, string, sys
from datetime import datetime, timedelta, timezone
from enum import Enum


TIMEZONE = -5
DEBUGCHANNEL = 1256018442784608287
# stackoverflow
def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper

class Logger():
    def __init__(self):
        self.level = 2
        self.original = sys.stdout
        self.output = f"bruh/{datetime.now().strftime('%H-%M-%S_%d-%m')}.log"

    class LogType(Enum):
        NONE = 0,
        WARNING = 1,
        ERROR = 2,
        CRITICAL = 3,
        INFO = 4,
        DEBUG = 5

    def log(self, function, msg, logType:LogType = LogType.NONE, level = 1):
        if logType == self.LogType.DEBUG and self.level < level: return
        format = f"[{logType.name if logType != self.LogType.NONE else ''}]({function}) {msg}"
        print(format)
        with open(self.output, "a", encoding="UTF-8") as file:
            file.write(format + "\n")
            # sys.stdout = file
            # print(format)
        #sys.stdout = self.original
    
    async def discLog(self, bot: discord.Client, interaction:discord.Interaction, msg, logType:LogType = LogType.NONE, level = 1):
        if logType == self.LogType.DEBUG:
            if self.level < level: return
            
            channel = bot.get_channel(DEBUGCHANNEL)
            await channel.send(f"[{logType.name if logType != self.LogType.NONE else ''}] {msg}")
            return
        await interaction.response.send_message(f"[{logType.name if logType != self.LogType.NONE else ''}] {msg}")

LOGGER = Logger()

async def roleCheck(interaction: discord.Interaction, LMAO):
    if interaction.user.id in LMAO: return True
    await interaction.response.send_message("not yet.")
    return False

def getColor(action):
    color = 0x0084d1
    red = 0xff0000
    orange = 0xffbf00
    match action.name:
        case "ban": color = red
        case "spy": color = red
        case "tp": color = red
        case "stats": color = orange
        case _: pass

    return color

def getTime(data: str):
    # time
    timeThing = re.search(r'(.*)\..*UTC]', data).group().replace("[", "").replace(" UTC]", "").split(" ")[::-1]
    amazingObf = random.randint(-3,-1)
    key = int(''.join(str(ord(char)) for char in random.choices(string.ascii_letters, k=10)))
    clockTime = datetime.strptime(timeThing[0].split('.')[0], "%H:%M:%S") + timedelta(seconds=amazingObf)
    # left ^ (right ^ 1337) ^ 420691337
    timestamp = f"{clockTime.strftime('%H:%M:%S')} {'-'.join(timeThing[-1].split('-')[1:])}"
    obf = f"\n{amazingObf ^ key ^ 420691337} {key ^ 1337}"
    timestamp = (datetime.strptime(timestamp, "%H:%M:%S %m-%d") - timedelta(hours=TIMEZONE)).strftime("%m-%d %H:%M:%S")
    return (timestamp, obf)
