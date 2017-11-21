#!/usr/bin/python

# Copyright (C) 2017 Ed Guy <edguy@eguy.org> 

from websocket import create_connection, WebSocket
import ssl
import sys
import fileinput
import os
import time
from settings import login, connection

from asterisk.ami import AMIClient
from asterisk.ami import EventListener
from pprint import pprint

class MyWebSocket(WebSocket):
    def recv_message(self):
	message = super().recv_frame()
        print('Recieved message: {}'.format(message))
        return message

def sayCLI(line):
	ws = create_connection("ws://0.0.0.0:8181/core", sslopt={"cert_reqs": ssl.CERT_NONE}, class_=MyWebSocket)
    	mycroft_type = '"speak"'
    	mycroft_data = '{"expect_response": false, "utterance": "%s"}, "context": null' % line.strip()
    	message = '{"type": ' + mycroft_type + ', "data": ' + mycroft_data + '}'
#    	print(message)
#    	print("Sending 'Message'...")
    	ws.send(message)
#    	print(ws.recv())
#    	print("Sent")
	ws.close()

def event_notification(source, event):
    #pprint(str(event))
    pprint('notify-send "%s" "%s"' % (event.name, event["ConnectedLineNum"]))
    pprint('notify-send "%s" "%s"' % (event.name, event["ConnectedLineName"]))
    sayCLI(event["ConnectedLineName"]) 

client = AMIClient(**connection)
future = client.login(**login)
if future.response.is_error():
    raise Exception(str(future.response))

client.add_event_listener(EventListener(on_event=event_notification, white_list='Newstate', ChannelStateDesc='Ringing'))

try:
    while True:
        time.sleep(10)
except (KeyboardInterrupt, SystemExit):
    client.logoff()

