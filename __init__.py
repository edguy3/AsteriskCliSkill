#!/usr/bin/python

# Copyright (C) 2017 Ed Guy <edguy@eguy.org> 

from asterisk.ami import AMIClient, EventListener, AutoReconnect
from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'edguy3'
LOGGER = getLogger(__name__)


class AsteriskCliSkill(MycroftSkill):

    # constructor calls MycroftSkill's constructor to build data structures. 
    def __init__(self):
        super(AsteriskCliSkill, self).__init__(name="AsteriskCliSkill")
        self.loggedin=False
        self.lastcaller="No One"

    # runtime initialize instance for use. 
    def initialize(self):
        self.load_data_files(dirname(__file__))
	h=self.settings.get("host","127.0.0.1")
	try:
	    p=int(self.settings.get("port",5038))
	except Exception:
            p=5038

        self.client = AMIClient(address=h,port=p)
        future = self.client.login(username=self.settings.get('username','pi'),secret=self.settings.get('password','password'))
        if future.response.is_error():
            LOGGER.debug("AsteriskCliSkill login fail: "+str(future.response))
            return
        self.loggedin=True
        #self.autoconnect=AutoReconnect(self.client)
            
        # what was that last call? 
        #last_call_intent = IntentBuilder("LastCallIntent").\
        #	require("WhoLastCaller").build()
        #self.register_intent(last_call_intent, self.handle_last_call_intent)


        self.client.add_event_listener(EventListener(on_event=self.handle_cli, white_list='Newstate', ChannelStateDesc='Ringing'))
        LOGGER.info("AsteriskCliSkill Listening host: "+h+" port set to: "+str(p))

        
    # other calling functions. 

    def handle_last_call_intent(self, message):
        LOGGER.debug("AsteriskCliSkill last_caller invoked")
	self.speak_dialog("last.caller", {'name': self.lastcaller})

    def handle_cli(self, message):
        LOGGER.debug("AsteriskCliSkill CLI invoked")
        self.speak(event["ConnectedLineName"])
        self.lastcaller=event["ConnectedLineName"]

    # tear down connection
    def stop(self):
        LOGGER.debug("AsteriskCliSkill Stopping...")
	if self.loggedin:
	    try:
		del self.autoconnect
            except Exception:
                LOGGER.debug("AsteriskCliSkill Exception handled 1")
	if self.loggedin:
	    try:
                self.client.disconnect()
            except Exception:
                LOGGER.debug("AsteriskCliSkill Exception handled 2")
		pass
        LOGGER.debug("AsteriskCliSkill stopped!!")


def create_skill():
    return AsteriskCliSkill()
