from utils import Utils
from player import Player
import os, time

class Update():
    def __init__(self, ut):
        self.ut = ut
        self.Configuration = self.ut.readConfiguration()
        self.store = self.ut.requestString("store.php",
                                           accesstoken=self.Configuration["accessToken"])
        self.startFunctionUpdate()

    def startFunctionUpdate(self):

        # get money info
        money = self.store["money"]
        p = Player(self.ut)

        
        # get applications and update this
        # check number of running tasks before the start of the for loop
        # this value is stored in the variable update and should be incremented with every successfull update.
        # This will reduce the number of requests sent to the server which will lower chances of botting detection.
        getTask = self.ut.requestString("tasks.php", accesstoken=self.Configuration["accessToken"])
        if 'updateCount' in getTask.keys():
            update = getTask['updateCount']
        
        for applications in self.store["apps"]:
            if update < 10:
                Appid = int(applications["appid"])
                for list_update in self.Configuration["update"]:
                    time.sleep(0.3)
                    application_update = int(p.getHelperApplication()[list_update]["appid"])
                    if Appid == application_update:
                        if money >= applications["price"]:
                            result = self.ut.requestString("store.php",
                                                               accesstoken=self.Configuration["accessToken"],
                                                               appcode=application_update,
                                                               action="100")
                            if result['result'] == '0':
                                self.ut.viewsPrint("showMsgUpdate", "[{}] - Update for your {} +1".format(os.path.basename(__file__), list_update))
                                update = update + 1
                                time.sleep(0.5)
                        else:
                            self.ut.viewsPrint("showMsgUpdate", "[{}] - you have not money to upgrade {}".format(os.path.basename(__file__), list_update))
                            time.sleep(0.5)
            else:
            	self.ut.viewsPrint("showMsgUpdatefull", "[{}] - full task used please wait.".format(os.path.basename(__file__)))
            	time.sleep(0.5)
            	return False


