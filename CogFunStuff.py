from discord.ext import commands
from discord.utils import get
import re
import random
import discord

class CogFunStuff(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
    
    @commands.command (name="roll", aliases = ["Roll","rolls","Rolls"])
    async def roll(self,ctx,die : str):
        try :
            sides = int(re.split("d",die,flags=re.IGNORECASE)[-1])
            occ = int(re.split("d",die,flags=re.IGNORECASE)[0])
            number = 0
            if not occ:
                occ = 1
            for i in range (occ):
                number += random.randint(1,sides)
            if occ == 1 :
                await ctx.channel.send(f"you rolled a {number} on the D{sides}")
            else : 
                await ctx.channel.send(f"you rolled a {number} on the {occ} D{sides}")
        except :
            await ctx.channel.send("Utilisez le format [x]D[y] pour la commande ou x et y sont des nombres entiers")
        