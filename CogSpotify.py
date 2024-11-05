from discord.ext import commands
from discord.utils import get
import discord
from dotenv import load_dotenv
import os

class CogSpotify(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

        load_dotenv()

        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")

        
    

        
        
    
