#!/usr/bin/python2.7
# -*- coding: utf-8

import base64
import hashlib
import time
import requests

from requests.exceptions import ReadTimeout
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import ssl
import logging
import json
import ruamel.yaml as yaml
from ruamel.yaml.scalarstring import SingleQuotedScalarString, DoubleQuotedScalarString
import sys
import os
import platform
import io
import logging
import coloredlogs
import datetime
import random
from coloredterm import colored
from time import gmtime, strftime
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
from terminaltables import AsciiTable, SingleTable
from sys import stdout
import re
try:
    import fcntl
    import termios
    windows = False
except:
    windows = True
import time
import contextlib

#logger = logging.getLogger(__name__)

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


@contextlib.contextmanager
def raw_mode(file):
    if windows is False:
        old_attrs = termios.tcgetattr(file.fileno())
        new_attrs = old_attrs[:]
        new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
        try:
            termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
            yield
        finally:
            termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


USER_AGENT = ['Dalvik/2.1.0 (Linux; U; Android 5.0.1; GT-I9508V Build/LRX22C)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.1; MX4 Build/LRX22C)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; D5322 Build/19.3.A.0.472)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; D816w Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; HTC D816v Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; HTC E9pw Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; HTC M8t Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; HTC One M8s Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; LG-F320L Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; Letv X500 Build/DBXCNOP5500912251S)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; Nexus 5 Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0.2; SM-N9005 Build/LRX22G)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0; ASUS_Z00ADB Build/LRX21V)',
              'Dalvik/2.1.0 (Linux; U; Android 5.0; Nexus 5 Build/LPX13D)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1 Build/LYZ28N)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; 2014811 MIUI/6.1.26)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; A0001 Build/LMY47V)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; A0001 Build/LMY48Y)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; D5833 Build/23.4.A.1.232)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; GT-I9152 Build/LMY48Y)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; LG-D802 Build/LMY48W)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; MI 2 Build/LMY48B)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; MI 2SC Build/LMY47V)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; MI 3 Build/LMY48Y)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Mi-4c MIUI/6.1.14)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; NX403A Build/LMY48Y)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; ONE A2001 Build/LMY47V)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; R7Plusm Build/LMY47V)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Redmi Note 2 Build/LMY48Y)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-J3109 Build/LMY47X)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-N9200 Build/LMY47X)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Sparkle V Build/LMY47V)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; Xperia Z2 Build/LMY48Y)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1.1; titan Build/LMY48W)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; HTC M9w Build/LMY47O)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; HTC One M9 Build/LMY47O)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; LG-H818 Build/LMY47D)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; MX5 Build/LMY47I)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; XT1060 Build/LPA23.12-39.7)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; XT1085 Build/LPE23.32-53)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; m1 note Build/LMY47D)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; m2 Build/LMY47D)',
              'Dalvik/2.1.0 (Linux; U; Android 5.1; m2 note Build/LMY47D)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; 2014813 Build/MMB29U)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; A0001 Build/MMB29M)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; ASUS_Z00A Build/MMB29T)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; MI 4LTE Build/MMB29M)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Mi-4c Build/MMB29U)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Moto G 2014 Build/MMB29M)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Moto G 2014 LTE Build/MMB29T)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus 4 Build/MMB29M)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus 5 Build/MMB29K)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Sensation Build/MMB29U)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0.1; Z1 Build/MMB29T)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0; MI 2 Build/MRA58K)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0; MI 2A Build/MRA58K)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0; Moto G 2014 Build/MDB08M)',
              'Dalvik/2.1.0 (Linux; U; Android 6.0; XT1097 Build/MPE24.49-18)']


