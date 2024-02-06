import nextcord
from nextcord.ext import commands
from nextcord.ext import tasks

import asyncio
from requests import get, post

import API

class countingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loopsStarted = False
        self.supportServer = {
            'webhook': API.supportServerWebhook,
            'number': None,
            'webhookChannelID': None
        }

    @commands.Cog.listener(name='on_message')
    async def commandsHandler(self, msg):
        c = msg.content
        if msg.channel.id != self.supportServer['webhookChannelID'] or msg.author.id != API.devUsers[0]:
            return
        if c == 'stop counting':
            self.webhookSender.stop()
            await msg.reply('Stopped Counting')
        elif c == 'start counting':
            if self.webhookSender.is_running():
                await msg.reply('Already running')
            else:
                self.webhookSender.start()
                await msg.reply('Started Counting')
        elif c == 'restart counting':
            if self.webhookSender.is_running:
                self.webhookSender.stop()
            await self.loops_starter()

    @commands.Cog.listener(name='on_ready')
    async def loops_starter(self):
        self.supportServer['webhookChannelID'] = int(get(self.supportServer['webhook']).json()['channel_id'])
        self.supportServer['webhookID'] = int(get(self.supportServer['webhook']).json()['user']['id'])
        if not self.loopsStarted:
            tries = 0
            while True:
                tries+=1
                channel = await self.bot.fetch_channel(self.supportServer['webhookChannelID'])
                async for msg in channel.history(limit=50):
                    if msg.author.id in [self.supportServer['webhookID'], API.devUsers[0]] and 'Count: ' in msg.content:
                        break
                if 'Count: ' in msg.content:
                    count = msg.content[7:]
                    count = count.replace(',', '')
                    self.supportServer['number'] = int(count)+1
                    print(count)
                    print(self.supportServer['number'])
                    break

                if tries == 10: 
                    await channel.send('Couldn`t restart counting :sob:')
                    return

                await asyncio.sleep(30)

            self.webhookSender.start()
            self.loopsStarted = True


    @tasks.loop(seconds=3)
    async def webhookSender(self):
        post(
            url=self.supportServer['webhook'],
            headers={
                "Content-Type":"application/json"
            }, 
            json={
                "content":f"Count: {self.supportServer['number']:,}"
            }
        )
        self.supportServer['number']+=1


def setup(bot):
    bot.add_cog(countingCog(bot))

