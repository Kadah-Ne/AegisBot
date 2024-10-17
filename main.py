from os import name, execv, system, environ,getenv
from sys import argv, executable, stdout
import sqlite3
import discord
from discord.utils import get
from discord.ext import commands
# from dotenv import load_dotenv
from CogJoin import CogJoin
from CogRoleMenuG import CogRoleMenuG
from CogManage import CogManage
from CogFunStuff import CogFunStuff

#Test Enviro
DB_File = '/home/pi/Desktop/DBStuff/AegisBot/config_db.db'
DB_CON = sqlite3.connect(DB_File)
DB_CUR = DB_CON.cursor()

ID,GUILD_NAME,GUILD,GChannel,Prefix = [a for a in DB_CUR.execute("SELECT * FROM GUILD_STORAGE WHERE GUILD_NAME = 'Random Flash Generation'")][0]

TOKEN = [a for a in DB_CUR.execute("SELECT * FROM TOKEN WHERE TOKEN_NAME = 'MAIN'")][0][2]
DB_CON.close()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=Prefix,intents=intents)

async def setup(bot,Setuper,RoleGame,Manager,Funny):
    await bot.add_cog(Setuper)
    await bot.add_cog(RoleGame)
    await bot.add_cog(Manager)
    await bot.add_cog(Funny)
    
@bot.event

async def on_ready():

    ## 06/12/2022 Added presence
    await bot.change_presence(activity=discord.Game(name="Made with 🐛s by Kadah Ne#2737"))
    
    guild = bot.get_guild(GUILD) 
    Manager = CogManage(bot,guild)
    Setuper = CogJoin(bot,Manager)
    RoleGame = CogRoleMenuG(bot,guild,Manager)
    Funny = CogFunStuff(bot)
    await setup(bot,Setuper,RoleGame,Manager,Funny)
    # await Manager.DELETE(GChannel)
    # await RoleGame.RoleM(bot.get_channel(GChannel))
    await Manager.writeLogs(f"Aegis Bot a redémarré")
    print("Aegis is running")



bot.run(TOKEN)