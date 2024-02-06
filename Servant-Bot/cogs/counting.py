import nextcord
from nextcord.ext import commands
from nextcord.ext import tasks

from requests import post

class countingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loopsStarted = False
        self.supportServer = {
            'webhook': 'https://discord.com/api/webhooks/1203826499040452639/jbtGukvxjE5zNRHIR1N8v4FRm1LIXuby3bnZOShSeFqMAiCa0V3nleLb0RQFO5h05jH5',
            'number': None
        }

    @commands.Cog.listener(name='on_ready')
    async def loops_starter(self):
        if not self.loopsStarted:
            while True:
                channel = await self.bot.fetch_channel(1195668273782595625)
                async for msg in channel.history(limit=50):
                    if msg.author.id in [1203826499040452639, 856143242922950667]:
                        break
                if 'Count: ' in msg.content:
                    count = msg.content[7:]
                    count = count.replace(',', '')
                    self.supportServer['number'] = int(count)+1
                    break
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

