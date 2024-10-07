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

        ## Added GGST Role 14/04/2022
        self.dicoRole["GGST"] = get(self.guild.roles, name="GGST")

        ## Added Striker Role 15/05/2023
        self.dicoRole["Omega"] = get(self.guild.roles, name="Striker")

        ## Added Grindframe Role 10/10/2023
        self.dicoRole["WF"] = get(self.guild.roles, name="GrindFrame")

        ## Added Altered-addict Role 7/10/2024
        self.dicoRole["ALT"] = get(self.guild.roles, name="ALTERED ADDICT")

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

        ## Added GGST Role 14/04/2022
        self.dicoImg["GGST"] = self.bot.get_emoji(1096438707491451002)

        ## Added Striker Role 15/05/2023
        self.dicoImg["Omega"] = self.bot.get_emoji(1103284633954680842)

        ## Added Grindframe Role 10/10/2023
        self.dicoImg["WF"] = self.bot.get_emoji(1161221507465355265)

        ## Added Altered-addict Role 7/10/2024
        self.dicoRole["ALT"] = self.bot.get_emoji(1292922742714400892)

    async def RoleM(self,channelG,channelR):
        await self.setupDicoI()
        await self.setupDicoR()
        await self.MenuR(channelR)
        await self.MenuG(channelG)
        
    
    async def MenuR(self,channel):
        message = await channel.send(f"Réagissez pour recevoir le role adéquat :\n{self.dicoImg['Member']} : `Membre du server`\n{self.dicoImg['Event']} : `Membre temporaire invité(e) pour un **Event**, restreint l'accès au server !`")
        await message.add_reaction(self.dicoImg["Member"])
        await message.add_reaction(self.dicoImg["Event"])

        self.msgIdStatus = message.id

    async def MenuG(self,channel):
        message = await channel.send(f"Réagissez pour recevoir le role adéquat :\n{self.dicoImg['LOL']} : `LOL`\n{self.dicoImg['YGO']} : `YGO`\n{self.dicoImg['APEX']} : `APEX`\n{self.dicoImg['FF']} : `FFXIV`\n{self.dicoImg['CIV']} : `CIV`\n{self.dicoImg['Valo']} : `Valorant`\n{self.dicoImg['GGST']} : `Guilty Gear`\n{self.dicoImg['Omega']} : `Omega Stiker`\n{self.dicoImg['WF']} : `Warframe`\n{self.dicoImg['ALT']} : `Altered`")
        await message.add_reaction(self.dicoImg["LOL"])
        await message.add_reaction(self.dicoImg["YGO"])
        await message.add_reaction(self.dicoImg["FF"])
        await message.add_reaction(self.dicoImg["APEX"])

        ## 07/12/2022 Added CIV role
        await message.add_reaction(self.dicoImg["CIV"])

        ## 07/12/2022 Added CIV role
        await message.add_reaction(self.dicoImg["Valo"])

        ## 07/12/2022 Added CIV role
        await message.add_reaction(self.dicoImg["GGST"])

        ## Added Striker Role 15/05/2023
        await message.add_reaction(self.dicoImg["Omega"])
        self.msgIdGame = message.id

        ## Added Grindframe Role 10/10/2023
        await message.add_reaction(self.dicoImg["WF"])

        ## Added ALTERED ADDICT Role 10/10/2023
        await message.add_reaction(self.dicoImg["ALT"])

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

            ## Added Civ role 14/04/2022
            elif reaction == self.dicoImg["GGST"]:
                await self.addRole(user,self.dicoRole["GGST"]) 

            ## Added Striker Role 15/05/2023    
            elif reaction == self.dicoImg["Omega"]:
                await self.addRole(user,self.dicoRole["Omega"]) 

            ## Added Grindframe Role 10/10/2023
            elif reaction == self.dicoImg["WF"]:
                await self.addRole(user,self.dicoRole["WF"]) 

            ## Added ALTERED ADDICT Role 7/10/2024
            elif reaction == self.dicoImg["ALT"]:
                await self.addRole(user,self.dicoRole["ALT"]) 
                
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
            
            ## Added GGST role 14/04/2022
            elif reaction == self.dicoImg["GGST"]:
                await self.rmvRole(user,self.dicoRole["GGST"])  

            ## Added Striker Role 15/05/2023 
            elif reaction == self.dicoImg["Omega"]:
                await self.rmvRole(user,self.dicoRole["Omega"])  

            ## Added Grindframe Role 10/10/2023
            elif reaction == self.dicoImg["WF"]:
                await self.rmvRole(user,self.dicoRole["WF"])
            
            ## Added ALTERED ADDICT Role 7/10/2024
            elif reaction == self.dicoImg["WF"]:
                await self.rmvRole(user,self.dicoRole["ALT"])
                
                
        
    
        