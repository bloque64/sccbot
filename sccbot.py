import discord

import discord
from discord.ext import commands
import secrets
from secrets import token_hex
from settings import Settings
import data

__author__ = "@pgarcgo"
__version__ = "0.1"

name = "Steem Community Curation BOT"
steem_curation_account = "sccb"


my_settings = Settings()
my_settings.load()

TOKEN = my_settings.discord_token


bot = commands.Bot(command_prefix='!') 

# @bot.event
# async def on_message(message):
    
#     if(message.author == bot.user):
#         return
        
#     print(dir(message.channel))


@bot.command
async def init(ctx):
    await ctx.send("Inicitalizing channel structure...")
    

@bot.command()
async def reg(ctx, account_name):
    print("Reg...")
    await ctx.send("Associendo tu cuenta de discord con la cuenta en Steem: " + account_name)
    register_token = token_hex(16)
    msg = "Manda 0.001 SBD a la cuenta ***"  + steem_curation_account + "*** con este Memo: " + register_token + " y ejecuta el comando ***!verifica " + account_name + "*** para finlizar el registro"
    await ctx.send(msg)
    

@bot.command()
async def faa(ctx):
    await ctx.send('Bye')

@bot.command()
async def foo(ctx):
    await ctx.send('Hello')
    
print("Runnng bot...")
bot.run(TOKEN)