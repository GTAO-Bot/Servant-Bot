import nextcord
from nextcord.ext import commands

from aioconsole import aexec
import io
import contextlib
from traceback import format_exception
import time

from API import bot_token

class evalCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help=" -> Evalute some code", hidden=True)
    async def eval(self, ctx, *, code=None):
        if ctx.author.id not in self.bot.allowed:
            return

        if code is None or code == '':
            await ctx.send_help(ctx.command)
            return

        if '```py' in code:
            code = code[5:]
            code = code[:-3]
        elif '```' in code:
            code = code[3:]
            code = code[:-3]

        stdout = io.StringIO()

        start_time = time.perf_counter()

        try:
            with contextlib.redirect_stdout(stdout):
                r = await aexec(code)
                r = f"{stdout.getvalue()}"

            result = r.splitlines()

            def formatter(line):
                return f' > {line}'

            result = map(formatter, result)
            result = '\n'.join(result)
            errors_found = False
        except Exception as e:
            r = "".join(format_exception(e, e, e.__traceback__))
            result = e
            errors_found = True

        end_time = time.perf_counter()
        total_time = float(f"{round((end_time - start_time), 2)}")

        content = f'''```
{result}
```
Time Taken to execute Code: {total_time+0.1} s
Errors Found: {errors_found}
'''
        if bot_token in content:
            await ctx.send('Error, Access Denied')
            return

        embed = nextcord.Embed(
            title='Eval Result',
            description=content, 
            color=0x00aa00
        )
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(evalCommand(bot))
