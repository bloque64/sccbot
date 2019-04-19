__author__ = "http://steemit.com/@cervantes"
__copyright__ = "Copyright (C) 2018 steem's @cervantes"
__license__ = "MIT"
__version__ = "1.0"


import discord
from discord.ext import commands
import asyncio
import secrets
from secrets import token_hex
from settings import Settings
import data
import evaluator
import register
import manager
import traceback
from data import User, Post
from datetime import datetime

__author__ = "@pgarcgo"
__version__ = "0.1"

name = "Steem Community Curation BOT"

sa_session = data.return_session()

settings = Settings(sa_session, "../config/")
settings.load()

data.create_tables()

message_evaluator = evaluator.MessageEvaluator(settings)
user_registerer = register.UserRegisterer(settings)
curator = manager.Manager(settings)

TOKEN = settings.discord_token
COMMAND_PREFIX = "!"

print("Bot TOKEN: %s" % TOKEN)
print("Discord.py version: %s" % discord.__version__)
print("Database Host: %s" % settings.sccbot_db_host)
print("Database Name: %s" % settings.sccbot_db_name)


bot = commands.Bot(command_prefix=COMMAND_PREFIX)



async def my_background_task():
        await bot.wait_until_ready()
        counter = 0
        while not bot.is_closed():
            counter += 1
            await asyncio.sleep(1) # task runs every 60 seconds

#A function to log messages on a configurable channel.
async def log_message(msg):
    log_channel = bot.get_channel(settings.get_log_channel_id())
    await log_channel.send(msg)

async def send_private_message(msg,  member_id):
    await bot.get_user(member_id).send(msg)

# background task verification_status
@bot.listen()
async def verification_status(ctx):
    await bot.wait_until_ready()
    counter = 0
    while not bot.is_closed():
        counter += 1
        #await channel.send(counter)
        print(counter)
        await asyncio.sleep(3) # task runs every 60 seconds


# bot.loop.create_task(verification_status())
 
@bot.command()
async def list_channels(ctx):
    guild = ctx.guild
    await ctx.send("Listing channels...")

    categories = settings.get_categories()
    for c in settings.get_channels():
         await ctx.send("Channel: %s" % c)


@bot.command()
async def init_db(ctx):

    try:
        data.drop_tables()
        data.create_tables()
        msg = "Tables deleted and created again!"
        await ctx.send(msg)
        await log_message(msg)

    except Exception as e:
        msn = "Coult not created tables: %s" % (str(e))

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
    
    channels = settings.get_channels_level_0()
    for ch in channels:
        await ctx.send("Creating level 0 channel: %s" % chr)
        chan = await guild.create_text_channel(ch["name"])
        settings.set_channel_id(channel_name = ch["name"], category_name ="", id=chan.id)


    settings.save()

@bot.command()
async def shutdown(ctx):
    bot.close()
    await ctx.send("Shutting down sccbot!!.\nAfter this, manual re-start on server side is needed!!")
    exit()


# Delete all channels but general
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

#Delete channels in settings with deletable = True
@bot.command()
async def delete(ctx):

    guild = ctx.guild
    channels = guild.text_channels

    await ctx.send("Deleting channel/categories structure...")

    for c in channels:

        if c.id in settings.get_deletable_channels_ids():
            await ctx.send("Deleting channel: %s" % c)
            await c.delete()

    for cat in guild.categories:
          
        if cat.id in settings.get_category_ids():
            await ctx.send("Deleting category: %s" % cat)
            await cat.delete()

@bot.command()
async def list_users(ctx):
    guild = ctx.guild
    await ctx.send("Listing registered user:")
    users = user_registerer.get_users()
    for u in users:
        await ctx.send("   %s (%s) => @%s (STATUS: %s)" % (u.discord_member_name,
                                                           u.discord_member_id,
                                                           u.steem_account,
                                                           u.verification_status)) 

@bot.group()
async def reg(ctx):
    subcommands = ['new', 'check', 'update']
    print(ctx.invoked_subcommand)
    #if ctx.invoked_subcommand not in subcommands:
    if ctx.invoked_subcommand is None:
        fmt = 'The !reg command options: {}, {}, {}'
        await ctx.send(fmt.format(*subcommands))

@reg.command(name='new')
async def _new(ctx, steem_account_name: str):
    discord_user =  ctx.message.author
    try:

        new_user = User()
        new_user.discord_member_id = discord_user.id
        new_user.discord_member_name = discord_user.name
        new_user.steem_account = steem_account_name
        new_user.role = data.USER_ROLE_REGISTERED
        new_user.verification_status = data.VS_PENDING
        new_user.registerd_on =datetime.now()

        user_registerer.add_user(new_user)

        await ctx.send("Added steem account to the registering qeue: " + steem_account_name)
        register_token = token_hex(16)
        msg = "Sent 0.001 SBD to this following account  ***"  + settings.registrant_account + "*** using this memo: " + register_token
        
        print("new_user.discord_member_id: %s" % new_user.discord_member_id)
        print("new_user.discord_member_id: %s" % new_user.discord_member_id)
        user_registerer.update_verification_token(discord_id = new_user.discord_member_id, verification_token = register_token)
        await ctx.send(msg)

    except Exception as e:
        await ctx.send(str(e))
        #await log_message(msg)
        #await send_private_message(msg, message.author.id)
        #await message.delete()
        pass

@_new.error
async def _new_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You need to specify a valid steem account as first parameter!")
    else:
        discord_user =  ctx.message.author
        try:
            user_registerer.map_user(discord_member_id=discord_user.id,
                                     discord_member_name=discord_user.name,
                                     steem_account=steem_account_name,
                                     role=data.USER_ROLE_REGISTERED)
            await ctx.send("Added steem account to the registering qeue: " + steem_account_name)
            register_token = token_hex(16)
            msg = "Sent 0.001 SBD to this following account  ***"  + settings.registrant_account + "*** using this memo: " + register_token
            await ctx.send(msg)
        except:
            await ctx.send(traceback.format_exc())

@bot.command()
async def validate_pending(ctx):

    try:
        user_registerer.validate_pending()
        await log_message("Pending users validated")
    except Exception as e:
        await log_message(str(e))


@bot.command()
async def delete_users(ctx):

    try:
        #user_registerer.delete_users(discord_user.id, discord_user.name, account_name)
        user_registerer.delete_users()
        msg = "All users deleted"
        await ctx.send(msg)
        await log_message(msg)
    except Exception as e:
        await log_message(str(e))

    
@bot.listen()
async def on_message(message):
    
    channel = message.channel

    if(message.author == bot.user):
        return


    if settings.get_category_by_channel_id(channel.id) == "PROMOCION":

        r = message_evaluator.check_message(message)

        if(not r):

            await log_message(r.message3p)
            await send_private_message(r.message1p, message.author.id)
            await message.delete()

        else:
            m_user = user_registerer.get_user_by_discord_id(r.curator_discord_id)
            r = curator.promote_post(user = m_user, url = r.content)
            await log_message(r.message3p)
            await send_private_message(r.message1p, message.author.id)

    else:
        print("Non Promotion channel...")

#await channel.send(message.content)

def exit_gracefully():

    print("Quiting sccbot...")
    
print("Runnng bot...")

try:
    bg_task = bot.loop.create_task(my_background_task())
    bot.run(TOKEN)
except KeyboardInterrupt:
    pass
finally:
    exit_gracefully()

