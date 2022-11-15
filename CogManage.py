from discord.ext import commands
from discord.utils import get
import discord

class CogManage(commands.Cog):
    def __init__(self,bot,guild):
        self.bot = bot
        self.guild = guild

    
    @commands.command (name="promote", aliases = ["Promote"])
    @commands.has_role('Staff')
    async def promote(self,ctx,peon : discord.Member):
        role = get(self.guild.roles, name="Event")
        if role in peon.roles:
            await peon.add_roles(get(self.guild.roles, name="Random Members"))
            await peon.remove_roles(role)


    @commands.command(name = "Purge")
    @commands.has_permissions(manage_messages=True)
    async def deletAllMessages(self,ctx, channelID : int = None):
        if channelID:
            channel = channelID
        else:
            channel = ctx.channel.id
        await self.DELETE(channel)
        

    async def DELETE(self,channelId : int):
        channel = self.bot.get_channel(channelId)
        messages = await channel.history(limit=10).flatten()
        for i in messages:
            await i.delete()

    @commands.command (name = "Prefix", aliases = ["prefix","p","P"])
    @commands.has_role('Staff')
    async def pref(self,ctx,NEWPREFIX : str = None):
        if NEWPREFIX:
            f = open("config","r")
            lines = f.readlines()
            f.close()
            f = open("config","w")
            for line in lines:
                if "DEFAULTPREFIX=" not in line:
                    f.write(line)
            f.write("DEFAULTPREFIX="+NEWPREFIX)
            await ctx.channel.send("Le prefix a été changer a `"+NEWPREFIX+"`")
        else:
            await ctx.channel.send(f"Mon prefix actuel est : `{PREFIX}`")
