from os import name, execv, system, environ,getenv
from sys import argv, executable, stdout
import discord
from discord.utils import get
from discord.ext import commands
from dotenv import load_dotenv
from CogTest import CogTest
from CogJoin import CogJoin
from CogRoleMenuG import CogRoleMenuG

load_dotenv(dotenv_path="config")
GUILD = int(getenv("GUILD")) #Server discord par defaut
client = discord.Client()
intents = discord.Intents.all()
TOKEN = str(getenv("TOKENP1") + getenv("TOKENP2"))
bot = commands.Bot(command_prefix='&',intents=intents)




async def setup(bot,RoleGame):
    bot.add_cog(CogJoin(bot))
    bot.add_cog(RoleGame)
    
@bot.event
async def on_ready():
    guild = bot.get_guild(GUILD)   
    RoleGame = CogRoleMenuG(bot,guild)
    await setup(bot,RoleGame)
    await RoleGame.RoleM(0,bot.get_channel(1016701714478411827))
    print("Aegis is running")

bot.run(TOKEN)