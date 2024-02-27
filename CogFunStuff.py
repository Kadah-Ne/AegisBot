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
        occ = -1
        item =""
        sides_mod = re.split("d",die,flags=re.IGNORECASE)[-1]
        if sides_mod.__contains__('+'):
            sides = re.split("+",sides_mod,flags=re.IGNORECASE)[0]
            mod = re.split("+",sides_mod,flags=re.IGNORECASE)[-1]
            item = "+"
        elif sides_mod.__contains__('-'):
            sides = re.split("-",sides_mod,flags=re.IGNORECASE)[0]
            mod = re.split("-",sides_mod,flags=re.IGNORECASE)[-1]
            item = "-"
        else : 
            sides = re.split("-",sides_mod,flags=re.IGNORECASE)[0]
        
        try :
            sides = int(sides)
            
            if mod != -1:
                mod = int(mod)
            if (re.split("d",die,flags=re.IGNORECASE)[0]) :
                 
                occ = int(re.split("d",die,flags=re.IGNORECASE)[0])
            
            number = 0
            if occ == -1:
                occ = 1
            
            for i in range (occ):
                rand = random.randint(1,sides)
                numlist.append(rand)
                number += rand
            print(item)
            if item == "+":
                number += mod
            elif item == "-" :
                number -= mod
            print(occ)
            if occ == 1 :
                numlist.sort()
                textchain = ""
                for i in numlist: 
                        textchain += f"+ {i} "
                
                textchain = textchain[0:]
                if item == "":
                    print(f"you rolled a {number} on the D{sides}")
                else : 
                     print(f"you rolled a {number}({numlist[0]} {item} {mod}) on the D{sides}")
            else : 
                print(f"you rolled a {number}({textchain} {item} {mod}) on the {occ} D{sides}")
            
            
        except :
            print("Utilisez le format [x]D[y]+/-[z] pour la commande ou x,y et z sont des nombres entiers")
        