class Utils:
    def __init__(self):
        self.platform = platform.system()
        self.request = None
        self.secret = "aeffI"
        self.url = "https://api.vhack.cc/mobile/36/"
        self.Configuration = self.readConfiguration()
        self.numberLoop = 0
        self.account_info = None
        self.login = "0"

        try:
            self.username = str(self.Configuration["username"]).lstrip()
            self.password = str(self.Configuration["password"]).lstrip()
            self.debug = self.Configuration["debug"]
            self.show_info = self.Configuration["show_info"]
            self.sync_mobile = self.Configuration["sync_mobile"]
            self.attack_mode = self.Configuration["attack_mode"]
            self.update = self.Configuration["update"]
            self.msgremotelog = self.Configuration["msgLog"]
            self.timesleep = self.Configuration["timeSleep"]
            self.errorTime = self.Configuration["errorTime"]
            self.version = self.Configuration["version"]
        except KeyError as e:
            print("Error Configuration {}".format(e))
            sys.exit()
        if self.username is None or self.password is None:
            print("please Change Username/Password to config.yml")
            sys.exit()
        self.user_agent = self.generateUA(self.username + self.password)
        self.all_data = [
            ['Console Log vHackOS - by vBlackOut  [https://github.com/vBlackOut]']]

        try:
            if self.sync_mobile:
                self.generateConfiguration(
                    uID=self.Configuration["uID"], accessToken=self.Configuration["accessToken"])
            else:
                self.generateConfiguration()
        except TypeError:
            self.generateConfiguration()

        try:
            self.accessToken = self.Configuration["accessToken"]
            if self.accessToken == "":
                self.accessToken = None
        except:
            self.accessToken = None

        try:
            self.uID = self.Configuration["uID"]
            if self.uID == "":
                self.uID = None
        except KeyError:
            self.uID = None

    def check_version(self):
        r = requests.get("https://raw.githubusercontent.com/OlympicCode/vHackOSBot-Python/master/config.yml")
        for line in r.iter_lines():
            if "version:" in str(line):
                version = str(line).split(":")[1].replace("'", "")
                break

        if version.lstrip() != str(self.version.lstrip()):
            print("Please update your bot on github.")
            exit(1)

    def readConfiguration(self):
        # open configuration
        with open("config.yml", 'r') as stream:
            try:
                Configuration = yaml.load(stream, Loader=yaml.RoundTripLoader)
            except yaml.YAMLError as exc:
                self.viewsPrint("ErrorConfiguration", "{} [{}]".format(
                    "Error in your config.yml please check in", exc))
                sys.exit()

        if Configuration:
            return Configuration

    def result(self, result, code):
        self.viewsPrint(
            "showResult", "Error: {} code: {}".format(result, code))

    def viewsPrint(self, condition, Msg):
        if condition == "ErrorRequest":
            self.add_error()
            if self.Configuration["debug"]:
                print(self.printConsole("\033[0;103m\033[1;30mOutputBot: {} - {}\033[0m".format(
                    strftime("%Y-%m-%d %H:%M:%S", gmtime()), Msg)))
            else:
                return self.OutputTable("OutputBot: {} - {}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime()), colored(condition, self.printConsole(Msg)).autocolored()), 2)

        if condition in self.Configuration["show_info"] or "All" in self.Configuration["show_info"]:
            if "!{}".format(condition) in self.Configuration["show_info"]:
                pass
            else:
                if self.Configuration["debug"]:
                    print(self.printConsole("\033[0;103m\033[1;30mOutputBot: {} - {}\033[0m".format(
                        strftime("%Y-%m-%d %H:%M:%S", gmtime()), Msg)))
                else:
                    return self.OutputTable("OutputBot: {} - {}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime()), colored(condition, self.printConsole(Msg)).autocolored()), 2)

    def exploit(self):
        try:
            return self.exploits
        except:
            return 0

    def account(self):
        time.sleep(random.uniform(0.2, 0.5))
        try:
            return self.requestStringNowait("update.php", uID=self.uID, accesstoken=self.accessToken)
        except requests.exceptions.ReadTimeout:
            self.viewsPrint(
                "ErrorRequest", "Request Timeout... TimeOut connection")
            self.generateConfiguration(errorTime=int(time.time()))
            return None

    def OutputTable(self, msg, select_tables):
        if self.numberLoop < 6:
            self.numberLoop = self.numberLoop + 1
        else:
            self.numberLoop = 0

        if len(self.all_data) > 6:
            del self.all_data[-6]
        self.all_data.append([msg])
        data = self.all_data

        if select_tables == 1:
            table = AsciiTable(data)
            print(table.table)

        elif select_tables == 2:
            try:
                self.account_info = self.requestString(
                    "update.php", accesstoken=self.Configuration["accessToken"])
                self.exploits = int(self.account_info["exploits"])
                progress = round(
                    int(self.account_info["exp"])) / round(int(self.account_info["expreq"]))

                self.account_info["money"] = '{:0,}'.format(
                    int(self.account_info["money"]))
                self.account_info["netcoins"] = '{:0,}'.format(
                    int(self.account_info["netcoins"]))

                account_information = [["your account information", "update information"],
                                       ["{0}: {1}\n{2}: {3}\n{4}: {5}\n{6}: {7}\n{8}: {9}\n{10}: {11}".format("Your exploits ", self.exploits,
                                                                                                              "Your spam ", self.account_info[
                                                                                                                  "spam"],
                                                                                                              "Your network speed ", self.account_info[
                                                                                                                  "inet"],
                                                                                                              "Your money ", self.account_info[
                                                                                                                  "money"],
                                                                                                              "Your IP ", self.account_info[
                                                                                                                  "ipaddress"],
                                                                                                              "Your netcoins ", self.account_info["netcoins"]),

                                        "{}: {}\n{}: {}\n{}: {}\n{}: {}\n{}: {}, XP({}%)".format("Your SDK ", self.account_info["sdk"],
                                                                                                 "Your Firewall ", self.account_info[
                                                                                                     "fw"],
                                                                                                 "Your Antivirus ", self.account_info[
                                            "av"],
                                           "Your BruteForce ", self.account_info[
                                            "brute"],
                                           "Your level ", self.account_info["level"], round(progress * 100, 1))]]
            except (KeyError, requests.exceptions.ReadTimeout):
                account_information = [
                    ["your account information", "update information"], ["Error", "Error"]]

            table1 = SingleTable(data)
            table2 = SingleTable(account_information)
            time.sleep(random.uniform(0.1, 0.3))
            if self.platform == "Linux":
                print("\033[H\033[J")
            else:
                os.system('cls')

            req_version = (3, 0)
            cur_version = sys.version_info
            # for windows Try to print tables else pass python 2
            try:
                print(table1.table)
                print(table2.table)
                if windows is False:
                    sys.stdout.write("""\nCMD: [m] Get Miner info
     [a] Get All applications
     [q] Quit Program

Waiting for user input : """)
                    with raw_mode(sys.stdin):
                        try:
                            if cur_version <= req_version:
                                while True:
                                    ch = sys.stdin.read(1)
                                    if ch == "a":
                                        p = Player(self)
                                        getTask = self.requestString(
                                            "tasks.php", accesstoken=self.Configuration["accessToken"])
                                        sdk = p.getHelperApplication()[
                                            "SDK"]["level"]
                                        ipsp = p.getHelperApplication()[
                                            "IPSP"]["level"]
                                        bp = p.getHelperApplication()[
                                            "BP"]["level"]
                                        brute = p.getHelperApplication()[
                                            "BRUTE"]["level"]
                                        spam = p.getHelperApplication()[
                                            "SPAM"]["level"]
                                        fw = p.getHelperApplication()[
                                            "FW"]["level"]
                                        av = p.getHelperApplication()[
                                            "AV"]["level"]
                                        sys.stdout.write("\n \
    SDK: {} \
    IPSP: {}\n \
    Bank Protect: {} \
    BruteForce: {}\n \
    SPAM: {} \
    Firewall: {}\n \
    Antivirus: {}".format(sdk, ipsp, bp, brute, spam, fw, av))

                                        time.sleep(0.5)
                                    if ch == "m":
                                        self.minefinish = int(
                                            self.account_info['minerLeft'])
                                        sys.stdout.write(
                                            "\nminerLeft {} in secondes".format(self.minefinish))
                                        sys.stdout.write("\nwaiting until {} --- {}".format(self.tuntin(
                                            self.minefinish), datetime.timedelta(seconds=(self.minefinish))))
                                        time.sleep(1)
                                    if ch == "q":
                                        sys.stdout.write(
                                            "\nok ok, good bye ;)\n")
                                        sys.exit()
                            else:
                                while True:
                                    ch = sys.stdin.read(1)
                                    if ch == "a":
                                        p = Player(self)
                                        getTask = self.requestString(
                                            "tasks.php", accesstoken=self.Configuration["accessToken"])
                                        sdk = p.getHelperApplication()[
                                            "SDK"]["level"]
                                        ipsp = p.getHelperApplication()[
                                            "IPSP"]["level"]
                                        bp = p.getHelperApplication()[
                                            "BP"]["level"]
                                        brute = p.getHelperApplication()[
                                            "BRUTE"]["level"]
                                        spam = p.getHelperApplication()[
                                            "SPAM"]["level"]
                                        fw = p.getHelperApplication()[
                                            "FW"]["level"]
                                        av = p.getHelperApplication()[
                                            "AV"]["level"]
                                        sys.stdout.write("\n \
     SDK: {} \
     IPSP: {}\n \
     Bank Protect: {} \
     BruteForce: {}\n \
     SPAM: {} \
     Firewall: {}\n \
     Antivirus: {}".format(sdk, ipsp, bp, brute, spam, fw, av))

                                        time.sleep(0.5)
                                    if str(ch) == "m":
                                        self.minefinish = int(
                                            self.account_info['minerLeft'])
                                        sys.stdout.write(
                                            "\nminerLeft {} in secondes".format(self.minefinish))
                                        sys.stdout.write("\nwaiting until {} --- {}".format(self.tuntin(
                                            self.minefinish), datetime.timedelta(seconds=(self.minefinish))))
                                        time.sleep(1)
                                    if ch == "q":
                                        sys.stdout.write(
                                            "\nok ok, good bye ;)\n")
                                        sys.exit()
                                    break
                        except (KeyboardInterrupt, EOFError):
                            pass
            except IOError as e:
                pass

    def tuntin(self, secs):
        st = (datetime.datetime.now() + datetime.timedelta(seconds=300))
        return st.strftime('%H:%M:%S')

    def getPlatform(self):
        return self.platform

    def printConsole(self, txt):
        if self.platform == "Linux":
            return txt
        else:
            ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
            return ansi_escape.sub('', txt)

    def generateConfiguration(self, uID=False, accessToken=False, errorTime=False):
        # append uID/accessToken and other param in new configuration file.
        self.Configuration['username'] = self.username
        self.Configuration['password'] = self.password
        self.Configuration['debug'] = self.debug
        self.Configuration['show_info'] = self.show_info
        self.Configuration['sync_mobile'] = self.sync_mobile
        self.Configuration['attack_mode'] = self.attack_mode
        self.Configuration['update'] = self.update
        self.Configuration["msgLog"] = self.msgremotelog
        self.Configuration["timeSleep"] = self.timesleep
        self.Configuration["version"] = self.version

        if errorTime is not False:
            self.Configuration["errorTime"] = errorTime
        else:
            self.Configuration["errorTime"] = None

        # delete old file
        # os.remove("config.yml")

        try:
            self.Configuration['uID'] = uID
        except KeyError:
            self.Configuration['uID'] = self.uID

        try:
            self.Configuration['accessToken'] = accessToken
        except KeyError:
            self.Configuration['accessToken'] = self.accessToken

        if not self.Configuration['accessToken'] and not self.Configuration['uID']:
            self.request = requests.Session()
            self.request.headers.update({'User-agent': self.user_agent})
            url = 'login.php'
            url_login = self.Login(url, self.username, self.password)

            try:
                result = self.request.get(url_login, timeout=5, verify=False)
            except requests.exceptions.ConnectTimeout:
                self.viewsPrint(
                    "ErrorRequest", "Request Timeout... TimeOut connection '{}'".format(url))
                sys.exit()

            except requests.exceptions.ReadTimeout:
                self.viewsPrint(
                    "ErrorRequest", "Request Timeout... TimeOut connection {}".format(php))
                sys.exit()

            except requests.exceptions.ConnectionError:
                self.viewsPrint(
                    "ErrorRequest", "Request Timeout... Connection Error '{}'".format(url))
                sys.exit()

            result.encoding = 'UTF-8'
            parseJson = result.json()

            check_return_server = self.CheckServerError(parseJson)
            if check_return_server:
                print("Server Error: [{}] {}".format(
                    check_return_server[0], check_return_server[1]))
                return False

            self.accessToken = str(parseJson["accesstoken"])
            self.uID = int(parseJson["uid"].encode("UTF-8"))

            self.Configuration.yaml_add_eol_comment(
                "# < Your Username Account", 'username', column=5)
            self.Configuration.yaml_add_eol_comment(
                "# < Your Password Account\n\n", 'password', column=5)
            self.Configuration.yaml_add_eol_comment(
                "# < debug mode\n\n", 'debug', column=5)
            self.Configuration.yaml_add_eol_comment(
                "# < show the return bot print information\n\n", 'show_info', column=5)
            self.Configuration.yaml_add_eol_comment(
                "# < If your are uID and accessToken and your phone bot use configuration for login please replace your uid and accesstoken sync to phone. (Recommended OFF)\n\n", 'sync_mobile', column=5)
            self.Configuration.yaml_add_eol_comment(
                "# < Automatically added uID for your account don't change /!\\", 'uID', column=5)
            self.Configuration.yaml_add_eol_comment(
                "# < Automatically added accessToken for your account don't change /!\\", 'accessToken', column=5)

            try:
                # for python 3
                with io.open('config.yml', 'w+') as outfile:
                    yaml.dump(self.Configuration, stream=outfile, default_flow_style=False,
                              Dumper=yaml.RoundTripDumper, indent=4, block_seq_indent=1)
            except:
                # for python 2
                with io.open('config.yml', 'wb') as outfile:
                    yaml.dump(self.Configuration, stream=outfile, default_flow_style=False,
                              Dumper=yaml.RoundTripDumper, indent=4, block_seq_indent=1)

            self.request = None

        else:

            self.Configuration.yaml_add_eol_comment(
                "# < Your Username Account", 'username', column=5)
            self.Configuration.yaml_add_eol_comment(
                "# < Tour Password Account\n\n", 'password', column=5)
            self.Configuration.yaml_add_eol_comment(
                "# < debug mode dev online\n\n", 'debug', column=5)
            self.Configuration.yaml_add_eol_comment(
                "# < show the return bot print information\n\n", 'show_info', column=5)
            self.Configuration.yaml_add_eol_comment(
                "# < If your are uID and accessToken and your phone bot use configuration for login please replace your uid and accesstoken sync to phone. (Recommended OFF)\n\n", 'sync_mobile', column=5)
            self.Configuration.yaml_add_eol_comment(
                "# < Automatically added uID for your account don't change /!\\", 'uID', column=5)
            self.Configuration.yaml_add_eol_comment(
                "# < Automatically added accessToken for your account don't change /!\\", 'accessToken', column=5)

            try:
                # for python 3
                with io.open('config.yml', 'w+') as outfile:
                    yaml.dump(self.Configuration, stream=outfile, default_flow_style=False,
                              Dumper=yaml.RoundTripDumper, indent=4, block_seq_indent=1)
            except:
                # for python 2
                with io.open('config.yml', 'wb') as outfile:
                    yaml.dump(self.Configuration, stream=outfile, default_flow_style=False,
                              Dumper=yaml.RoundTripDumper, indent=4, block_seq_indent=1)

    def add_error(self):
        self.remove_error()
        with open("config.yml", "a") as file:
            file.write("errorTime: {}".format(int(time.time()) + 600))

    def remove_error(self):
        with open('config.yml', 'r+') as f:
            f.seek(0, os.SEEK_END)
            while f.tell() and f.read(1) != '\n':
                f.seek(-2, os.SEEK_CUR)
            f.truncate()

    def generateUA(self, identifier):
        pick = int(self.md5hash(identifier), 16)
        user_agents = tuple(USER_AGENT)
        return user_agents[pick % len(user_agents)]

    def getTime(self):
        return int(round(time.time()))

    def md5hash(self, txt):
        m = hashlib.md5()
        m.update(txt.encode('utf-8'))
        return m.hexdigest()

    def generateUser(self, bArr):
        b64 = base64.urlsafe_b64encode(bArr.encode('UTF-8')).decode('ascii')
        return b64.replace("=", "")

    def Login(self, php, username, password):

        passmd5 = self.md5hash(password)
        jsonString = {'username': username, 'password': passmd5}
        jsonString = json.dumps(jsonString, separators=(',', ':'))

        str8 = self.md5hash("{}{}{}".format(jsonString, jsonString,
                                            self.md5hash(jsonString)))

        return "{}{}?user={}&pass={}".format(self.url, php,
                                             self.generateUser(jsonString), str8)

    def generateURL(self, uid, php, **kwargs):
        jsonString = kwargs
        jsonString.update(
            {'uid': str(self.uID), 'accesstoken': str(self.accessToken)})
        jsonString.pop("debug", None)
        jsonString = json.dumps(jsonString, default=set_default)
        str8 = self.md5hash("{}{}{}".format(jsonString, jsonString,
                                            self.md5hash(jsonString)))

        return "{}{}?user={}&pass={}".format(self.url, php, self.generateUser(jsonString), str8)

    def CheckServerError(self, code_return):
        try:
            code_return = code_return["result"]
        except (TypeError, IndexError):
            code_return = "0"

        t = None
        if code_return == u"5":
            t = (5, "Check your Internet Connection.")
        elif code_return == u"2":
            t = (8, "User/Password wrong!")
        elif code_return == u"10":
            t = (10, "API is updated.")
        elif code_return == u"15":
            t = (10, "You are banned sorry :(")
        elif code_return == u"99":
            t = (99, "Server is down for Maintenance, please be patient.")
        return t

    def requestString(self, php, **kwargs):
        # print("Request: {}, {}".format(php, self.uID))
        self.user_agent = self.generateUA(
            "test{}test".format(random.randint(1, 9999)))
        try:
            if kwargs["debug"] is True:
                time.sleep(self.timesleep)
                http_client.HTTPConnection.debuglevel = 0
                # You must initialize logging, otherwise you'll not see debug output.
                logging.basicConfig()
                logger = logging.getLogger().setLevel(logging.DEBUG)
                requests_log = logging.getLogger("requests.packages.urllib3")
                requests_log.setLevel(logging.DEBUG)
                requests_log.propagate = True
                coloredlogs.install(level='DEBUG')
                coloredlogs.install(level='DEBUG', logger=requests_log)

        except KeyError:
            kwargs["debug"] = self.debug
            if kwargs["debug"] is True:
                time.sleep(self.timesleep)
                http_client.HTTPConnection.debuglevel = 0
                # You must initialize logging, otherwise you'll not see debug output.
                logging.basicConfig()
                logger = logging.getLogger().setLevel(logging.DEBUG)
                requests_log = logging.getLogger("requests.packages.urllib3")
                requests_log.setLevel(logging.DEBUG)
                requests_log.propagate = True
                coloredlogs.install(level='DEBUG')
                coloredlogs.install(level='DEBUG', logger=requests_log)

        time.sleep(random.uniform(0.5, 1))
        i = 0
        while True:
            if i > 10:
                self.viewsPrint(
                    "ErrorRequest", "Request Timeout... TimeOut connection {}".format(php))
                sys.exit()

            try:
                self.uID
                self.accessToken
                self.request
                self.sync_mobile
            except AttributeError:
                print("\nError - Your account blocked. please wait")
                try:
                    error_time = self.errorTime - int(time.time())
                except:
                    error_time = 600

                if error_time > 0:
                    for remaining in range(error_time, 0, -1):
                        sys.stdout.write("\r")
                        sys.stdout.write(
                            "{:2d} seconds remaining. number retry ({})".format(remaining, i))
                        sys.stdout.flush()
                        time.sleep(1)
                        self.add_error()
                self.remove_error()

                i = i + 1
                python = sys.executable
                os.execl(python, python, * sys.argv)
                return False

            if self.uID is None or self.accessToken is None or self.request is None and self.sync_mobile is False:
                # connect login.
                self.request = requests.Session()
                self.request.headers.update({'User-agent': self.user_agent})
                url_login = self.Login(
                    'login.php', self.username, self.password)
                try:
                    time.sleep(self.timesleep)
                    result = self.request.get(
                        url_login, timeout=5, verify=False)

                except requests.exceptions.ConnectTimeout:
                    self.viewsPrint(
                        "ErrorRequest", "Request Timeout... TimeOut connection {}".format(php))

                except requests.exceptions.ReadTimeout:
                    self.viewsPrint(
                        "ErrorRequest", "Request Timeout... TimeOut connection {}".format(php))

                except requests.exceptions.ConnectionError:
                    self.viewsPrint("ErrorRequest", "Request Timeout... Connection Error '{}' with code: [{}]".format(
                        'login.php', url_login.status_code))

                result.encoding = 'UTF-8'
                parseJson = result.json()

                check_return_server = self.CheckServerError(parseJson)

                if check_return_server:
                    print("Server Error: [{}] {}".format(
                        check_return_server[0], check_return_server[1]))
                    return False

                self.accessToken = str(parseJson["accesstoken"])
                self.uID = int(parseJson["uid"].encode("UTF-8"))
                global login
                self.login = "1"

                self.generateConfiguration(self.uID, self.accessToken)

                # Create First request.
                try:
                    result = self.request.get(self.generateURL(
                        self.uID, php, **kwargs), timeout=5)
                except requests.exceptions.ConnectTimeout:
                    self.viewsPrint(
                        "ErrorRequest", "Request Timeout... TimeOut connection {}".format(php))

                except requests.exceptions.ReadTimeout:
                    self.viewsPrint(
                        "ErrorRequest", "Request Timeout... TimeOut connection {}".format(php))

                except requests.exceptions.ConnectionError:
                    self.viewsPrint("ErrorRequest", "Request Timeout... Connection Error '{}' with code: [{}]".format(
                        php, url_login.status_code))

                if kwargs["debug"] is True:
                    logging.info(result.json())

            elif self.uID is not None or self.accessToken is not None:
                #request = requests.Session()
                if not self.request:
                    self.request = requests.Session()

                self.request.headers.update({'User-agent': self.user_agent})

                if self.sync_mobile is True:
                    if self.login is "0":
                        self.login = "1"
                        self.request.get(self.generateURL(
                            self.uID, 'update.php', accesstoken=self.accessToken, lang="fr", lastread="0"), timeout=3)

                # return just request don't login before.
                try:
                    result = self.request.get(self.generateURL(
                        self.uID, php, **kwargs), timeout=5)
                except requests.exceptions.ConnectTimeout:
                    self.viewsPrint(
                        "BadRequest", "Request Timeout... TimeOut connection {}".format(php))

                except requests.exceptions.ReadTimeout:
                    self.viewsPrint(
                        "ErrorRequest", "Request Timeout... TimeOut connection {}".format(php))

                except requests.exceptions.ConnectionError:
                    self.viewsPrint(
                        "BadRequest", "Request Timeout... Connection Error '{}'".format(php))

                result.encoding = 'UTF-8'
                try:
                    parseJson = result.json()
                    result = True
                except ValueError:
                    self.viewsPrint(
                        "ErrorJson", "Closing bot upon bad request...")
                    time.sleep(5)

                try:
                    self.accessToken = str(parseJson["accesstoken"])
                except (KeyError, UnboundLocalError):
                    pass

            i = i + 1
            if kwargs["debug"] is True:
                logging.info(parseJson)

            if result:
                break

        if parseJson["result"] is not None or len(parseJson) > 1:
            return parseJson
        else:
            self.viewsPrint(
                "BadRequest", "/!\ Block Script your credential as changed")
            exit(1)

    def requestStringNowait(self, php, **kwargs):
        # print("Request: {}, {}".format(php, self.uID))
        self.user_agent = self.generateUA("testtest")
        try:
            if kwargs["debug"] is True:
                http_client.HTTPConnection.debuglevel = 0
                # You must initialize logging, otherwise you'll not see debug output.
                logging.basicConfig()
                logger = logging.getLogger().setLevel(logging.DEBUG)
                requests_log = logging.getLogger("requests.packages.urllib3")
                requests_log.setLevel(logging.DEBUG)
                requests_log.propagate = True
                coloredlogs.install(level='DEBUG')
                coloredlogs.install(level='DEBUG', logger=requests_log)

        except KeyError:
            kwargs["debug"] = self.debug
            if kwargs["debug"] is True:
                http_client.HTTPConnection.debuglevel = 0
                # You must initialize logging, otherwise you'll not see debug output.
                logging.basicConfig()
                logger = logging.getLogger().setLevel(logging.DEBUG)
                requests_log = logging.getLogger("requests.packages.urllib3")
                requests_log.setLevel(logging.DEBUG)
                requests_log.propagate = True
                coloredlogs.install(level='DEBUG')
                coloredlogs.install(level='DEBUG', logger=requests_log)

        i = 0
        while True:
            if i > 10:
                break
            if self.uID is None or self.accessToken is None or self.request is None and self.sync_mobile is False:
                # connect login.
                self.request = requests.Session()
                self.request.headers.update({'User-agent': self.user_agent})
                url_login = self.Login(
                    'login.php', self.username, self.password)
                try:
                    result = self.request.get(
                        url_login, timeout=3, verify=False)
                except requests.exceptions.ConnectTimeout:
                    self.viewsPrint(
                        "ErrorRequest", "Request Timeout... TimeOut connection {}".format(php))

                except requests.exceptions.ReadTimeout:
                    self.viewsPrint(
                        "ErrorRequest", "Request Timeout... TimeOut connection {}".format(php))

                except requests.exceptions.ConnectionError:
                    self.viewsPrint("ErrorRequest", "Request Timeout... Connection Error '{}' with code: [{}]".format(
                        'login.php', url_login.status_code))

                result.encoding = 'UTF-8'
                parseJson = result.json()

                check_return_server = self.CheckServerError(parseJson)
                if check_return_server:
                    print("Server Error: [{}] {}".format(
                        check_return_server[0], check_return_server[1]))
                    return False

                self.accessToken = str(parseJson["accesstoken"])
                self.uID = int(parseJson["uid"].encode("UTF-8"))
                global login
                self.login = "1"

                self.generateConfiguration(self.uID, self.accessToken)

                # Create First request.
                try:
                    result = self.request.get(self.generateURL(
                        self.uID, php, **kwargs), timeout=5)
                except requests.exceptions.ConnectTimeout:
                    self.viewsPrint(
                        "ErrorRequest", "Request Timeout... TimeOut connection {}".format(php))

                except requests.exceptions.ReadTimeout:
                    self.viewsPrint(
                        "ErrorRequest", "Request Timeout... TimeOut connection {}".format(php))

                except requests.exceptions.ConnectionError:
                    self.viewsPrint("ErrorRequest", "Request Timeout... Connection Error '{}' with code: [{}]".format(
                        php, url_login.status_code))

                if kwargs["debug"] is True:
                    logging.info(result.json())

            elif self.uID is not None or self.accessToken is not None:
                #request = requests.Session()
                if not self.request:
                    self.request = requests.Session()

                self.request.headers.update({'User-agent': self.user_agent})

                if self.sync_mobile is True:
                    if self.login is "0":
                        self.login = "1"
                        self.request.get(self.generateURL(
                            self.uID, 'update.php', accesstoken=self.accessToken, lang="fr", lastread="0"), timeout=3)

                # return just request don't login before.
                try:
                    result = self.request.get(self.generateURL(
                        self.uID, php, **kwargs), timeout=5)

                except requests.exceptions.ConnectTimeout:
                    self.viewsPrint(
                        "ErrorRequest", "Request Timeout... TimeOut connection {}".format(php))

                except requests.exceptions.ReadTimeout:
                    self.viewsPrint(
                        "ErrorRequest", "Request Timeout... TimeOut connection {}".format(php))

                except requests.exceptions.ConnectionError:
                    self.viewsPrint("ErrorRequest", "Request Timeout... Connection Error '{}' with code: [{}]".format(
                        php, url_login.status_code))

                result.encoding = 'UTF-8'
                try:
                    parseJson = result.json()
                except:
                    time.sleep(random.uniform(0.5, 1.5))
                    result = self.request.get(self.generateURL(
                        self.uID, php, **kwargs), timeout=5)
                    result.encoding = 'UTF-8'
                    parseJson = result.json()

                try:
                    self.accessToken = str(parseJson["accesstoken"])
                except (KeyError, UnboundLocalError):
                    pass

            i = i + 1
            if kwargs["debug"] is True:
                logging.info(result.json())
        return parseJson


class Player():
    def __init__(self, ut):
        self.ut = ut
        self.Configuration = self.ut.readConfiguration()
        self.getStore = self.ut.requestString("store.php",
                                              accesstoken=self.Configuration["accessToken"], lang="en")

    def getApplication(self):
        Dict_request = self.getStore["apps"]
        ApplicationCount = []

        for ApplicationUp in enumerate(Dict_request):
            Application = {}
            try:
                Application["baseprice"] = ApplicationUp[1]["baseprice"]
                Application["level"] = ApplicationUp[1]["level"]
                Application["price"] = ApplicationUp[1]["price"]
                Application["factor"] = ApplicationUp[1]["factor"]
                Application["maxlvl"] = ApplicationUp[1]["maxlvl"]
                Application["running"] = ApplicationUp[1]["running"]
                Application["appid"] = ApplicationUp[1]["appid"]
                Application["require"] = ApplicationUp[1]["require"]

            except KeyError as e:
                Application["baseprice"] = None
                Application["level"] = ApplicationUp[1]["level"]
                Application["price"] = ApplicationUp[1]["price"]
                Application["factor"] = None
                Application["maxlvl"] = ApplicationUp[1]["maxlvl"]
                Application["running"] = None
                Application["appid"] = ApplicationUp[1]["appid"]
                Application["require"] = ApplicationUp[1]["require"]

            ApplicationCount.append(Application)

        return ApplicationCount

    def getHelperApplication(self):
        Application = self.getApplication()
        FinalApplication = {}

        for allApplication in Application:
            # antivirus
            if int(allApplication["appid"]) == 1:
                FinalApplication["AV"] = allApplication

            # firewall
            if int(allApplication["appid"]) == 2:
                FinalApplication["FW"] = allApplication

            # spam
            if int(allApplication["appid"]) == 3:
                FinalApplication["SPAM"] = allApplication

            # brute force
            if int(allApplication["appid"]) == 4:
                FinalApplication["BRUTE"] = allApplication

            # banque protecte
            if int(allApplication["appid"]) == 5:
                FinalApplication["BP"] = allApplication

            # Software developement kit
            if int(allApplication["appid"]) == 6:
                FinalApplication["SDK"] = allApplication

            if int(allApplication["appid"]) == 7:
                pass
                #FinalApplication[""] = allApplication

            if int(allApplication["appid"]) == 8:
                pass
                #FinalApplication[""] = allApplication

            if int(allApplication["appid"]) == 9:
                pass
                #FinalApplication[""] = allApplication

            if int(allApplication["appid"]) == 10:
                FinalApplication["IPSP"] = allApplication

            if int(allApplication["appid"]) == 11:
                pass
                #FinalApplication[""] = allApplication

            if int(allApplication["appid"]) == 12:
                pass
                #FinalApplication[""] = allApplication

            if int(allApplication["appid"]) == 13:
                pass
                #FinalApplication[""] = allApplication

            if int(allApplication["appid"]) == 14:
                pass
                #FinalApplication[""] = allApplication

            if int(allApplication["appid"]) == 15:
                pass
                #FinalApplication[""] = allApplication

        return FinalApplication
