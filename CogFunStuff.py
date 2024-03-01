from discord.ext import commands
from discord.utils import get
import re
import random
import discord
import math

class CogFunStuff(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
    
    @commands.command (name="roll", aliases = ["Roll","rolls","Rolls","r","R"])
    async def roll(self,ctx,die : str):
        die = die.replace(" ","")
        mod = -1
        numlist = []
        occ = -1
        item =""
        sides_mod = re.split("d",die,flags=re.IGNORECASE)[-1]
 
        if sides_mod.__contains__('+'):
            sides = sides_mod.split("+")[0]
            mod = sides_mod.split("+")[-1]
            item = "+"
        elif sides_mod.__contains__('-'):
            sides = sides_mod.split("-")[0]
            mod = sides_mod.split("-")[-1]
            item = "-"
        else : 
            sides = re.split("-",sides_mod,flags=re.IGNORECASE)[0]
        
        try :
            
            sides = int(sides)
            if sides >= 2000:
                raise Exception("Fuckyou")

            if mod != -1:
                mod = int(mod)
            if (re.split("d",die,flags=re.IGNORECASE)[0]) :
                 
                occ = int(re.split("d",die,flags=re.IGNORECASE)[0])
                
            number = 0
            if occ == -1:
                occ = 1
            if occ < 1 or occ >=1000 :
                raise Exception("Fuck You")
            for i in range (occ):
                rand = random.randint(1,sides)
                numlist.append(rand)
                number += rand
            if item == "+":
                number += mod
            elif item == "-" :
                number -= mod
            
            if occ == 1 :
               
                if item == "":
                    await ctx.channel.send(f"you rolled a {number} on the D{sides}")
                else : 
                    await ctx.channel.send(f"you rolled a {number} : ({numlist[0]}{item}[{mod}]) on the D{sides}")
            else : 
                numlist.sort()
                textchain = ""
                for i in numlist: 
                        textchain += f"+{i}"
                
                textchain = textchain[1:]
                print(textchain)
                if len(textchain) > 1500:
                    if item == "":
                        await ctx.channel.send(f"you rolled a {number} on the {occ} D{sides}")
                    else :
                        await ctx.channel.send(f"you rolled a {number} on the {occ} D{sides}")
                else :
                    if item == "":
                        await ctx.channel.send(f"you rolled a {number} : ({textchain}) on the {occ} D{sides}")
                    else :
                        await ctx.channel.send(f"you rolled a {number} : ({textchain}{item}[{mod}]) on the {occ} D{sides}")
        except :
            await ctx.channel.send("Utilisez le format [x]D[y]+/-[z] pour la commande ou x,y et z sont des nombres entiers")
        
