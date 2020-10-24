import os # for heroku config vars
import random
import asyncio
import time
import datetime
import discord
from discord import Game
from discord.ext.commands import Bot

BOT_PREFIX = ("!", "")
TOKEN = os.environ.get('BOT_TOKEN_EU')
ROLENAMESTAFF = "scrim staff"
ROLENAME = "Scrims"
CHANNELNAME = "eu-match-info"
TIME = 75

client = Bot(command_prefix=BOT_PREFIX)

global msg, msglist, msgnames, ongoing
ongoing = False
async def fortnite(channel, message):
    global msg, msglist, msgnames, ongoing
    embed=discord.Embed(title="The match has begun!", color=0xb405ff)
    embed.add_field(name="Enter your server IDs below", value=" - Put the last 3 digits of the server identifier in the chat\n - You will find this on the top left of your screen", inline=True)
    embed.set_footer(text=time.strftime("Time - %H:%M", time.gmtime(time.time())))
    await client.send_message(channel, embed=embed)
    embed=discord.Embed(title="Servers:", color=0x004eeb)
    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/285894122349527040/13074cb7aea2ec1bbb5bf5ac9d7addae.png")
    embed.set_footer(text=time.strftime("Time - %H:%M", time.gmtime(time.time())))
    msg = await client.send_message(channel, embed=embed)
    ongoing = True
    msglist = []
    msgnames = []
    overwrite = discord.PermissionOverwrite(send_messages=True, read_messages=True)
    role = discord.utils.get(message.server.roles, name=ROLENAME)
    await client.edit_channel_permissions(message.channel, role, overwrite)
    await asyncio.sleep(TIME)
    overwrite = discord.PermissionOverwrite(send_messages=False, read_messages=True)
    ongoing = False
    await client.edit_channel_permissions(message.channel, role, overwrite)
    embed=discord.Embed(title="Chat Locked", color=0xff05fb)
    embed.add_field(name="The chat has been locked", value="Good luck on the match everyone!", inline=True)
    embed.set_footer(text=time.strftime("Time - %H:%M", time.gmtime(time.time())))
    await client.send_message(channel, embed=embed)   

@client.event
async def on_message(message):
    global msg, msglist, msgnames, ongoing
    if message.channel.name != CHANNELNAME:
        return
    if message.author == client.user:
        return
    if message.content == "!codes" and ROLENAMESTAFF in [y.name.lower() for y in message.author.roles]:
        ongoing = True
        await fortnite(message.channel, message)
    if ongoing:
        message.content = message.content.lower()
        if message.channel.name == CHANNELNAME:
            await client.delete_message(message)
        if len(str(message.content)) == 3 and message.content.isalnum():
            ending = False
            for each1 in range(len(msgnames)):
                for each2 in range(len(msgnames[each1])):
                    if each2 != 0:
                        if msgnames[each1][each2] == message.author.mention:
                            if msgnames[each1][0] == 1:
                                del msgnames[each1]
                                del msglist[each1]
                                ending = True
                                break
                            else:
                                del msgnames[each1][each2]
                                msgnames[each1][0] -= 1
                                ending = True
                                break
                if ending == True:
                    break
            if message.content not in msglist:
                msglist.append(str(message.content))
                msgnames.append([1, str(message.author.mention)])
            else:
                msgnames[msglist.index(str(message.content))].append(str(message.author.mention))
                msgnames[msglist.index(str(message.content))][0] += 1
            embed=discord.Embed(title="Servers:", color=0x004eeb)
            embed.set_thumbnail(url="https://cdn.discordapp.com/icons/285894122349527040/13074cb7aea2ec1bbb5bf5ac9d7addae.png")
            newlist = []
            for each in range(len(msglist)):
                newlist.append([msglist[each], msgnames[each]])
            newlist = sorted(newlist, key = lambda x: x[1][0], reverse=True)
            for each in range(len(newlist)):
                text = "players"
                if newlist[each][1][0] == 1:
                    text = "player"
                idname = "ID: {0} - {1} {2}\n".format(newlist[each][0], newlist[each][1][0], text)
                idvalue = ""
                for each2 in range(len(newlist[each][1])-1):
                    idvalue += newlist[each][1][each2+1]+"\n"
                embed.add_field(name=idname, value=idvalue, inline=True)
            print("--")
            print(message.content, message.author.mention, CHANNELNAME)
            print(msgnames)
            print(msglist)
            print("--")
            embed.set_footer(text=time.strftime("%H:%M", time.gmtime(time.time())))
            await client.edit_message(msg, embed=embed)

@client.event
async def on_ready():
    await client.change_presence(game=Game(name="Scrims"))

async def go():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)
        
client.loop.create_task(go())
client.run(TOKEN)
