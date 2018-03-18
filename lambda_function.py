# -*- coding: utf-8 -*-
"""
channels_that_dont_work:
ITV3 (chup)
Sky Sports Mix
Sky One+1
ITV1+1 (chup)
"""

import logging
import time
import json
import uuid
import socket
from os import environ
from botocore.vendored import requests
from fuzzywuzzy import fuzz
# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

commands = {
        "power": 0,
        "select": 1,
        "backup": 2,
        "dismiss": 2,
        "channelup": 6,
        "channeldown": 7,
        "interactive": 8,
        "sidebar": 8,
        "help": 9,
        "services": 10,
        "search": 10,
        "tvguide": 11,
        "home": 11,
        "i": 14,
        "text": 15, 
        "up": 16,
        "down": 17,
        "left": 18,
        "right": 19,
        "red": 32,
        "green": 33,
        "yellow": 34,
        "blue": 35,
        "0": 48,
        "1": 49,
        "2": 50,
        "3": 51,
        "4": 52,
        "5": 53,
        "6": 54,
        "7": 55,
        "8": 56,
        "9": 57,
        "play": 64,
        "pause": 65,
        "stop": 66,
        "record": 67,
        "fastforward": 69,
        "rewind": 71,
        "boxoffice": 240,
        "sky": 241
}


appliances = [
    {
        "applianceId": "skybox-001",
        "manufacturerName": "Sky",
        "modelName": "Digibox",
        "version": "1",
        "friendlyName": "Sky Box",
        "description": "Sky Digibox",
        "isReachable": True,
        "displayCategories":["TV"],
        "actions": [
            "turnOn",
            "turnOff",
            ],
        "cookie": {}
    },
    {
        "applianceId": "skybox-tvguide",
        "manufacturerName": "Sky",
        "version": "1",
        "friendlyName": "TV Guide",
        "description": "Sky TV Guide scene via Sky Digibox",
        "isReachable": True,
        "displayCategories":["SCENE_TRIGGER"],
        "actions": [
            "turnOn",
            "turnOff"
            ],
        "cookie": {}
    },
        {
        "applianceId": "skybox-subtitles",
        "manufacturerName": "Sky",
        "version": "1",
        "friendlyName": "Subtitles",
        "description": "Sky Subtitles scene via Sky Digibox",
        "isReachable": True,
        "displayCategories":["SCENE_TRIGGER"],
        "actions": [
            "turnOn",
            "turnOff"
            ],
        "cookie": {}
    },
    {
        "applianceId": "skybox-audio-description",
        "manufacturerName": "Sky",
        "version": "1",
        "friendlyName": "Audio Description",
        "description": "Sky Audio Description scene via Sky Digibox",
        "isReachable": True,
        "displayCategories":["SCENE_TRIGGER"],
        "actions": [
            "turnOn",
            "turnOff"
            ],
        "cookie": {}
    },
    {
        "applianceId": "skybox-info",
        "manufacturerName": "Sky",
        "version": "1",
        "friendlyName": "Info",
        "description": "Sky Info scene via Sky Digibox",
        "isReachable": True,
        "displayCategories":["SCENE_TRIGGER"],
        "actions": [
            "turnOn",
            "turnOff"
            ],
        "cookie": {}
    }
    ]


def lambda_handler(request, context):
    """Main Lambda handler.

    Since you can expect both v2 and v3 directives for a period of time during the migration
    and transition of your existing users, this main Lambda handler must be modified to support
    both v2 and v3 requests.
    """

    try:
        logger.info("Directive:")
        logger.info(json.dumps(request, indent=4, sort_keys=True))

        if request["directive"]["header"]["name"] == "Discover":
            response = handle_discovery(request)
        else:
            response = handle_non_discovery(request)

        logger.info("Response:")
        logger.info(json.dumps(response, indent=4, sort_keys=True))

        return response
    except ValueError as error:
        logger.error(error)
        raise

def get_utc_timestamp(seconds=None):
    return time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime(seconds))

def get_uuid():
    return str(uuid.uuid4())
    
