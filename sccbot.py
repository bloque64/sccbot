import discord

import discord
from discord.ext import commands
import secrets
from secrets import token_hex

__author__ = "@pgarcgo"
__version__ = "0.1"

name = "Steem Community Curation BOT"
steem_curation_account = "sccb"

TOKEN = 'NDM0Mzc0NDEwNzcwNTc5NDYy.DbJgIQ.dggA7YLdly30MeSRto-8Z0gbyAE'

#

canales = [{"name":"ciencia", "category":"promocion", "id":0},
           {"name":"gente_nueva", "category":"promocion", "id":0},
           {"name":"ciencia", "category":"post_curables", "id":0},
           {"name":"gente_nueva", "category":"post_curables", "id":0}]


bot = commands.Bot(command_prefix='!') 


# @bot.event
# async def on_message(message):
    
#     if(message.author == bot.user):
#         return
        
#     print(dir(message.channel))

    
@bot.command()
async def reg(account_name):
    print("Reg...")
    await bot.say("Associendo tu cuenta de discord con la cuenta en Steem: " + account_name)
    register_token = token_hex(16)
    msg = "Manda 0.001 SBD a la cuenta ***"  + steem_curation_account + "*** con este Memo: " + register_token + " y ejecuta el comando ***!verifica " + account_name + "*** para finlizar el registro"
    await bot.say(msg)
    

@bot.command()
async def cc():
    await bot.say("Creating channels...")
    


@bot.command()
async def verifica():

    await bot.say("Verificando...")
    

print("Discord.py version: " + discord.__version__)
bot.run(TOKEN)