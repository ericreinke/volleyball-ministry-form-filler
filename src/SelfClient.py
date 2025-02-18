
# Need to put self_token and channel IDs here.

import discord
import FormFiller
def client_init_and_start(): # I just wanted to store the token here, thats all
    fillerBot = SelfClient()
    fillerBot.run(self_token)

class SelfClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        #print(message)
        if message.channel.id == COMP_CHANNEL_ID or message.channel.id == CASUAL_CHANNEL_ID or message.channel.id == test_CHANNEL_ID:
            print('Message: ' + message.content)
            start = message.content.find('http')
            space = message.content.find(' ', start)
            newLine = message.content.find('\n', start)
            if space > 0 and newLine > 0:
                end = min(space, newLine)
            else:
                end = max(space, newLine)
            print(start)
            print(end)
            if(start < 0 or end < 0):
                return
            url = message.content[start:end]
            FormFiller.complete_form(url)

