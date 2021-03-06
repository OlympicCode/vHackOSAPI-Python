from utils import Utils
from player import Player
import os
import time


class Network():
    def __init__(self, ut):
        self.ut = ut
        self.Configuration = self.ut.readConfiguration()
        self.targetBruted = self.ut.requestString("tasks.php",
                                                  accesstoken=self.Configuration["accessToken"])
        self.network = self.ut.requestString("network.php",
                                             accesstoken=self.Configuration["accessToken"], lang="en")


        if self.Configuration["attack_mode"] == "All" or self.Configuration["attack_mode"] == "just_attack":
            self.startFunctionAttack()

        if self.Configuration["attack_mode"] == "All" or self.Configuration["attack_mode"] == "just_recolt":
            self.createMalwareKit()
            self.RecoltMoney()

    def startFunctionAttack(self):
        # collect information in network.
        if "ips" not in self.network:
            self.ut.viewsPrint("showMsgErrorAPI", "You dont have ips in the network app... weird ... please wait")
            return False

        collect_scan_player = [(x["ip"], x["fw"], x["open"], x["level"]) \
                                for x in self.network["ips"]]

        p = Player(self.ut)
        for info_player in collect_scan_player:
            ip = str(info_player[0])
            firewall = int(info_player[1])

            # currency calcule for attack
            calc_attack = (firewall / int(p.getHelperApplication()["SDK"]["level"])) -1

            # define the rule for attack target
            if calc_attack >= 0.8:
                # not possible to attack user if their firewall is too strong
                self.ut.viewsPrint("showMsgDoesntPossibleAttack", "[{}] - Don't Attack Your SDK ({}) vs Target Firewall ({}) Match off ~({}%) on ip : '{}' :(".format(os.path.basename(__file__), int(p.getHelperApplication()["SDK"]["level"]), firewall, round(calc_attack*100), ip))
            else:
                # attack ip if firewall enemy < your SDK
                result = self.AttackTarget(ip)
                if result == 0:
                    break
        self.ut.viewsPrint("showMsgEndAttack", "[{}] - End Attack Loop Success.".format(os.path.basename(__file__)))
        return True

    def ChangeLog(self, ip):
        reqRemotelog = self.ut.requestString("remotelog.php", target=ip, accesstoken=self.Configuration["accessToken"], action="100", log=self.Configuration["msgLog"])
        resultLog = int(reqRemotelog["result"])

        if resultLog == 2:
            self.ut.viewsPrint("showMsgWriteLog", "[{}] - Write log '{}' to '{}'".format(os.path.basename(__file__), self.Configuration["msgLog"], ip))


    def AttackTarget(self, ip):
        your_exploit = self.ut.exploit()
        if int(your_exploit) > 0:

            # get information in device.
            targetHack = self.ut.requestString("exploit.php", lang="en", target=ip, accesstoken=self.Configuration["accessToken"])
            resultHack = int(targetHack["result"])

            # if result is good you are able to connect
            if resultHack == 0:
                # connect to the device
                targetRemote = self.ut.requestString("remote.php", lang="en", target=ip, accesstoken=self.Configuration["accessToken"])
                resultRemote = int(targetRemote["result"])
            else:
                return self.ut.result(result="don't return 0 weird", code=1)

            # if result is good you can launch a bruteforce to steal from bank
            if resultRemote == 0:
                bankingRemote = self.ut.requestString("remotebanking.php", target=ip, accesstoken=self.Configuration["accessToken"])
                resultbanking = int(bankingRemote["result"])
                passwordbanking = str(bankingRemote["remotepassword"])
            else:
                return self.ut.result(result="not returning 0 weird", code=2)

            # if password string was not recieved then it was not cracked ... start bruteforce
            if passwordbanking == "":
                reqBruteForce = self.ut.requestString("startbruteforce.php", target=ip, accesstoken=self.Configuration["accessToken"])
                resultBruteforce = int(reqBruteForce["result"])
            else:
                return self.ut.result(result="don't return '' weird", code=3)

            # verify your command target
            if resultBruteforce == 0:
                self.ut.viewsPrint("showMsgCollectMoneyUser", "[{}] - {} '{}'".format(os.path.basename(__file__), "Start Bruteforce to", ip))
                self.ChangeLog(ip)

            # if the return result is 2, then you have no exploits
            # not possible for you to hack, wait to
            # regenerate exploits.
            elif resultHack == 2:
                pass
        else:
            self.ut.viewsPrint("showMsgErrorSdk=0", "[{}] - not possible to hack, no exploits wait.".format(os.path.basename(os.path.basename(__file__))))
            return 0

    def RecoltMoney(self):
        # collect information in bruteforce list.
        try:
            collect_brute_player = [(x["username"], x["end"], x["user_ip"], x["start"], x["result"], x["now"], x["id"]) \
                                    for x in self.targetBruted["brutes"]]
        except KeyError:
            collect_brute_player = []

        for PlayerBrute in collect_brute_player:
            PlayerBruteUsername = PlayerBrute[0]
            PlayerBruteIP = PlayerBrute[2]
            reqBanking = self.ut.requestString("remotebanking.php", target=PlayerBruteIP, accesstoken=self.Configuration["accessToken"])
            try:
                money = int(reqBanking["money"])
            except KeyError:
                money = 0
            if money > 0:
                reqMoney = self.ut.requestString("remotebanking.php", target=PlayerBruteIP, accesstoken=self.Configuration["accessToken"], action="100", amount=money,  lang="en")
                self.ut.viewsPrint("showMsgCollectMoneyUser", "[{}] - {} {} to '{}'\033[0m".format(os.path.basename(__file__), "you are collected +", money, PlayerBruteIP))
                self.ChangeLog(PlayerBruteIP)
            else:
                self.ut.viewsPrint("showMsgCollectMoneyUser", "[{}] - {} {} to '{}'\033[0m".format(os.path.basename(__file__), "money = 0 no possible to get money", money, PlayerBruteIP))
                self.ChangeLog(PlayerBruteIP)

    def createMalwareKit(self):
        malware = self.ut.requestString("mwk.php", accesstoken=self.Configuration["accessToken"], lang="en")
        if int(malware["result"]) == 0:
            if int(malware["tasksCount"]) != 1:
                malware = self.ut.requestString("mwk.php", accesstoken=self.Configuration["accessToken"], action="100", lang="en")
                self.ut.viewsPrint("showMsgGenerateMWK", "[{}] -  Creating Malware Kit, you have ({}) Malware Kits".format(os.path.basename(__file__), malware["mwReady"]))
