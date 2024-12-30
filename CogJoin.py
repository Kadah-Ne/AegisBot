from discord.ext import commands
from discord.utils import get
class CogJoin(commands.Cog):
    def __inti__(self,bot,Manager):
        self.bot = bot
        self.Manager = Manager

    async def addRoleNew(self,target):
        Role = get(target.guild.roles, name="Random Members")
        await target.add_roles(Role)
    
    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel= member.guild.system_channel
        if channel is not None:
            await channel.send(f'Bienvenue {member.mention}.')
        await self.addRoleNew(member)
        await self.Manager.writeLogs(f"{member} as joined the server")
    
    
        