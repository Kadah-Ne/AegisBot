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
        mod = -1
        numlist = []
        sides_mod = re.split("d",die,flags=re.IGNORECASE)[-1]
        if sides_mod.__contains__('+'):
            sides = re.split("+",sides_mod,flags=re.IGNORECASE)[0]
            mod = re.split("+",sides_mod,flags=re.IGNORECASE)[-1]
            item = "+"
        elif sides_mod.__contains__('-'):
            sides = re.split("-",sides_mod,flags=re.IGNORECASE)[0]
            mod = re.split("-",sides_mod,flags=re.IGNORECASE)[-1]
            item = "-"
        try :
            sides = int(sides)
            if mod != -1:
                mod = int(mod)
            occ = int(re.split("d",die,flags=re.IGNORECASE)[0])
            number = 0
            if not occ:
                occ = 1
            for i in range (occ):
                rand = random.randint(1,sides)
                numlist.append(rand)
                number += rand
            match item:
                case "+" :
                    number += mod
                case "-" :
                    number -= mod

            if occ == 1 :
                numlist.sort()
                textchain = ""
                for i in numlist: 
                        textchain += f"+ {i} "
                    
                
                textchain = textchain[0:]
                await ctx.channel.send(f"you rolled a {number}({textchain} {item} {mod}) on the D{sides}")
            else : 
                await ctx.channel.send(f"you rolled a {number}({textchain} {item} {mod}) on the {occ} D{sides}")
            
            
        except :
            await ctx.channel.send("Utilisez le format [x]D[y]+/-[z] pour la commande ou x,y et z sont des nombres entiers")
        