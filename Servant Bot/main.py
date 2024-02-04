import nextcord
from nextcord.ext import commands
from nextcord import Interaction

import time
import asyncio

from API import bot_token, devUsers

intents = nextcord.Intents().default()
intents.message_content = True

bot = commands.Bot(
    command_prefix=[">"], 
    intents=intents, 
    case_insensitive=True, 
    status=nextcord.Status.online
)

bot.allowed = devUsers

@bot.event
async def on_ready():
    print(f'{bot.user} is online in {len(bot.guilds)} guild.')
    bot.add_view(button())
    bot.add_view(colorsButton())


bot.load_extension('cogs.counting')
bot.load_extension('cogs.eval')
bot.load_extension('cogs.miscellaneous')



class button(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        for numb in range(1,26):
            self.add_item(callback(label=f"{numb}", custom_id=f"button-{numb*69}"))

class callback(nextcord.ui.Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def callback(self, interaction: Interaction):
        self.label = f"{int(self.label)+1}"
        await interaction.response.edit_message(view=self.view)

class colorsButton(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.colors = [nextcord.ButtonStyle.green, nextcord.ButtonStyle.red, nextcord.ButtonStyle.blurple, nextcord.ButtonStyle.gray]
        for numb in range(0,4):
            self.add_item(callbackColors(label="⠀", custom_id=f"button-{numb*69}", style=self.colors[numb]))

class callbackColors(nextcord.ui.Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def callback(self, interaction: Interaction):
        self.colors = self.view.colors
        index = self.colors.index(self.style) + 1 if self.colors.index(self.style) != 3 else 0
        self.style = self.colors[index]
        await interaction.response.edit_message(view=self.view)


@bot.command(help=" -> Buttons Game")
async def buttons(ctx):
    await ctx.send(content="Press the button.",view=button())


@bot.command(help=" -> Color Buttons Game")
async def colors(ctx):
    await ctx.send(content="Press the button to change the color.",view=colorsButton())


while True:
	bot.run(bot_token)