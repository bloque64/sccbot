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


settings = Settings()
settings.load()

TOKEN = settings.discord_token


bot = commands.Bot(command_prefix='!') 




@bot.command()
async def init(ctx):
    guild = ctx.guild
    await ctx.send("Inicitalizing channel structure...")

    categories = settings.get_categories()
    for c in categories:
        await ctx.send("Creating category: %s" % c)
        cat = await guild.create_category(c["name"])
        settings.set_category_id(c["name"], cat.id)
        channels = settings.get_channels_by_cat(c["name"])
        for ch in channels:
            chan = await guild.create_text_channel(ch["name"], category=cat)
    
    settings.save()

@bot.command()
async def del(ctx):
    guild = ctx.guild
    await ctx.send("Deleting channel structure...")
 

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


@bot.listen()
async def on_message(message):
    
    channel = message.channel

    if(message.author == bot.user):
        return

    
    await channel.send(message.content)

    
print("Runnng bot...")
bot.run(TOKEN)