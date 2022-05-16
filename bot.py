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
GAMECHANNEL = int(os.getenv("GAMECHANNEL"))
PREFIX = (os.getenv("DEFAULTPREFIX")) #Prefix du bot par defaut
TOKEN = str(os.getenv("TOKENP1") + os.getenv("TOKENP2"))
###########################################################################

listeEvents=[]
client = discord.Client()
intents = discord.Intents.all()

#initialisation de la variable contenant le bot
bot = commands.Bot(command_prefix=PREFIX,intents=intents)






@bot.event
async def on_ready():
    print("Aegis is up and running")
    for guild in bot.guilds:
        print('Active in {}\n Member Count : {}'.format(guild.name,guild.member_count))
    writeLogs("Aegis a redemarre, pensez a &RGame dans le salon aproprier")

    print(bot.get_guild(GUILD))
    #Recuperation des roles de guild
    new = get(bot.get_guild(GUILD).roles, name="Nouvel Arrivant")
    member = get(bot.get_guild(GUILD).roles, name="Random Members")
    a_poil = get(bot.get_guild(GUILD).roles, name="A-poil")
    FFXIV = get(bot.get_guild(GUILD).roles, name="FFXIV")
    LOL = get(bot.get_guild(GUILD).roles, name="League of Legends")
    YGO = get(bot.get_guild(GUILD).roles, name="Yu gi oh")
    APEX = get(bot.get_guild(GUILD).roles, name="Apex Legends")
    global RoleDict
    RoleDict = {"new" : new,"member": member,"a_poil" : a_poil,"FFXIV" : FFXIV,"LOL" : LOL,"YGO" : YGO,"APEX" : APEX}
    ArrivalChan = bot.get_guild(GUILD).get_channel(ARRIVAL)
    GameChan = bot.get_guild(GUILD).get_channel(GAMECHANNEL)
    await manageRoleArrival()
    await checkEveryone.start()
    

    
    

########### Fonctions de gestion des roles

#Fonction permettant de promouvoir quelqu'un en membre permanant
@bot.command (name="promote", aliases = ["Promote"])
@commands.has_role('Staff')
async def promote(ctx,peon : discord.Member):
    role = get(bot.get_guild(GUILD).roles, name="Event")
    if role in peon.roles:
        await giveRole(peon,RoleDict["member"])
        updateEventFile(str(peon.id))
        await peon.remove_roles(role)
        writeLogs(f"{str(peon)} a ete promue en membre permanant")


#Fonction du menu de role cote server   
async def manageRoleArrival():
    Channel = bot.get_guild(GUILD).get_channel(ARRIVAL)
    reac2 = "<:CAT_Simp:864745278685970452>"
    reac1 = "<:OG_Smug:708637710608498698>"
    await DELETE(bot.get_guild(GUILD).get_channel(ARRIVAL))
    message = await Channel.send(f"Réagissez pour recevoir le role adéquoit :\n{reac1} : `Random member` : Ce role est attribué a toute personne souhaitant rester sur le server\n{reac2} : `Event` : Ce role est attribué aux personnes ne souhaitant pas rester sur le server plus de 3 jours")
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
                await removeRole(user,RoleDict["new"])
                await event(user)
            elif (str(reaction) == reac1):
                await removeRole(user,RoleDict["new"])
                await giveRole(user,RoleDict["member"])
                await giveRole(user,RoleDict["a_poil"])
    
@bot.command(name = "RGame")
async def manageRoleGames(ctx):
    Channel = bot.get_guild(GUILD).get_channel(GAMECHANNEL)
    reacLol = "<:LOL_12:838472239761850399>"
    reacApex = "<:ApexLegends:975748414136533092>"
    reacFF = "<:FFcroixbatonv:975748447481241630>"
    reacYGO = "<:AM_Kaiba_Deleted:781176640721256449>"
    await DELETE(bot.get_guild(GUILD).get_channel(GAMECHANNEL))
    message = await Channel.send(f"Réagissez pour recevoir le role de jeu adéquoit :\n{reacLol} : `League of Legends`\n{reacYGO} : `Yu gi oh`\n{reacFF} : `Final Fantasy XIV`\n {reacApex} : `Apex Legends`\n 👍 : `Finis`")
    await message.add_reaction(reacLol)
    await message.add_reaction(reacYGO)
    await message.add_reaction(reacFF)
    await message.add_reaction(reacApex)
    await message.add_reaction("👍")
    def check(reaction, user):
                return user != message.author and (str(reaction.emoji) == reacApex or str(reaction.emoji) == reacFF or str(reaction.emoji) == reacLol or str(reaction.emoji) == reacYGO or str(reaction.emoji) =="👍" )
    while(True):
        try:
            reaction, user = await bot.wait_for('reaction_add', check=check)
        except Exception as e:
            a=2
            print(a)
        else :
            if (str(reaction) == reacLol):
                await giveRole(user,RoleDict["LOL"])
            elif (str(reaction) == reacApex):
                await giveRole(user,RoleDict["APEX"])
            elif (str(reaction) == reacYGO):
                await giveRole(user,RoleDict["YGO"])
            elif (str(reaction) == reacFF):
                await giveRole(user,RoleDict["FFXIV"])
            elif (str(reaction) == "👍"):
                await removeRole(user,RoleDict["a_poil"])
             
            

        
