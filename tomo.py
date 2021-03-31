import re
import socket
import cabocha
import requests

from cabocha.analyzer import CaboChaAnalyzer
from pprint import pprint
import pytmi
# from jNlp.jTokenize import jTokenize

"""set up for connecting to the twitch channel chat"""
server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'tomoKanji'
token = 'oauth:<token>'
channel = '#<channel-name>'

"""getting the socket set up to listen for messages in the chat"""
sock = socket.socket()
sock.connect((server, port))

"""connecting"""
sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

"""function to tokenize and return a tree"""
def printTree(tree):
    for chunk in tree:
        for token in chunk:
            pprint(vars(token))
            print(vars(token)['genkei'])


def tokenizeTree(tree):
    tokenList = []
    for chunk in tree:
        for token in chunk:
            tokenList.append(vars(token)['genkei'])
    tokenList.pop()     # to remove the '*' that's
    return tokenList

"""query the tokens that are kanji"""
async def askJisho(tokenList):
    url = 'http://jisho.org/api/v1/search/words?keyword=\"'
    for word in tokenList:
        response = requests.get('http://jisho.org/api/v1/search/words?keyword=\"' + word)



"""constantly listen for message on the socket"""
while True:
    resp = sock.recv(2048).decode('utf-8')

    if resp.startswith('PING'):
        sock.send("PONG\n".encode('utf-8'))

    elif len(resp) > 0:
        #  parse　
        result = re.search(':(.*)!.*@.*.tmi.twitch.tv PRIVMSG #(.*) :(.*)', resp)
        if result:
            username, channel, message = result.groups()
            print("MESSAGE: ", message)
            # list_of_tokens = jTokenize(message)
            # print(', '.join(list_of_tokens).encode('utf-8'))
            analyzer = CaboChaAnalyzer()
            tree = analyzer.parse(message)
            # printTree(tree)
            tokenList = tokenizeTree(tree)
            print(tokenList)
            words = await askJisho(tokenList)
        else:
            print("parse failed")
            # raise SyntaxError('parse failed')


# config = {
#     'username': "kanjiFriendBot", # botname
#     'password': "oauth:<token>", #oauthstring
#     'channels': ["#<channel-name>"] # channelname
# }
#
# client = pytmi.TwitchClient()
#
# @client.event
# async def on_message(message):
#     print("message: ", message.content)
#
# client.run_sync(**config)