def get_channels():
    url = 'http://tv.sky.com/channel/index/4101-1'
    a = requests.get(url)
    chan_list = a.json()['init']['channels']
    channels = {}
    for chan in chan_list:
        names = []
        names.append(chan['t'])
        names.append(str(chan['lcn']))
        replacements = [('f1','f. one'),('one','1'),('two','2'),('three','3'),('four','4'),
                        ('five','5'),('syfy','sci-fi')]
        for f,r in replacements:
            if f in chan['t'].lower():
                names.append(chan['t'].lower().replace(f,r).replace('+',' plus '))
            if r in chan['t'].lower():
                names.append(chan['t'].lower().replace(r,f).replace('+',' plus '))
            if chan['lcn'] and f in chan['lcn'].lower():
                names.append(chan['t'].lower().replace(f,r).replace('+',' plus '))
            if chan['lcn'] and r in chan['lcn'].lower():
                names.append(chan['t'].lower().replace(r,f).replace('+',' plus '))
        chan_number = chan['c'][1]
        channels[chan_number] = names
    return channels

def get_channel_number(channels, channel_request):
    hd = environ['HD'] == 'True'
    best_score = 0
    for key in channels.keys():
        for chan in channels[key]:
            score = fuzz.ratio(chan.lower(), channel_request.lower())
            if score > best_score:
                best_score = score
                channel_number = key
            if hd:
                score = fuzz.ratio(chan.lower(), channel_request.lower()+' hd')
                if score >= best_score:
                    best_score = score
                    channel_number = key
    return channel_number

# v3 handlers
def handle_discovery(request):
    endpoints = []
    for appliance in appliances:
        endpoints.append(get_endpoint(appliance))

    response = {
        "event": {
            "header": {
                "namespace": "Alexa.Discovery",
                "name": "Discover.Response",
                "payloadVersion": "3",
                "messageId": get_uuid()
                },
            "payload": {
                "endpoints": endpoints
                }
            }
        }
    return response

def handle_non_discovery(request):
    print("***")
    print(request)
    print("***")
    request_namespace = request["directive"]["header"]["namespace"]
    request_name = request["directive"]["header"]["name"]

    if request_namespace == "Alexa.PowerController":
        response_name = "powerState"
        if request_name == "TurnOn":
            value = "ON"
            command = 'sky'
        else:
            value = "OFF"
            command = 'power'
        properties = [ {
                        "namespace": request_namespace,
                        "name": response_name,
                        "value": value,
                        "timeOfSample": get_utc_timestamp(),
                        "uncertaintyInMilliseconds": 500
                    } ]
        print properties
        send_command(command)
            
    elif request_namespace == "Alexa.PlaybackController":
        if request_name == "Play":
            command="play"
        elif request_name == "Pause":
            command="pause"
        elif request_name == "FastForward":
            command="fastforward"
        elif request_name == "Rewind":
            command="rewind"
        elif request_name == "Stop":
            command="backup"
        send_command(command)
        properties = []
    
    elif request_namespace == "Alexa.ChannelController":
        if request_name == "ChangeChannel":
            if 'name' in request["directive"]["payload"]["channelMetadata"]:
                channel_request = request["directive"]["payload"]["channelMetadata"]["name"]
            elif 'number' in request["directive"]["payload"]["channel"]:
                channel_request = request["directive"]["payload"]["channel"]["number"]
            else:
                return make_response(request, [])
            if 'on sky box' in channel_request:
                channel_request = channel_request.replace('on sky box','')
            print("channel_request: "+channel_request)
            channel_number = None
            channels = get_channels()
            try:
                channel_number = int(channel_request)
                if channel_number < 100:
                    channel_request = 'channel '+channel_request
                    raise
            except:
                channel_number = get_channel_number(channels, channel_request)
            channel_name = channels[channel_number][0]
            for i in str(channel_number):
                send_command(i)
            properties = [ {
                        "namespace": request_namespace,
                        "name": "channel",
                        "value": {
                            "number": str(channel_number),
                            "callSign": channel_name,
                            },
                        "timeOfSample": get_utc_timestamp(),
                        "uncertaintyInMilliseconds": 500
                    } ]
        elif request_name == "SkipChannels":
            increment = request["directive"]["payload"]["channelCount"]
            properties = []
            if increment == 1:
                send_command('channelup')
            if increment == -1:
                send_command('channeldown')

    elif request_namespace == "Alexa.SceneController":
        endpointId = request['directive']['endpoint']['endpointId']
        if endpointId == "skybox-tvguide":
            if request_name == "Activate":
                send_command('tvguide')
                send_command('select')
                send_command('select')
                name = "ActivationStarted"
            if request_name == "Deactivate":
                send_command('sky')
                name = "DeactivationStarted"
        elif endpointId == "skybox-subtitles":
            if request_name == "Activate":
                name = "ActivationStarted"
            if request_name == "Deactivate":
                name = "DeactivationStarted"       
            send_command('help')
            send_command('down')
            send_command('right')
            send_command('select')
        elif endpointId == "skybox-audio-description":
            if request_name == "Activate":
                name = "ActivationStarted"
            if request_name == "Deactivate":
                name = "DeactivationStarted"       
            send_command('help')
            send_command('right')
            send_command('select')
        elif endpointId == "skybox-info":
            if request_name == "Activate":
                name = "ActivationStarted"
            if request_name == "Deactivate":
                name = "DeactivationStarted"       
            send_command('i')
        return make_scene_response(request, name)
    return make_response(request, properties)