#Fonction donnant un role aux nouveaux arrivants
@bot.event
async def on_member_join(member : discord.member):
    role = get(bot.get_guild(GUILD).roles, name="Nouvel Arrivant")
    await member.add_roles(role)
    writeLogs(f"{str(member)} a rejoint le server")


#Fonction retirant le role de nouvel arrivant
async def removeRole(member : discord.user,role : discord.role):
    await member.remove_roles(role)

#Fonction donnant le role temporaire
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


#Fonction donnant le role permanent
async def giveRole(member : discord.user, role : discord.role):
    await member.add_roles(role)
    writeLogs(f"{str(member)} a recut le role {role}")
        
#Loop lit la liste des utilisateurs temporaires et lance la fonction de check pour chacun
@tasks.loop(minutes=10)
async def checkEveryone():
    today= str(date.today())
    listevent=[]
    members = await bot.get_guild(GUILD).fetch_members().flatten()
    for i in members:
        for j in i.roles:
            if (str(j).split(" ")[0] == "Event"):
                listevent.append(i)
    
    for i in listevent:
        await checkForTime(i)


#Fonction qui verifie si la durée de vie d'un membre est dépassée
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

#Fonction qui ecrit dans le fichier des utilisateur temporaires
def writeId(id):
    now = str(datetime.now()).split(" ")[0]
    f = open("Liste","a")
    f.write(str(id) + ";" +now +"\n")
    f.close()

#Fonction qui met a jour la liste des utilisateur temporaires en retirant l'id de l'utilisateur kick
def updateEventFile(id : str):
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

########### Fonctions de gestion du server

#Fonction qui supprime tout les messages du channel *
@bot.command(name = "Purge")
@commands.has_permissions(manage_messages=True)
async def deletAllMessages(ctx, channelID : discord.channel = None):
    if channelID:
        channel = channelID
    else:
        channel = ctx.channel
    await DELETE(channel)
    writeLogs(f"{str(ctx.author)} a supprimer les messages du salon {channel}")

async def DELETE(channel : discord.channel):
    messages = await channel.history(limit=10).flatten()
    for i in messages:
        await i.delete()
    

########### Fonctions pour controler le Bot

#Fonction d'affichage des logs
@bot.command (name = "showLogs", aliases = ["logs","Logs","ShowLogs","showlogs","Showlogs"])
@commands.has_role("Staff")
async def showLogs(ctx,InputDate = None):
    if not InputDate:
        InputDate = str(date.today())
    logname="Log-"+InputDate+".txt"
    message =""
    try:
        log = open(f"Logs/{logname}","r")
        data = log.readlines()
        log.close()
        await ctx.channel.send(f"Logs du {InputDate}")
        for line in data:
            message = message+line
            if len(message)>=500:
                await ctx.channel.send(message)
                message = ""
        await ctx.channel.send(message)
    except Exception as e:
        await ctx.channel.send("Veuillez entrer une date valide dans le format `YYYY-MM-DD` ou j'ai été en fonction")
        await ctx.channel.send(":warning: Si rien ne s'est passé ce jour-ci, les logs du jour n'existeront pas :warning:")

#Fonction d'écriture des logs
def writeLogs(message : str):
    Horodatage = "["+str(datetime.now()).split(".")[0]+"]"
    logname = "Log-"+str(date.today())+".txt"
    log = open(f"Logs/{logname}","a")
    log.write(Horodatage+" "+message+"\n")
    log.close()

#Fonction permettant de changer le prefix (néccessite un reboot)
@bot.command (name = "Prefix", aliases = ["prefix","p","P"])
@commands.has_role('Staff')
async def pref(ctx,NEWPREFIX : str = None):
    if NEWPREFIX:
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
    else:
        await ctx.channel.send(f"Mon prefix actuel est : `{PREFIX}`")





bot.run(TOKEN)
