#Importation des librairies néccessaires

from inspect import getcallargs
import discord
from discord import guild,channel
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
from discord.utils import get
import time
from datetime import datetime, datetime, date

######### BETA
import youtube_dl
#########

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

#initialisation de la variable contenant le bot
bot = commands.Bot(command_prefix=PREFIX,intents=intents)


@bot.event
async def on_ready():
    print("Aegis is up and running")
    writeLogs("Aegis a redemarre")
    await manageRole()
    await checkEveryone.start()
    

########### Fonctions de gestion des roles

#Fonction permettant de promouvoir quelqu'un en membre permanant
@bot.command (name="promote", aliases = ["Promote"])
@commands.has_role('Staff')
async def promote(ctx,peon : discord.Member):
    role = get(bot.get_guild(GUILD).roles, name="Event")
    if role in peon.roles:
        await member(peon)
        updateEventFile(str(peon.id))
        await peon.remove_roles(role)
        writeLogs(f"{str(member)} a ete promue en membre permanant")


#Fonction du menu de role cote server   
async def manageRole():
    Channel = bot.get_guild(GUILD).get_channel(ARRIVAL)
    reac2 = "<:CAT_Simp:864745278685970452>"
    reac1 = "<:OG_Smug:708637710608498698>"
    await DELETE(bot.get_guild(GUILD).get_channel(ARRIVAL))
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
            

        
#Fonction donnant un role aux nouveaux arrivants
@bot.event
async def on_member_join(member : discord.member):
    role = get(bot.get_guild(GUILD).roles, name="Nouvel Arrivant")
    await member.add_roles(role)
    writeLogs(f"{str(member)} a rejoint le server")


#Fonction retirant le role de nouvel arrivant
async def removeNew(member : discord.user):
    role = get(bot.get_guild(GUILD).roles, name="Nouvel Arrivant")
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
async def member(member : discord.user):
    role = get(bot.get_guild(GUILD).roles, name="Random Members")
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

#Fonction qui supprime 10 messages du channel
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

########### Fonctions pour les utilisateurs (BETA)

#Definition des options de ytdl (A BOUGER EN HAUT UNE FOIS SORTI DE BETA)
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

# Commande permettant au bot de rejoindre un channel vocal
@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

# Commande permettant au bot de quitter un channel vocal
@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

# Commande envoyant la requete de la musique (Faire en sorte que on ne soit pas obligé de mettre un url)
@bot.command(name='play_song', help='To play song')
async def play(ctx,url):
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    except:
        await ctx.send("The bot is not connected to a voice channel.")

# Commande mettant en pause la musique
@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")

# Commande relancant la musique    
@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")

# Commande arretant la musique
@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")



bot.run(TOKEN)
