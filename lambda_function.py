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
import requests
from fuzzywuzzy import fuzz
# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
try:
    sky_box_name = environ['SKY_BOX_NAME']
except:
    sky_box_name = 'Sky Box'

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
        "friendlyName": sky_box_name,
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
        "applianceId": "skyq-netflix",
        "manufacturerName": "Sky",
        "version": "1",
        "friendlyName": "Netflix",
        "description": "Netflix scene via Sky Q",
        "isReachable": True,
        "displayCategories":["SCENE_TRIGGER"],
        "actions": [
            "turnOn",
            "turnOff"
            ],
        "cookie": {}
    },
    {
        "applianceId": "skyq-youtube",
        "manufacturerName": "Sky",
        "version": "1",
        "friendlyName": "YouTube",
        "description": "YouTube scene via Sky Q",
        "isReachable": True,
        "displayCategories":["SCENE_TRIGGER"],
        "actions": [
            "turnOn",
            "turnOff"
            ],
        "cookie": {}
    },
    {
        "applianceId": "skyq-spotify",
        "manufacturerName": "Sky",
        "version": "1",
        "friendlyName": "Spotify",
        "description": "Spotify scene via Sky Q",
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


def get_channels_file(url):
    if url.startswith('http'):
        r = requests.get(url)
        channels = r.json()
    else:
        with open(url) as f:
            channels = json.load(f)
    return channels


def get_channels():
    if 'CHANNELS_FILE' in environ:
        url = environ['CHANNELS_FILE']
    elif 'Italia' in environ:
        url = 'https://raw.githubusercontent.com/ndg63276/alexa-sky-hd/master/channels-it.json'
    else:
        url = 'http://epgservices.sky.com/5.1.1/api/2.1/region/json/4101/1/'
    channels_json = get_channels_file(url)
    if 'init' in channels_json:
        channels = parse_channels_json(channels_json)
    else:
        channels = channels_json
    return channels


def parse_channels_json(channels_json):
    chan_list = channels_json['init']['channels']
    channels = {}
    for chan in chan_list:
        names = []
        names.append(chan['t'])
        if chan['lcn'] is not None:
            names.append(str(chan['lcn']))
        replacements = [('f1','f. one'),('one','1'),('two','2'),('three','3'),('four','4'),
                        ('five','5'),('syfy','sci-fi'),('skypremierehd','sky premiere hd'),('sky prem+1','sky premiere+1')]
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
    hd = False
    if 'HD' in environ and environ['HD'] == 'True':
        hd = True
    plus_one_request = False
    if ' plus one' in channel_request:
        plus_one_request = channel_request.replace(' plus one', '')
    print "plus_one_request: "+str(plus_one_request)
    best_score = 0
    best_plus_one_score = 0
    for key in channels.keys():
        for chan in channels[key]:
            score = fuzz.ratio(chan.lower(), channel_request.lower())
            if score > best_score:
                best_score = score
                channel_number = key
                print 'normal', channel_number, score
            if hd:
                score = fuzz.ratio(chan.lower(), channel_request.lower()+' hd')
                if score >= best_score:
                    best_score = score
                    channel_number = key
                    print 'hd', channel_number, score
            if plus_one_request:
                plus_one_score = fuzz.ratio(chan.lower(), plus_one_request.lower())
                if plus_one_score > best_plus_one_score:
                    best_plus_one_score = plus_one_score
                    plus_one_channel_number = key
                    print 'plus_one', plus_one_channel_number, plus_one_score
        if best_score == 100:
            break
    if plus_one_request:
        if best_plus_one_score > best_score and plus_one_channel_number < 200:
            channel_number = plus_one_channel_number + 100
    return channel_number


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
    request_namespace = request["directive"]["header"]["namespace"]
    request_name = request["directive"]["header"]["name"]
    endpointId = request['directive']['endpoint']['endpointId']
    namespace = "Alexa"
    name = "Response"
    commands = []
    properties = []
    
    if request_namespace == "Alexa.PowerController":
        response_name = "powerState"
        if request_name == "TurnOn":
            commands.append('sky')
            value = "ON"
        else:
            commands.append('sky')
            commands.append('power')
            value = "OFF"
        properties = [ {
            "namespace": "Alexa.PowerController",
            "name": "powerState",
            "value": value,
            "timeOfSample": get_utc_timestamp(),
            "uncertaintyInMilliseconds": 500
        } ]
    elif request_namespace == "Alexa.KeypadController":
        keystroke = request["directive"]["payload"]["keystroke"]
        if keystroke == "SELECT":
            commands.append("select")
        if keystroke == "INFO" or keystroke == "MORE":
            commands.append("i")

    elif request_namespace == "Alexa.PlaybackController":
        if request_name == "Play":
            commands.append("play")
        elif request_name == "Pause":
            commands.append("pause")
        elif request_name == "FastForward":
            commands.append("fastforward")
        elif request_name == "Rewind":
            commands.append("rewind")
        elif request_name == "Stop":
            commands.append("backup")

    elif request_namespace == "Alexa.ChannelController":
        if request_name == "ChangeChannel":
            if 'name' in request["directive"]["payload"]["channelMetadata"]:
                channel_request = request["directive"]["payload"]["channelMetadata"]["name"]
            elif 'number' in request["directive"]["payload"]["channel"]:
                channel_request = request["directive"]["payload"]["channel"]["number"]
            else:
                return make_response(request, [])
            if 'on '+sky_box_name.lower() in channel_request:
                channel_request = channel_request.replace('on '+sky_box_name.lower(),'')
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
            for i in str(channel_number):
                commands.append(i)

        elif request_name == "SkipChannels":
            increment = request["directive"]["payload"]["channelCount"]
            if increment == 1:
                commands.append('channelup')
            if increment == -1:
                commands.append('channeldown')

    elif request_namespace == "Alexa.SceneController":
        namespace = request["directive"]["header"]["namespace"]
        if endpointId == "skybox-tvguide":
            if request_name == "Activate":
                commands.append('tvguide')
                commands.append('select')
                commands.append('select')
                name = "ActivationStarted"
            if request_name == "Deactivate":
                commands.append('sky')
                name = "DeactivationStarted"
        elif endpointId == "skyq-netflix":
            if request_name == "Activate":
                commands=['tvguide','sleep','right','down','down','down','down','down','select']
                name = "ActivationStarted"
            if request_name == "Deactivate":
                commands.append('sky')
                name = "DeactivationStarted"
        elif endpointId == "skyq-spotify":
            if request_name == "Activate":
                commands=['tvguide','sleep','right','down','down','down','down','down','right','select']
                name = "ActivationStarted"
            if request_name == "Deactivate":
                commands.append('sky')
                name = "DeactivationStarted"
        elif endpointId == "skyq-youtube":
            if request_name == "Activate":
                commands=['tvguide','sleep','right','down','down','down','down','down','right','right','select']
                name = "ActivationStarted"
            if request_name == "Deactivate":
                commands.append('sky')
                name = "DeactivationStarted"
        elif endpointId == "skybox-subtitles":
            if request_name == "Activate":
                name = "ActivationStarted"
            if request_name == "Deactivate":
                name = "DeactivationStarted"       
            commands.append('help')
            commands.append('down')
            commands.append('right')
            commands.append('select')
        elif endpointId == "skybox-audio-description":
            if request_name == "Activate":
                name = "ActivationStarted"
            if request_name == "Deactivate":
                name = "DeactivationStarted"       
            commands.append('help')
            commands.append('right')
            commands.append('select')
        elif endpointId == "skybox-info":
            if request_name == "Activate":
                name = "ActivationStarted"
            if request_name == "Deactivate":
                name = "DeactivationStarted"       
            commands.append('i')
    for command in commands:
        send_command(command, endpointId)
    return make_response(request, properties, namespace, name)


def make_response(request, properties, namespace, name):       
    response = {
        "context": {
            "properties": properties
        },
        "event": {
            "header": {
                "messageId": get_uuid(),
                "correlationToken": request["directive"]["header"]["correlationToken"],
                "namespace": namespace,
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


def send_command(command, endpointId=''):
    if command == 'sleep':
        time.sleep(1)
        return
    code=commands[command]
    commandBytes = [4,1,0,0,0,0,224 + (code/16), code % 16]
    b=bytearray()
    for i in commandBytes:
        b.append(i)
    l = 12
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(environ['PORT'])
    if endpointId == 'skybox-002':
        port = int(environ['PORT_2'])
    s.connect((environ['HOST'], port))
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
                    "proactivelyReported": False,
                    "retrievable": False
                }
            },
            {  
                "type": "AlexaInterface",
                "interface": "Alexa.ChannelController",
                "version": "1.0",
                "properties": {
                    "supported": [
                        { "name":"channel" }
                    ]
                }
            },
            {  
                 "type": "AlexaInterface",
                 "interface": "Alexa.PlaybackController",
                 "version": "1.0",
                 "properties": { },
                 "supportedOperations": ["Play", "Pause", "Rewind", "FastForward", "Stop"]
            },
            {
                "type": "AlexaInterface",
                "interface": "Alexa.KeypadController",
                "version": "3",
                "keys": [
                    "INFO", "MORE", "SELECT",
                    "UP", "DOWN", "LEFT", "RIGHT",
                    "PAGE_UP", "PAGE_DOWN", "PAGE_LEFT", "PAGE_RIGHT"
                ]
            },
        ]

    elif displayCategories == ["SCENE_TRIGGER"]:
        capabilities = [
            {
              "type": "AlexaInterface",
              "interface": "Alexa.SceneController",
              "version" : "3",
              "supportsDeactivation" : True,
              "proactivelyReported" : False
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
            "proactivelyReported": False,
            "retrievable": False
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

