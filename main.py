from os import name, execv, system, environ,getenv
from sys import argv, executable, stdout
import discord
from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv
from CogJoin import CogJoin
from CogRoleMenuG import CogRoleMenuG
from CogManage import CogManage

load_dotenv(dotenv_path="config")
GUILD = int(getenv("GUILD")) #Server discord par defaut
FChannel = int(getenv("ARRIVALCHANNEL"))
GChannel = int(getenv("GAMECHANNELCHANNEL"))
Prefix = getenv("DEFAULTPREFIX")
client = discord.Client()
intents = discord.Intents.all()
TOKEN = str(getenv("TOKENP1") + getenv("TOKENP2"))
bot = commands.Bot(command_prefix='&',intents=intents)




async def setup(bot,RoleGame,Manager):
    bot.add_cog(CogJoin(bot))
    bot.add_cog(RoleGame)
    bot.add_cog(Manager)
    
@bot.event
async def on_ready():
    guild = bot.get_guild(GUILD)   
    RoleGame = CogRoleMenuG(bot,guild)
    Manager = CogManage(bot,guild)
    await setup(bot,RoleGame,Manager)
    await Manager.DELETE(FChannel)
    await Manager.DELETE(GChannel)
    await RoleGame.RoleM(bot.get_channel(GChannel),bot.get_channel(FChannel))
    print("Aegis is running")



bot.run(TOKEN)