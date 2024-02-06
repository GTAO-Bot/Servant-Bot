import nextcord
from nextcord.ext import commands
from nextcord.ext import tasks

import asyncio

from API import devUsers

class mischallenousCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help=" -> Get information about a specific user",  hidden=True)
    async def info(self, ctx, userid=None,):
        if ctx.author.id not in devUsers:
            return
        if userid == None or userid == ctx.author.id:
            await ctx.reply("Why are you researching yourself? :face_with_raised_eyebrow:")
            userid = ctx.author.id
        user = await self.bot.fetch_user(userid)
        badges = []
        badgesList = user.public_flags.all()
        for each in badgesList:
            badges.append(each.name)
        badges = ", ".join(badges)
        badges = "None" if badges == "" else badges
        guilds = []
        for each in user.mutual_guilds:
            guilds.append(each.name)
        guilds = ", ".join(guilds)
        guilds = "None" if guilds == "" else guilds
        description = f'''
    Info on {user.mention}
    ```
     ╔═══════════════════════════╦════════════════
     ║ Name                      ║  {user.name}
     ║ Global Name               ║  {user.global_name}
     ║ Display Name              ║  {user.display_name}
     ║ Discriminator             ║  {user.discriminator}
     ║ ID                        ║  {user.id}
     ║ Bot?                      ║  {user.bot}
     ║ System?                   ║  {user.system}
     ║ Mutual Guilds (with Bot)  ║  {guilds}
     ║ Accent Color              ║  {user.accent_color}
     ║ Avatar                    ║  {user.avatar}
     ║ Banner                    ║  {user.banner}
     ║ Color                     ║  {user.color}
     ║ Created At                ║  {user.created_at}
     ║ Default Avatar            ║  {user.default_avatar}
     ║ Display Avatar            ║  {user.display_avatar}
     ║ Mention                   ║  {user.mention}
     ║ Badges                    ║  {badges}
     ╚═══════════════════════════╩══════════════
    ```
    '''
        await ctx.send(description)


    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        if isinstance(thread.parent, nextcord.ForumChannel):
            if thread.parent_id in [1192066530263961631, 1195348626944295032]:
                await thread.send(f'Thread auto add: <@&1128392572788813907>')

    @commands.command(help=" -> Purge x last messages",  hidden=True)
    async def purge(self, ctx, count: int):
        deleted = await ctx.channel.purge(limit=count+1)
        await ctx.send(f'Deleted {len(deleted)-1} message(s)', delete_after=3)

    @commands.command(help=" -> Archive a dev discussion thread",  hidden=True)
    async def archive(self, ctx, *reason):
        await ctx.send(f'<@&1128392572788813907>, {ctx.author.mention} archived the thread.\nReason: {" ".join(reason)}')
        await ctx.channel.edit(archived=True)

    @commands.command(help=" -> Get Bot Ping")
    async def ping(ctx, *, code=None):
        x = await ctx.send("Pong in <a:loading:1184992104108281977>")
        await asyncio.sleep(1)
        await x.edit(f'Pong! In {round(self.bot.latency * 1000)}ms')

def setup(bot):
    bot.add_cog(mischallenousCog(bot))