def make_scene_response(request, name):
    response = {
        "context" : { },
        "event": {
            "header": {
                "messageId": get_uuid(),
                "correlationToken": request["directive"]["header"]["correlationToken"],
                "namespace": request["directive"]["header"]["namespace"],
                "name": name,
                "payloadVersion": "3"
            },
            "endpoint": {
                "scope": {
                    "type": "BearerToken",
                    "token": "access-token-from-Amazon"
                },
                "endpointId": request["directive"]["endpoint"]["endpointId"]
            },
            "payload": {
                "cause" : {
                    "type" : "VOICE_INTERACTION"
                },
                "timestamp" : get_utc_timestamp()
            }
        }
    }
    return response


def make_response(request, properties):       
    response = {
            "context": {
                "properties": properties
            },
            "event": {
                "header": {
                    "namespace": "Alexa",
                    "name": "Response",
                    "payloadVersion": "3",
                    "messageId": get_uuid(),
                    "correlationToken": request["directive"]["header"]["correlationToken"]
                },
                "endpoint": {
                    "scope": {
                        "type": "BearerToken",
                        "token": "access-token-from-Amazon"
                    },
                    "endpointId": request["directive"]["endpoint"]["endpointId"]
                },
                "payload": {}
            }
        }
    return response

def send_command(command):
    code=commands[command]
    commandBytes = [4,1,0,0,0,0,224 + (code/16), code % 16]
    b=bytearray()
    for i in commandBytes:
        b.append(i)
    l = 12
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((environ['HOST'], int(environ['PORT'])))
    recv=s.recv(64)
    while len(recv)<24:
        s.sendall(recv[0:l])
        l = 1
        recv=s.recv(64)
    s.sendall(b)
    commandBytes[1]=0
    b=bytearray()
    for i in commandBytes:
        b.append(i)
    s.sendall(b)
    s.close()

def get_endpoint(appliance):
    endpoint = {
        "endpointId": appliance["applianceId"],
        "manufacturerName": appliance["manufacturerName"],
        "friendlyName": appliance["friendlyName"],
        "description": appliance["description"],
        "displayCategories": appliance["displayCategories"],
        "cookie": appliance["cookie"],
        "capabilities": []
    }
    endpoint["capabilities"] = get_capabilities(appliance)
    return endpoint

def get_capabilities(appliance):
    displayCategories = appliance["displayCategories"]
    if displayCategories == ["TV"]:
        capabilities = [
            {
                "type": "AlexaInterface",
                "interface": "Alexa.PowerController",
                "version": "3",
                "properties": {
                    "supported": [
                        { "name": "powerState" }
                    ],
                    "proactivelyReported": True,
                    "retrievable": True
                }
            },
            {  
                "type":"AlexaInterface",
                "interface":"Alexa.ChannelController",
                "version":"1.0",
                "properties":{  
                    "supported":[  
                       { "name":"channel" }
                    ]
                }
            },
            {  
                     "type":"AlexaInterface",
                     "interface":"Alexa.PlaybackController",
                     "version":"1.0",
                     "properties":{ },
                     "supportedOperations" : ["Play", "Pause", "Rewind", "FastForward", "Stop"] 
            },

        ]

    elif displayCategories == ["SCENE_TRIGGER"]:
        capabilities = [
            {
              "type": "AlexaInterface",
              "interface": "Alexa.SceneController",
              "version" : "3",
              "supportsDeactivation" : True,
              "proactivelyReported" : True
            }
          ]
    # additional capabilities that are required for each endpoint
    endpoint_health_capability = {
        "type": "AlexaInterface",
        "interface": "Alexa.EndpointHealth",
        "version": "3",
        "properties": {
            "supported":[
                { "name":"connectivity" }
            ],
            "proactivelyReported": True,
            "retrievable": True
        }
    }
    alexa_interface_capability = {
        "type": "AlexaInterface",
        "interface": "Alexa",
        "version": "3"
    }
    capabilities.append(endpoint_health_capability)
    capabilities.append(alexa_interface_capability)
    return capabilities