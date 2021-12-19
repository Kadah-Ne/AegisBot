from inspect import getcallargs
import discord
from discord import guild
from discord import channel
from discord.ext import commands
from dotenv import load_dotenv
import os
from discord.utils import get
import time
from datetime import datetime, datetime
from discord.ext import tasks

listeEvents=[]
client = discord.Client()
intents = discord.Intents.all()
load_dotenv(dotenv_path="config")
bot = commands.Bot(command_prefix='&',intents=intents)
GUILD = int(os.getenv("GUILD"))
ARRIVAL = int(os.getenv("ARRIVALCHANNEL"))

@bot.event
async def on_ready():
    print("ça tourne")
    await checkEveryone.start()

def writeId(id):
    now = str(datetime.now()).split(" ")[0]
    f = open("Liste","a")
    f.write(str(id) + ";" +now +"\n")
    f.close()


@bot.command(name = "manageRole", aliases=['role'])
async def manageRole(ctx):
    reac2 = "<:CAT_Simp:864745278685970452>"
    reac1 = "<:OG_Smug:708637710608498698>"
    await deletAllMessages()
    role = get(ctx.guild.roles, name="Event")
    message = await ctx.channel.send(f"Réagissez pour recevoir le role adéquoit :\n{reac1} : `Resident permanent`\n{reac2} : `Event`")
    await message.add_reaction(reac1)
    await message.add_reaction(reac2)
    def check(reaction, user):
                return user != message.author and (str(reaction.emoji) == reac2 or str(reaction.emoji) == reac1)
    while(True):
        try:
            reaction, user = await bot.wait_for('reaction_add', check=check)
        except e:
            a=2
            print(a)
        else :
            if (str(reaction) == reac2):
                await removeNew(ctx,user)
                await event(ctx, user)
            elif (str(reaction) == reac1):
                await removeNew(ctx,user)
                await stable(ctx,user)
            

        

@bot.event
async def on_member_join(member : discord.member):
    role = get(bot.get_guild(GUILD).roles, name="Nouvel Arrivant")
    await member.add_roles(role)


async def removeNew(ctx, member : discord.user):
    role = get(bot.get_guild(GUILD).roles, name="Nouvel Arrivant")
    await member.remove_roles(role)


async def event(ctx, member : discord.user):
    flag = False
    role = get(bot.get_guild(GUILD).roles, name="Event")
    
    await member.add_roles(role)
    f = open("Liste","r")
    for i in f:
        if i.split(";")[0] == str(member.id):
            flag = True
    f.close()
    if not flag:
        writeId(member.id)



async def stable(ctx, member : discord.user):
    role = get(bot.get_guild(GUILD).roles, name="Random Members")
    await member.add_roles(role)
        

@tasks.loop(minutes=10)
async def checkEveryone():
    listevent=[]
    members = await bot.get_guild(GUILD).fetch_members().flatten()
    for i in members:
        for j in i.roles:
            if (str(j).split(" ")[0] == "Event"):
                listevent.append(i)
    
    for i in listevent:
        await checkForTime(i)



async def checkForTime(member : discord.user):
    user = ""
    role = get(bot.get_guild(GUILD).roles, name="Event")
    now = str(datetime.now()).split(" ")[0]
    f = open("Liste","r")
    for i in f:
        
        if i.split(";")[0] == str(member.id):
            user = i.rstrip("\n")
    f.close()
    if user:
        userTime = user.split(";")[1]
        userId = int(user.split(";")[0])
        user = bot.get_guild(GUILD).get_member(userId)
        diffY = int(now.split("-")[0]) - int(userTime.split("-")[0])
        diffM = int(now.split("-")[1]) - int(userTime.split("-")[1])
        diffD = int(now.split("-")[2]) - int(userTime.split("-")[2])
        print(diffY,diffM,diffD)
        isNewYear = int(userTime.split("-")[1]) == 12 and int(userTime.split("-")[2]) > 29 and diffY == 1 and int(now.split("-")[2]) < 3 and int(now.split("-")[0]) == 1
        isNewMonth = diffM = 1 and int(userTime.split("-")[0]) == (28 or 29 or 30 or 31)
        if not isNewYear and not isNewMonth and (diffY !=0 or diffM !=0 or diffD > 2):
            await user.remove_roles(role)
            await bot.get_guild(GUILD).kick(user)
            updateEventFile(str(userId))


async def deletAllMessages():
    channel = bot.get_guild(GUILD).get_channel(ARRIVAL)
    messages = await channel.history(limit=123).flatten()
    for i in messages:
        await i.delete()


def updateEventFile(id):
    listUsersEvent = []
    temp = ""
    f = open("Liste","r")
    for i in f:
        listUsersEvent.append(i.strip("\n"))
    f.close()
    for i in listUsersEvent:
        if i.split(";")[0] == id:
            temp = i
    listUsersEvent.remove(temp)
    f = open("Liste","w")
    for i in listUsersEvent:
        f.write(i+"\n")

bot.run(str(os.getenv("TOKENP1") + os.getenv("TOKENP2")))