from os import name, execv, system, environ,getenv
from sys import argv, executable, stdout
import discord
from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv
from CogJoin import CogJoin
from CogRoleMenuG import CogRoleMenuG
from CogManage import CogManage
from CogFunStuff import CogFunStuff

load_dotenv(dotenv_path="config")
GUILD = int(getenv("GUILD")) #Server discord par defaut
FChannel = int(getenv("ARRIVALCHANNEL"))
GChannel = int(getenv("GAMECHANNEL"))
Prefix = getenv("DEFAULTPREFIX")
# client = discord.Client()
intents = discord.Intents.all()
TOKEN = str(getenv("TOKENP1") + getenv("TOKENP2"))
bot = commands.Bot(command_prefix=Prefix,intents=intents)




async def setup(bot,Setuper,RoleGame,Manager,Funny):
    bot.add_cog(Setuper)
    bot.add_cog(RoleGame)
    bot.add_cog(Manager)
    bot.add_cog(Funny)
    
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
    await Manager.DELETE(FChannel)
    await Manager.DELETE(GChannel)
    await RoleGame.RoleM(bot.get_channel(GChannel),bot.get_channel(FChannel))
    await Manager.writeLogs(f"Aegis Bot a redémarré")
    print("Aegis is running")



bot.run(TOKEN)