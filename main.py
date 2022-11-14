from os import name, execv, system, environ,getenv
from sys import argv, executable, stdout
import discord
from discord.ext import commands
from dotenv import load_dotenv
from CogTest import CogTest
from CogJoin import CogJoin
from CogRoleMenuG import CogRoleMenuG
clear, back_slash = "clear", "/"
load_dotenv(dotenv_path="config")
GUILD = int(getenv("GUILD")) #Server discord par defaut
client = discord.Client()
intents = discord.Intents.all()
TOKEN = str(getenv("TOKENP1") + getenv("TOKENP2"))
bot = commands.Bot(command_prefix='&',intents=intents)
guild = bot.get_guild(GUILD)

async def setup(bot):
    #bot.add_cog(CogTest(bot))
    bot.add_cog(CogJoin(bot))
    bot.add_cog(CogRoleMenuG(bot,guild))
    
@bot.event
async def on_ready():
    guild = bot.get_guild(GUILD)
    print("Aegis is running")
    await setup(bot)
    RoleGame = CogRoleMenuG(bot,guild)
    await RoleGame.RoleM(0,bot.get_channel(1016701714478411827))

bot.run(TOKEN)