import cabocha
import asyncio
from cabocha.analyzer import CaboChaAnalyzer
import configparser
from configparser import ConfigParser
import json
from pprint import pprint
import re
import requests
import socket
import urllib
import webbrowser

def loadConfig():
    config = configparser.ConfigParser()
    config.read('tomo.ini')
    nickname = config.get('TWITCH', 'nickname')
    channel = config.get('TWITCH', 'channel')
    token = config.get('TWITCH', 'token')
    return nickname, channel, token


"""pretty-print the tokens"""
def printTree(tree):
    for chunk in tree:
        for token in chunk:
            pprint(vars(token))
            print(vars(token)['genkei'])


"""Tokenizes a message and returns the resulting tree"""
def tokenizeTree(tree):
    tokenList = []
    for chunk in tree:
        for token in chunk:
            tokenList.append(vars(token)['genkei'])
    tokenList.pop()     # to remove the trailing '*' element
    return tokenList


"""takes a message (string) and returns a list of the generated tokens as strings"""
def tokenizeMessage(message):
    analyzer = CaboChaAnalyzer()
    tree = analyzer.parse(message)
    return tokenizeTree(tree)


"""query the tokens that are kanji"""
async def askJisho(tokenList):
    data = {}
    url = 'http://jisho.org/api/v1/search/words?keyword=\"'
    for word in tokenList:
        response = requests.get('http://jisho.org/api/v1/search/words?keyword=\"' + word)
        pprint(response.data)
        # json.loads(response.content.decode())['data']
        # json.loads(response.content.decode())['data'][i]['slug']


"""opens Jisho.org in a browser with the full chat message"""
async def openJisho(message):
    search = urllib.parse.quote(message)
    url = "http://jisho.org/search/" + search
    webbrowser.open(url)


"""constantly listen for message on the socket"""
async def listenForMessages(s):
    while True:
        resp = s.recv(2048).decode('utf-8')
        # to ensure connection to server isn't prematurely terminated
        if resp.startswith('PING'):
            s.send("PONG\n".encode('utf-8'))
        elif len(resp) > 0:
            # parse the message
            result = re.search(':(.*)!.*@.*.tmi.twitch.tv PRIVMSG #(.*) :(.*)', resp)
            if result:
                # extract tokens from message and put them into a list
                username, channel, message = result.groups()
                await openJisho(message)
                tokenList = tokenizeMessage(message)
                print(tokenList)
                # using the JishoAPI, query the word in the list
                words = await askJisho(tokenList)
            else:
                print("parse failed")


async def main():
    # load credentials from the config file
    nickname, channel, token = loadConfig()

    server = 'irc.chat.twitch.tv'
    port = 6667

    # connect session and setting up socket to listen for messages in chat
    s = socket.socket()
    s.connect((server, port))
    s.send(f"PASS {token}\n".encode('utf-8'))
    s.send(f"NICK {nickname}\n".encode('utf-8'))
    s.send(f"JOIN {channel}\n".encode('utf-8'))

    await listenForMessages(s)


if __name__=="__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())