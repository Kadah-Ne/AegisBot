from discord.ext import commands
from discord.utils import get
class CogJoin(commands.Cog):
    def __inti__(self,bot):
        self.bot = bot
        self._lastMemeber = None

    async def addRoleNew(self,target):
        Role = get(target.guild.roles, name="Nouvel Arrivant")
        await target.add_roles(Role)
    
    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel= member.guild.system_channel
        #if channel is not None:
            #await channel.send(f'Bienvenue {member.mention}.')
        self._lastMemeber = member
        await self.addRoleNew(member)
    
    
        