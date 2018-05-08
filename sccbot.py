import discord
from discord.ext import commands
import secrets
from secrets import token_hex
from settings import Settings
import data
import evaluator

__author__ = "@pgarcgo"
__version__ = "0.1"

name = "Steem Community Curation BOT"
steem_curation_account = "sccb"


settings = Settings()
settings.load()

message_evaluator = evaluator.MessageEvaluator()

TOKEN = settings.discord_token

print("Bot TOKEN: %s" % TOKEN)
print("Discord.py version: %s" % discord.__version__)


bot = commands.Bot(command_prefix='!') 


@bot.command()
async def list_channels(ctx):
    guild = ctx.guild
    await ctx.send("Listing channels...")

    categories = settings.get_categories()
    for c in settings.get_channels():
         await ctx.send("Channel: %s" % c)


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
        #await ctx.send("Int Category: %s" % cat.name)
        for ch in channels:
            await ctx.send("Creating channel: %s" % chr)
            chan = await guild.create_text_channel(ch["name"], category=cat)
            settings.set_channel_id(channel_name = ch["name"], category_name = c["name"], id=chan.id)
    
    settings.save()

@bot.command()
async def shutdown(ctx):
    bot.close()
    await ctx.send("Shutting down sccbot!!.\nAfter this, manual re-start on server side is needed!!")
    exit()

@bot.command()
async def force_delete(ctx):
    guild= ctx.guild
    channels = guild.text_channels
    for c in channels:

        if c.name != "general":
            await ctx.send("Deleting channel: %s" % c)
            await c.delete()

    for cat in guild.categories:
        await ctx.send("Deleting category: %s" % cat)  
        await cat.delete()

@bot.command()
async def delete(ctx):
    guild = ctx.guild
    await ctx.send("Deleting channel structure...")
    for c in settings.get_channels():
        print()
        await ctx.send("Deleting channel: %s" % c)
 
@bot.command()
async def reg(ctx, account_name):
    print("Reg...")
    await ctx.send("Associendo tu cuenta de discord con la cuenta en Steem: " + account_name)
    register_token = token_hex(16)
    msg = "Manda 0.001 SBD a la cuenta ***"  + steem_curation_account + "*** con este Memo: " + register_token + " y ejecuta el comando ***!verifica " + account_name + "*** para finlizar el registro"
    await ctx.send(msg)
    
@bot.listen()
async def on_message(message):
    
    channel = message.channel

    if(message.author == bot.user):
        return

    message_evaluator.evaluate_message(message)
    
#await channel.send(message.content)

def exit_gracefully():
    print("Quiting sccbot...")
    
print("Runnng bot...")

try:
    bot.run(TOKEN)
except KeyboardInterrupt:
    pass
finally:
    exit_gracefully()

