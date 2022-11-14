from discord.ext import commands
from discord.utils import get
import discord

class CogRoleMenuG(commands.Cog):
    def __init__(self,bot,guild):
        self.bot = bot
        self.guild = guild
        self.dicoRole = {}
        self.dicoImg = {}
        self.msgId = None

    async def setupDicoR(self):
        self.dicoRole["Member"] = get(self.guild.roles, name="Random Members")
        self.dicoRole["Event"] = get(self.guild.roles, name="Event")
        self.dicoRole["FF"] = get(self.guild.roles, name="FFXIV")
        self.dicoRole["LOL"] = get(self.guild.roles, name="League of Legends")
        self.dicoRole["YGO"] = get(self.guild.roles, name="Yu gi oh")
        self.dicoRole["APEX"] = get(self.guild.roles, name="Apex Legends")

    async def setupDicoI(self):
        self.dicoImg["Member"] = "<:OG_Smug:708637710608498698>"
        self.dicoImg["Event"] = "<:CAT_Simp:864745278685970452>"
        self.dicoImg["FF"] = "<:FFcroixbatonv:975748447481241630>"
        self.dicoImg["LOL"] = "<:LOL_12:838472239761850399>"
        self.dicoImg["YGO"] = "<:AM_Kaiba_Deleted:781176640721256449>"
        self.dicoImg["APEX"] = "<:ApexLegends:975748414136533092>"
    
    async def RoleM(self,channelG,channelR):
        await self.setupDicoI()
        await self.setupDicoR()
        await self.MenuR(channelR)
    
    async def MenuR(self,channel):
        message = await channel.send(f"Réagissez pour recevoir le role adéquoit :\n{self.dicoImg['Member']} : `Membre`\n{self.dicoImg['Event']} : `Simp`")
        await message.add_reaction(self.dicoImg["Member"])
        await message.add_reaction(self.dicoImg["Event"])

        ####################
        self.msgId = message.id

        # def check(reaction, user):
        #             return user != message.author and (str(reaction.emoji) == self.dicoImg["Member"] or str(reaction.emoji) == self.dicoImg["Event"])
        # while(True):
        #     try:
        #         reaction, user = await self.bot.wait_for('reaction_add', check=check)
        #         print(user)
        #     except Exception as e:
        #         a=2
        #         print(a)
        #     else :
        #         if (str(reaction) == self.dicoImg["Member"]):
        #             await user.add_roles(self.dicoRole["Member"])
        #         elif (str(reaction) == self.dicoImg["Event"]):
        #             await user.add_roles(self.dicoRole["Event"])

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        reaction = message.reactions
        user = payload.member
        print(reaction)
        # if reaction == self.dicoImg["Event"] and message == self.msgId and user.id != 916425159601180703:
        #     print("yes")
            

                
                
        
    
        