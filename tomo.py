import pytmi

config = {
    'username': "kanjiFriendBot", # botname
    'password': "oauth:<token>", #oauthstring
    'channels': ["#<channel-name>"] # channelname
}

client = pytmi.TwitchClient()

@client.event
async def on_message(message):
    print("message: ", message.content)

client.run_sync(**config)
