import discord 
import os 

key = "OTk4MjU0NTExOTM0MTYxMDM2.GoMVDD.xvSOjNsxg4Qea7Fc8sWPto2_bRxN0U0xdId8HI"

from discord.ext import commands

bot = commands.Bot(command_prefix='-')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


bot.run(key)