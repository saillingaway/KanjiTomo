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

apiURL = 'http://jisho.org/api/v1/search/words?keyword='

def load_config():
    config = configparser.ConfigParser()
    config.read('tomo.ini')
    nickname = config.get('TWITCH', 'nickname')
    channel = config.get('TWITCH', 'channel')
    token = config.get('TWITCH', 'token')
    return nickname, channel, token


def print_tree(tree):
    """pretty-print the tokens"""
    for chunk in tree:
        for token in chunk:
            pprint(vars(token))
            print(vars(token)['genkei'])


def analyze_msg(message):
    """Applies NLP Cabocha to the passed message and return resulting tree."""
    analyzer = CaboChaAnalyzer()
    return analyzer.parse(message)


def parse(tree):
    """Iterates through the tree to extract their base forms and returns
       the resulting list of strings"""
    tokens = []
    chunks = []
    for chunk in tree:
        tokenstr = ""
        for token in chunk:
            # chunk_genkei.append(vars(token)['genkei'])
            tokens.append(token.genkei)
            tokenstr += token.genkei
        chunks.append(tokenstr)
    if tokens[-1] == "*":
        tokens.pop()  # to remove the trailing '*' element
    if chunks[-1] == "*":
        chunks.pop()
    return chunks, tokens


async def askJisho(tokens):
    """Queries Jisho for the kanji"""
    data = {}
    url = 'http://jisho.org/api/v1/search/words?keyword=\"'
    for word in tokens:
        # s = word['genkei']
        response = requests.get(apiURL + s)
        data[word] = json.loads(response.content.decode('utf-8'))['data']
        # json.loads(response.content.decode())['data'][i]['slug']
    return data


async def openJisho(message):
    """Opens Jisho.org in a browser with the full chat message"""
    search = urllib.parse.quote(message)
    url = "http://jisho.org/search/" + search
    webbrowser.open(url)


def getSenses(data):
    """Iterates through the responses from Jisho and picks out
       the correct slug and it's english senses.
    """
    # for word in data:
    #     # json.loads(response.content.decode())['data'][i]['slug']
    #     i = 0
    #     for i in word:
    #         # if word[i]['slug'] ==


async def listenForMessages(s):
    """Listens for message on the socket"""
    while True:
        resp = s.recv(2048).decode('utf-8')
        # to ensure connection to server isn't prematurely terminated:
        if resp.startswith('PING'):
            s.send("PONG\n".encode('utf-8'))
        elif len(resp) > 0:
            # parse the message
            result = re.search(':(.*)!.*@.*.tmi.twitch.tv PRIVMSG #(.*) :(.*)', resp)
            if result:
                # extract tokens from message and put them into a list
                username, channel, message = result.groups()
                await openJisho(message)
                tree = analyze_msg(message)
                chunks = tree.chunks
                tokens = tree.tokens
                chunk_list, token_list = parse(tree)
                pprint(chunk_list)
                pprint(token_list)
                # using the JishoAPI, query the word in the list
                # words = await askJisho(tokens)
                # words2 = await askJisho(chunks)
            else:
                print("parse failed")


async def main():
    # load credentials from the config file
    nickname, channel, token = load_config()
    server = 'irc.chat.twitch.tv'
    port = 6667

    # connect session and setting up socket to listen for messages in chat
    s = socket.socket()
    s.connect((server, port))
    s.send(f"PASS {token}\n".encode('utf-8'))
    s.send(f"NICK {nickname}\n".encode('utf-8'))
    s.send(f"JOIN {channel}\n".encode('utf-8'))
    await listenForMessages(s)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
