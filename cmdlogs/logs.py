import json, tempfile
from cmdlogs.MonitorRequest import MonitorRequest
from cmdlogs.Funni import Funni

class Logs:
    def __init__(self):
        self.path = f"{__file__.replace('logs.py', '')}"
        self.filename = "logs.json"
        self.filePath = f"{self.path}{self.filename}"
        self.funnifilename = "funni.json"
        self.funnifilePath = f"{self.path}{self.funnifilename}"
        self.tempfilename = "temp.json"
        self.tempfilepath = f"{self.path}{self.tempfilename}"
        self.prepTemp()
        self.load()
        

    def load(self):
        try:
            with open(self.filePath, "r", encoding="UTF-8") as self.file:
                self.logsData:dict = json.load(self.file)
                verifyResp = self.verify("log")
                if not verifyResp:
                    print("retard what did u do u fucking dumbass")
                    exit()
                self.getActive()
                print("loaded the funny")
            with open(self.funnifilePath, "r", encoding="UTF-8") as self.funnifile:
                self.funnilogsData:dict = json.load(self.funnifile)
                verifyResp = self.verify("funni")
                if not verifyResp:
                    print("retard what did u do u fucking dumbass v2")
                    exit()
                print("loaded the funny v2")
        except Exception as e:
            print(f"bruh {e}")
            exit()

    def save(self):
        # bruh
        if not self.verify("log") or not self.verify("funni"):
            print(f"fuck yoy verify false {self.logsData} | {self.funnilogsData}")
            exit()
        with open(self.filePath, "w", encoding="UTF-8") as file:
            json.dump(self.logsData, file, ensure_ascii=False, indent=4)
        with open(self.funnifilePath, "w", encoding="UTF-8") as file:
            json.dump(self.funnilogsData, file, ensure_ascii=False, indent=4)

    def verify(self, typeL):
        try:
            if typeL == "log":
                if (self.logsData == None or "valid" not in self.logsData.keys()):
                    return False
                self.prepTemp()
                with open(self.tempfilepath, "w+", encoding="UTF-8") as temp:
                    json.dump(self.logsData, temp, ensure_ascii=False, indent=4)
                with open(self.tempfilepath, "r", encoding="UTF-8") as temp:
                    json.load(temp)

            elif typeL == "funni":
                if (self.funnilogsData == None or "valid" not in self.funnilogsData.keys()):
                    return False
                self.prepTemp()
                with open(self.tempfilepath, "w+", encoding="UTF-8") as temp:
                    json.dump(self.funnilogsData, temp, ensure_ascii=False, indent=4)
                with open(self.tempfilepath, "r", encoding="UTF-8") as temp:
                    json.load(temp)
            
            self.prepTemp()
            return True
        except Exception as e:
            print(f"FUCK {len(self.funnilogsData)} {len(self.logsData)} {e}")
            exit()

    def prepTemp(self):
        with open(self.tempfilepath, "w", encoding="UTF-8") as file:
            file.truncate(0)
    
    def getActive(self) -> list:
        self.activeLogs = [{key : log} for key, log in self.logsData["logs"].items() if log["active"]]
        return self.activeLogs
    
    def parseUser(self, user):
        try:
            return int(user)
        except:
            # add steam thing here
            if type(user) == str: return user.lower()
        return ""

    def getActiveUser(self, user, autocomplete = False):
        self.getActive()
        user = self.parseUser(user)
        logsTemp = {}
        for logEntry in self.activeLogs:
            logsTemp = {key : log for key, log in logEntry.items() if user != "" and (log["user"] == user or (type(user) == str and ((autocomplete and user in log["display"].lower()) and len(user) >= 3 or user == log["display"].lower()))) and log["active"]}
            if len(logsTemp) > 0: break
        return logsTemp
    
    def getMention(self, user, autocomplete = False):
        for log in self.getActiveUser(user, autocomplete).values():
            return log["mention"]["id"]
    
    def isUserActive(self, user, autocomplete = False):
        log = self.getActiveUser(user, autocomplete)
        return len(log) > 0
    
    def addm(self, data: MonitorRequest):
        try:
            # rare 🤯
            if data.id in self.logsData.keys():
                print("HOLY SHIT NOT A DRILL 16 DIGIT COLLISONSADGJNLAD!!!! imageine if this happened twice and now ur db is fucked!")
                #data.refreshID()
            self.logsData["logs"][data.id] = data.__dict__
            print(f"new log {data.user} added from {data.author['name']} for {data.mention['name']} | {data.id}")
            self.save()
        except Exception as e:
            print(f"Error adding request | {data.author['name']} | {data.id} | {data.__dict__} | {e}")

    def add(self, data: Funni):
        try:

            try:
                idData = str(data.id)
                guid = data.guid[0]
                if idData not in self.funnilogsData["funni"].keys(): self.funnilogsData["funni"][idData] = data.__dict__
                elif guid not in self.funnilogsData["funni"][idData]["guid"]: self.funnilogsData["funni"][idData]["guid"].append(guid)
            except:
                self.funnilogsData["funni"][data.id] = data.__dict__

            self.funnilogsData["funni"][idData]["joins"] += 1

            #print(f"new funni {data.player} added {data.guid} | {data.id}")
            self.save()
        except Exception as e:
            print(f"Error adding request | {data.player} | {data.id} | {data.__dict__} | {e}")

logs = Logs()
