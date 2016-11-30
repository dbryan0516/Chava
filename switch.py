#!/usr/bin/env python
#
#
# @author Dylan Bryan
# Used to turn the TP-Link HS-100 or HS-110 on or off
# Executing this program will change the state of the outlet

import json
import socket


# Set target IP, port and command to send
ip = '192.168.0.19'
port = 9999


def validIP(ip):
    try:
        socket.inet_pton(socket.AF_INET, ip)
    except socket.error:
        parser.error("Invalid IP Address.")
    return ip


def encrypt(string):
    key = 171
    result = "\0\0\0\0"
    for i in string:
        a = key ^ ord(i)
        key = a
        result += chr(a)
    return result


def decrypt(string):
    key = 171
    result = ""
    for i in string:
        a = key ^ ord(i)
        key = ord(i)
        result += chr(a)
    return result


def sendRequest(request):
    try:
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_tcp.connect((ip, port))
        sock_tcp.send(encrypt(request))
        response = sock_tcp.recv(4096)
        sock_tcp.close()
        return response
    except socket.error:
        quit("Cound not connect to host " + ip + ":" + str(port))


# Gets the info of the switch and returns the state; 1 is on, 0 is off
def getState():
    request = '{"system":{"get_sysinfo":{}}}'
    enResponse = sendRequest(request)
    response = json.loads(decrypt(enResponse[4:]))
    return response['system']['get_sysinfo']['relay_state']

# Switches the outlet depending on the state


def switch(state):

    if (state == 0):
        request = '{"system":{"set_relay_state":{"state":1}}}'
    else:
        request = '{"system":{"set_relay_state":{"state":0}}}'

    enResponse = sendRequest(request)
    response = json.loads(decrypt(enResponse[4:]))
    if (response['system']['set_relay_state']['err_code'] > 0):
        print 'Something went wrong'

validIP(ip)
state = getState()

switch(state)
