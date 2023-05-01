

import discord
import tsparse

TOKEN = '# Type Token Here'

class MyClient(discord.Client):
    async def on_ready(self):
        global ParseObject
        ParseObject = tsparse.TSParser()
        print('We have logged in as {0.user}'.format(client))


    async def on_message(self, message):
        if message.author != client.user:
            user = message.author
            msg = message.content
            reply = ParseObject.parseMessage(user, msg)
            await message.channel.send(reply)
        

if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)
    client.run(TOKEN)