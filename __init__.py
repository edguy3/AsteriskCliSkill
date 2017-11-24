#!/usr/bin/python

# Copyright (C) 2017 Ed Guy <edguy@eguy.org> 

from websocket import create_connection, WebSocket
import ssl
import sys
import fileinput
import os
import time

from asterisk.ami import AMIClient
from asterisk.ami import EventListener
from pprint import pprint

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

    # runtime initialize instance for use. 
    def initialize(self):
        self.load_data_files(dirname(__file__))

        h=self.settings.get("host","127.0.0.1")
        p=self.settings.get("port",5038)
        self.client = AMIClient(address=h,port=p)
        future = self.client.login(username=self.settings.get('username'),secret=self.settings.get('password'))
        if future.response.is_error():
            raise Exception(str(future.response))
        AutoReconnect(self.client)
        LOGGER.debug("AsteriskCliSkill Started")
            
        self.client.add_event_listener(EventListener(on_event=handle_cli, white_list='Newstate', ChannelStateDesc='Ringing'))
        LOGGER.debug("AsteriskCliSkill Listening")

        # what was that last call? 
        #        last_call_intent = IntentBuilder("LastCallIntent").\
        #            require("LastCallKeyword").build()
        #        self.register_intent(last_call_intent, self.handle_last_call_intent)
        
        # other calling functions. 

    def handle_cli(self, message):
        LOGGER.debug("AsteriskCliSkill CLI invoked")
        self.speak(event["ConnectedLineName"])
        self.lastcaller=event["ConnectedLineName"]

    # tear down connection
    def stop(self):
        LOGGER.debug("AsteriskCliSkill Stopped")
        self.client.logoff()

def create_skill():
    return AsteriskCliSkill()
