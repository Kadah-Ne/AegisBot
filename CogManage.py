from discord.ext import commands
from discord.utils import get
from datetime import datetime
from pathlib import Path
from os import path
import discord
import time

class CogManage(commands.Cog):
    def __init__(self,bot,guild):
        self.bot = bot
        self.guild = guild

    
    async def writeLogs(self,message):
        dateStr = datetime.now().strftime("%d%m%Y")
        Chemin = Path(f"./Logs/logs-{dateStr}.txt")
        if not Chemin.exists():
            logs = open(Chemin,"w")
            logs.write(f"{time.strftime('%H:%M:%S', time.localtime())} - {message} \n")
            logs.close()
        else:
            logs = open(Chemin,"a+")
            logs.write(f"\n{time.strftime('%H:%M:%S', time.localtime())} - {message}")
            logs.close()

    @commands.command (name="promote", aliases = ["Promote"])
    @commands.has_role('Staff')
    async def promote(self,ctx,peon : discord.Member):
        role = get(self.guild.roles, name="Event")
        if role in peon.roles:
            await peon.add_roles(get(self.guild.roles, name="Random Members"))
            await peon.remove_roles(role)
            await self.writeLogs(f"{peon} as recevieved the role {role}")


    @commands.command(name = "Purge")
    @commands.has_permissions(manage_messages=True)
    async def deletAllMessages(self,ctx, channelID : int = None):
        if channelID:
            channel = channelID
        else:
            channel = ctx.channel.id
        await self.DELETE(channel)
        await self.writeLogs(f"{ctx.author} deleted messages from {ctx.channel}")
        

    async def DELETE(self,channelId : int, nb :int = 10):
        channel = self.bot.get_channel(channelId)
        messages = await channel.history(limit=nb).flatten()
        for i in messages:
            await i.delete()

    @commands.command (name = "Prefix", aliases = ["prefix","p","P"])
    @commands.has_role('Staff')
    async def pref(self,ctx,NEWPREFIX : str = None):
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
            await self.writeLogs(f"{ctx.author} as changed the prefix to {NEWPREFIX}")
        else:
            await ctx.channel.send(f"Mon prefix actuel est : `{PREFIX}`")

    @commands.command (name = "Logs", aliases = ["logs","Log","log"])
    @commands.has_role('Staff')
    async def showLogs(self,ctx,message : str = None):
        LogChain = ""
        
        if message == None :
            dateStr = datetime.now().strftime("%d%m%Y")
            date = datetime.now()
            Chemin = Path(f"./Logs/logs-{dateStr}.txt")
            LogChain=date.strftime("%A - %d/%m/%Y") +" :"
            if Chemin.exists():
                logs = open(Chemin)
                lines = logs.readlines()
                for line in lines:
                    LogChain+= line
                await ctx.channel.send(LogChain)

            else:
                await ctx.channel.send(f"Aucun log pour la journée du {date.strftime('%d %B %Y')}")
        else:
            if message.__contains__("/"):
                a = 1
            elif message.__contains__("-"):
                a = 2
            else :
                a = 3
                
            if a == 1:
                date = datetime.strptime(message,"%d/%m/%Y")
            elif a == 2:
                date = datetime.strptime(message,"%d-%m-%Y")

            if a !=3 :
                dateStr = date.strftime("%d%m%Y")
                Chemin = Path(f"./Logs/logs-{dateStr}.txt")
                LogChain=date.strftime("%A - %d/%m/%Y") +" :"
                if Chemin.exists():
                    logs = open(Chemin)
                    lines = logs.readlines()
                    for line in lines:
                        LogChain+= line
                    await ctx.channel.send(LogChain)
                else:
                    await ctx.channel.send(f"Aucun log pour la journée du {date.strftime('%d %B %Y')}")
            else:
                await ctx.channel.send("Veuillez appeler cette fonction avec une date dans un des formats suivants :\n `jj mm aaaa` \n `jj-mm-aaaa` \n `jj/mm/aaaa`")
    
    
