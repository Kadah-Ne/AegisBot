from discord.ext import commands
from discord.utils import get
import re
import random
import discord
import math

class CogFunStuff(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
    def rollDie(self,dice:int) :
        return random.randint(1,dice)
    
    def splitCommande(self,input):
        trimmed = input.replace(" ","")
        mod = -1
        occ = -1
        opp = ""
        kh = -1
        kl = -1
        splitD = re.split("d",trimmed,flags=re.IGNORECASE)
        sides_mods = splitD[-1].lower()
   
        if "kh" in sides_mods:
            sides_mods,kh = sides_mods.split("kh")
        elif 'kl' in sides_mods :
            sides_mods,kl = sides_mods.split("kl")
        occ = splitD[0]

        if sides_mods.__contains__('+'):
            sides = sides_mods.split("+")[0]
            mod = sides_mods.split("+")[-1]
            opp = "+"
        elif sides_mods.__contains__('-'):
            sides = sides_mods.split("-")[0]
            mod = sides_mods.split("-")[-1]
            opp = "-"
        else : 
            sides = re.split("-",sides_mods,flags=re.IGNORECASE)[0]
        
        return(mod,occ,opp,sides,kh,kl)

    @commands.command (name="roll", aliases = ["Roll","rolls","Rolls","r","R"])
    async def roll(self,ctx,* die : str):
        die = ''.join([str(ele) + '' for ele in die])
        numlist = []
        mod,occ,item,sides,kh,kl = self.splitCommande(die)

        try :
            
            sides = int(sides)
            if sides >= 2000:
                raise Exception("Fuckyou")

            if mod != -1:
                mod = int(mod)                       
            number = 0
            if occ == "":
                occ = 1
            else:
                occ = int(occ)
            if occ < 1 or occ >=1000 :
                raise Exception("Fuck You")
            for i in range (occ):
                rand = self.rollDie(sides)
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
                if (kh == -1 and kl == -1) or (len(numlist) < int(kh) or len(numlist) < int(kl)) :
                    for i in numlist: 
                        textchain += f"+{i}"
                    
                    textchain = textchain[1:]
                    
                    if len(textchain) > 1500:
                        await ctx.channel.send(f"you rolled a {number} on the {occ} D{sides}")
                    else :
                        if item == "":
                            await ctx.channel.send(f"you rolled a {number} : ({textchain}) on the {occ} D{sides}")
                        else :
                            await ctx.channel.send(f"you rolled a {number} : ({textchain}{item}[{mod}]) on the {occ} D{sides}")
                else :
                    kh = int(kh)
                    kl = int(kl)
                    if kh > -1 :
                        newList = numlist[-1*int(kh):]
                    else :
                        newList = numlist[:int(kl)]
                    for i in newList: 
                            textchain += f"+{i}"
                    textchain = textchain[1:]
                    if item == "":
                        number = sum(newList)
                        if kh > -1 :
                            await ctx.channel.send(f"your {kh} highest rolls did {number} : ({textchain}) on the {occ} D{sides}")
                        else : 
                            await ctx.channel.send(f"your {kl} lowest rolls did {number} : ({textchain}) on the {occ} D{sides}")
                    else : 
                        if item == "+" :
                            number = sum(newList)+mod
                        else:
                            number = sum(newList)-mod
                        if kh > -1 :
                            await ctx.channel.send(f"your {kh} highest rolls did {number} : ({textchain})[{item}{mod}] on the {occ} D{sides}")
                        else : 
                            await ctx.channel.send(f"your {kl} lowest rolls did {number} : ({textchain})[{item}{mod}] on the {occ} D{sides}")
        except :
            await ctx.channel.send("Utilisez le format [x]D[y]+/-[z] pour la commande ou x,y et z sont des nombres entiers")
        
    
        