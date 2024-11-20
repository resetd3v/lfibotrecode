import aiohttp, time as timeStats, hashlib, os
from consts import CONSTS, sentHashes
from utils import LOGGER
from inspect import stack

from staff import staffLog, staffParse

async def retrieveLog(this):
    try:
        timer = timeStats.time()
        #stream=True,
        #resp = requests.get(f"{LOGDOMAIN}{LOGFILEURL}", headers={"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"}, timeout=30)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{CONSTS.LOGDOMAIN}{CONSTS.LOGFILEURL}", headers=CONSTS.getHeaders(), timeout=30) as resp:
                if resp.status != 200: await LOGGER.log(stack()[0][3], f"resp returned {resp.status}", LOGGER.LogType.ERROR)

                with open(CONSTS.LOGFILE, "wb") as file:
                    file.truncate(0)
                    file.write(await resp.content.read())
                    file.seek(0, os.SEEK_END)
                    size = file.tell()

        fileSize = size #os.path.getsize(f"{LOGPATH}/latest.log")
        if fileSize / 1000000 < 0.03 and this.current_loop != 0:
            LOGGER.log(stack()[0][3], f"server restarted {fileSize} {this.current_loop}", LOGGER.LogType.INFO)
            sentHashes.clear()
            this.restart()

        LOGGER.log(stack()[0][3], f"wrote {fileSize / 1000000}MB to latest.log in {timeStats.time() - timer}", LOGGER.LogType.DEBUG if this.current_loop != 0 else LOGGER.LogType.INFO, 4)
        #await LOGGER.discLog(None, f"wrote {fileSize / 1000000}MB to latest.log", LOGGER.LogType.DEBUG, 3)
        # caching/line check soon:tm:
        i = 0
        x = 0
        timer = timeStats.time()
        with open(CONSTS.LOGFILE, "r", encoding="UTF-8") as file:
            lines = file.readlines()[-500:]
            for i,line in enumerate(lines):
                if hashlib.md5(line.encode("utf")).hexdigest() in sentHashes:
                    x += 1
                    continue
                # fucking discord heartbeat
                args = await staffParse(line, i, this.current_loop)
                if args[0]: await staffLog(*args)
        LOGGER.log(stack()[0][3], f"read {i} lines from latest.log in {timeStats.time() - timer}s {x} lines skipped", LOGGER.LogType.DEBUG, 3)
    except Exception as e: pass