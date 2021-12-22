#Importation des librairies néccessaires

from inspect import getcallargs
import discord
from discord import guild
from discord import channel
from discord.ext import commands
from dotenv import load_dotenv
import os
from discord.utils import get
import time
from datetime import datetime, datetime, date
from discord.ext import tasks


#Initialisation des variables Globales

############ RECUPERATION DES INFOS DU FICHER CONFIG ###################### 
load_dotenv(dotenv_path="config")
GUILD = int(os.getenv("GUILD")) #Server discord par defaut
ARRIVAL = int(os.getenv("ARRIVALCHANNEL")) #Channel textuel d'arrivee par defaut
PREFIX = (os.getenv("DEFAULTPREFIX")) #Prefix du bot par defaut
TOKEN = str(os.getenv("TOKENP1") + os.getenv("TOKENP2"))
###########################################################################

listeEvents=[]
client = discord.Client()
intents = discord.Intents.all()

bot = commands.Bot(command_prefix=PREFIX,intents=intents)


@bot.event
async def on_ready():
    print("Aegis is up and running")
    writeLogs("Aegis a redemarre")
    await manageRole()
    await checkEveryone.start()
    

def writeLogs(message : str):
    Horodatage = "["+str(datetime.now()).split(".")[0]+"]"
    logname = "Log-"+str(date.today())+".txt"
    log = open(f"Logs/{logname}","a")
    log.write(Horodatage+" "+message+"\n")
    log.close()

@bot.command (name = "Prefix", aliases = ["prefix","p","P"])
@commands.has_role('Staff')
async def pref(ctx,NEWPREFIX : str):
    f = open("config","r")
    lines = f.readlines()
    f.close()
    f = open("config","w")
    for line in lines:
        if "DEFAULTPREFIX=" not in line:
            f.write(line)
    f.write("DEFAULTPREFIX="+NEWPREFIX)

    await ctx.channel.send("Le prefix a été changer a `"+NEWPREFIX+"`")
    writeLogs(f"{str(ctx.author)} a changer le prefix a {NEWPREFIX}")


def writeId(id):
    now = str(datetime.now()).split(" ")[0]
    f = open("Liste","a")
    f.write(str(id) + ";" +now +"\n")
    f.close()

@bot.command (name = "showLogs", aliases = ["logs","Logs","ShowLogs","showlogs","Showlogs"])
@commands.has_role("Staff")
async def showLogs(ctx,date = str(date.today())):
    logname="Log-"+date+".txt"
    message =""
    try:
        log = open(f"Logs/{logname}","r")
        data = log.readlines()
        log.close()
        await ctx.channel.send(f"Logs du {date}")
        for line in data:
            message = message+line
        await ctx.channel.send(message)

    except Exception as e:
        await ctx.channel.send("Veuillez entrer une date valide dans le format `YYYY-MM-DD` ou j'ai été en fonction")
        await ctx.channel.send(":warning: Si rien ne s'est passé ce jour-ci, les logs du jour n'existeront pas :warning:")
    
        
async def manageRole():
    Channel = bot.get_guild(GUILD).get_channel(ARRIVAL)
    reac2 = "<:CAT_Simp:864745278685970452>"
    reac1 = "<:OG_Smug:708637710608498698>"
    await deletAllMessages()
    message = await Channel.send(f"Réagissez pour recevoir le role adéquoit :\n{reac1} : `Resident permanent`\n{reac2} : `Event`")
    await message.add_reaction(reac1)
    await message.add_reaction(reac2)
    def check(reaction, user):
                return user != message.author and (str(reaction.emoji) == reac2 or str(reaction.emoji) == reac1)
    while(True):
        try:
            reaction, user = await bot.wait_for('reaction_add', check=check)
        except Exception as e:
            a=2
            print(a)
        else :
            if (str(reaction) == reac2):
                await removeNew(user)
                await event(user)
            elif (str(reaction) == reac1):
                await removeNew(user)
                await member(user)
            

        

@bot.event
async def on_member_join(member : discord.member):
    role = get(bot.get_guild(GUILD).roles, name="Nouvel Arrivant")
    await member.add_roles(role)
    writeLogs(f"{str(member)} a rejoint le server")


async def removeNew(member : discord.user):
    role = get(bot.get_guild(GUILD).roles, name="Nouvel Arrivant")
    await member.remove_roles(role)


async def event(member : discord.user):
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
    writeLogs(f"{str(member)} a recut le role {role}")



async def member(member : discord.user):
    role = get(bot.get_guild(GUILD).roles, name="Random Members")
    await member.add_roles(role)
    writeLogs(f"{str(member)} a recut le role {role}")
        

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
        isNewYear = int(userTime.split("-")[1]) == 12 and int(userTime.split("-")[2]) > 29 and diffY == 1 and int(now.split("-")[2]) < 3 and int(now.split("-")[0]) == 1
        isNewMonth = diffM = 1 and int(userTime.split("-")[0]) == (28 or 29 or 30 or 31)
        if not isNewYear and not isNewMonth and (diffY !=0 or diffM !=0 or diffD > 2):
            await user.remove_roles(role)
            await bot.get_guild(GUILD).kick(user)
            updateEventFile(str(userId))
            writeLogs(f"{str(user)} a été kick du server apès 2 jours du role event")


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

bot.run(TOKEN)