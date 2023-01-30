from discord.ext import commands
from discord.utils import get
import discord

class CogRoleMenuG(commands.Cog):
    def __init__(self,bot,guild,Manager):
        self.bot = bot
        self.msgIdStatus = None
        self.msgIdGame = None
        self.dicoImg = {}
        self.dicoRole = {}
        self.guild = guild
        self.Manager = Manager


    async def addRole(self,target,Role):
        await target.add_roles(Role)
    
    async def rmvRole(self,target,Role):
        await target.remove_roles(Role)

    async def setupDicoR(self):
        self.dicoRole["New"] = get(self.guild.roles, name="Nouvel Arrivant")
        self.dicoRole["Member"] = get(self.guild.roles, name="Random Members")
        self.dicoRole["Event"] = get(self.guild.roles, name="Event")
        self.dicoRole["FF"] = get(self.guild.roles, name="FFXIV")
        self.dicoRole["LOL"] = get(self.guild.roles, name="League of Legends")
        self.dicoRole["YGO"] = get(self.guild.roles, name="Yu gi oh")
        self.dicoRole["APEX"] = get(self.guild.roles, name="Apex Legends")

        ## Added Civ role 06/12/2022
        self.dicoRole["CIV"] = get(self.guild.roles, name="CIV")
        
        ## Aded Valo role 30/01/2023
        self.dicoRole["Valo"] = get(self.guild.roles, name="Valorant")

    async def setupDicoI(self):
        self.dicoImg["Member"] = self.bot.get_emoji(708637710608498698)
        self.dicoImg["Event"] = self.bot.get_emoji(864745278685970452)
        self.dicoImg["FF"] = self.bot.get_emoji(975748447481241630)
        self.dicoImg["LOL"] = self.bot.get_emoji(838472239761850399)
        self.dicoImg["YGO"] = self.bot.get_emoji(781176640721256449)
        self.dicoImg["APEX"] = self.bot.get_emoji(975748414136533092)

        ## Added Civ role 06/12/2022
        self.dicoImg["CIV"] = self.bot.get_emoji(1049706958816546926)
        
        ## Aded Valo role 30/01/2023
        self.dicoImg["Valo"] = self.bot.get_emoji(1069601356878463068)

        
    
    async def RoleM(self,channelG,channelR):
        await self.setupDicoI()
        await self.setupDicoR()
        await self.MenuR(channelR)
        await self.MenuG(channelG)
        
    
    async def MenuR(self,channel):
        message = await channel.send(f"Réagissez pour recevoir le role adéquat :\n{self.dicoImg['Member']} : `Membre`\n{self.dicoImg['Event']} : `Simp`")
        await message.add_reaction(self.dicoImg["Member"])
        await message.add_reaction(self.dicoImg["Event"])

        self.msgIdStatus = message.id

    async def MenuG(self,channel):
        message = await channel.send(f"Réagissez pour recevoir le role adéquat :\n{self.dicoImg['LOL']} : `LOL`\n{self.dicoImg['YGO']} : `YGO`\n{self.dicoImg['APEX']} : `APEX`\n{self.dicoImg['FF']} : `FFXIV`\n{self.dicoImg['CIV']} : `CIV`")
        await message.add_reaction(self.dicoImg["LOL"])
        await message.add_reaction(self.dicoImg["YGO"])
        await message.add_reaction(self.dicoImg["FF"])
        await message.add_reaction(self.dicoImg["APEX"])

        ## 07/12/2022 Added CIV role
        await message.add_reaction(self.dicoImg["CIV"])

        self.msgIdGame = message.id
    

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        reaction = self.bot.get_emoji(payload.emoji.id)
        user = payload.member
        if  user.id != 916425159601180703 and message.id == self.msgIdStatus:
            if reaction == self.dicoImg["Member"]:
                await self.addRole(user,self.dicoRole["Member"])
                await self.rmvRole(user,self.dicoRole["New"])
            elif reaction == self.dicoImg["Event"]:
                await self.addRole(user,self.dicoRole["Event"])
                await self.rmvRole(user,self.dicoRole["New"])
            

        elif user.id != 916425159601180703 and message.id == self.msgIdGame:
            if reaction == self.dicoImg["LOL"]:
                await self.addRole(user,self.dicoRole["LOL"])
            elif reaction == self.dicoImg["YGO"]:
                await self.addRole(user,self.dicoRole["YGO"])
            elif reaction == self.dicoImg["FF"]:
                await self.addRole(user,self.dicoRole["FF"])
            elif reaction == self.dicoImg["APEX"]:
                await self.addRole(user,self.dicoRole["APEX"])

            ## Added Civ role 06/12/2022
            elif reaction == self.dicoImg["CIV"]:
                await self.addRole(user,self.dicoRole["CIV"])   
                
            ## Added Valorant role 30/01/2023
            elif reaction == self.dicoImg["Valo"]:
                await self.addRole(user,self.dicoRole["Valo"])    

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        reaction = self.bot.get_emoji(payload.emoji.id)
        user = get(self.guild.members, id=payload.user_id)
        if user.id != 916425159601180703 and message.id == self.msgIdGame:
            if reaction == self.dicoImg["LOL"]:
                await self.rmvRole(user,self.dicoRole["LOL"])
            elif reaction == self.dicoImg["YGO"]:
                await self.rmvRole(user,self.dicoRole["YGO"])
            elif reaction == self.dicoImg["FF"]:
                await self.rmvRole(user,self.dicoRole["FF"])
            elif reaction == self.dicoImg["APEX"]:
                await self.rmvRole(user,self.dicoRole["APEX"]) 

            ## Added Civ role 06/12/2022
            elif reaction == self.dicoImg["CIV"]:
                await self.rmvRole(user,self.dicoRole["CIV"])
                
            ## Added Valorant role 30/01/2023
            elif reaction == self.dicoImg["Valo"]:
                await self.rmvRole(user,self.dicoRole["Valo"])    
            

                
                
        
    
        