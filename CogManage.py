from discord.ext import commands
from discord.utils import get
from datetime import datetime
from pathlib import Path
from os import path
import sqlite3
import discord
import time

class CogManage(commands.Cog):
    
    def __init__(self,bot,guild):
        self.bot = bot
        self.guild = guild


    async def writeLogs(self,message):
        DB_CON,DB_CUR = self.DB_CONNECT()

        dateNow = datetime.now().date()
        timeNow = datetime.now().strftime("%H:%M:%S")
        print(dateNow,timeNow)
        DB_CUR.execute("INSERT INTO Logs (Date,Time,Text,GUILD_ID) VALUES (?,?,?,?)",(dateNow,timeNow,message,self.guild.id))
        DB_CON.commit()
        DB_CON.close()

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
        messages = [msg async for msg in channel.history(limit = nb)]
        # messages = await channel.history(limit=nb).flatten()
        for i in messages:
            await i.delete()
            

    @commands.command (name = "Logs", aliases = ["logs","Log","log"])
    @commands.has_role('Staff')
    async def showLogs(self,ctx,message : str = None):
        LogChain = ""
        DB_CON,DB_CUR = self.DB_CONNECT()
        if message == None :
            dateNow = datetime.now().date()
            query = f"SELECT * FROM Logs WHERE Date = '{dateNow}' AND GUILD_ID = '{self.guild.id}'"
            list_logs = [a for a in DB_CUR.execute(query)]
            for log in list_logs :
                LogChain += log[1] +'-'+log[2]+' : '+ log[3] +'\n'
            await ctx.channel.send(LogChain)

    @commands.command(name = "update_arival", aliases = ["ua"])

    # @commands.has_role('Staff')
    async def updateArival(self,ctx) :
        DB_File = '/home/pi/Desktop/DBStuff/AegisBot/config_db.db'
        # DB_File = 'C:/Users/mgouv/Desktop/DBStuff/AegisBot/config_db.db'
        DB_CON = sqlite3.connect(DB_File)
        DB_CUR = DB_CON.cursor()
        #Will need to check coll name
        query = f"UPDATE GUILD_STORAGE SET ROLE_CHAN_ID = '{ctx.channel.id}' WHERE GUILD_NAME =  'Random Flash Generation'"
        # query = f"UPDATE GUILD_STORAGE SET ROLE_CHAN_ID = '{ctx.channel.id}' WHERE GUILD_NAME = 'Commission_land'"
        print(query)
        DB_CUR.execute(query)
        DB_CON.commit()
        DB_CON.close()
        
    def DB_CONNECT(self) :
        DB_FILE = '/home/pi/Desktop/DBStuff/AegisBot/logs_db.db'
        # DB_FILE = 'C:/Users/mgouv/Desktop/DBStuff/AegisBot/logs_db.db'
        DB_CON = sqlite3.connect(DB_FILE)
        DB_CUR = DB_CON.cursor() 
        return DB_CON,DB_CUR
