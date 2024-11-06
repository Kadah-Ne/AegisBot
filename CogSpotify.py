from discord.ext import commands
from discord.utils import get
import discord
from dotenv import load_dotenv
import json 
import spotipy 
import webbrowser
from spotipy.oauth2 import SpotifyClientCredentials
import os

class CogSpotify(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        load_dotenv()
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        username = os.getenv("USERNAME")
        redirect_uri = 'a'
        scope = "user-read-playback-state,user-modify-playback-state"
        client_credentials_manager = SpotifyClientCredentials()
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        # self.sp = spotipy.Spotify(
        #         auth_manager=spotipy.SpotifyOAuth(
        #         client_id=client_id,
        #         client_secret=client_secret,
        #         redirect_uri=redirect_uri,    
        #         scope=scope, open_browser=False))

    
    @commands.command (name = "RequestMusic", aliases = ["RM","rm","Music","music"])
    async def RequestMusic(self,ctx,* message : str):
        token_info = self.sp.auth_manager.get_access_token()
        flag = spotipy.SpotifyOAuth.is_token_expired(token_info)
        if(flag) :
            self.sp.auth_manager.refresh_access_token(token_info['refresh_token'])
            print("Refreshing Access Token.")
        message = ' '.join(message)
        results = self.sp.search(message, 1, 0, "track") 
        songs_dict = results['tracks'] 
        song_items = songs_dict['items'] 
        song = song_items[0]['id'] 
        # webbrowser.open(song) 
        self.sp.start_playback(uris=[f'spotify:track:{song}'])


        
    

        
        
    
