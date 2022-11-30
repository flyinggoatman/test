import discord
import re
import easygui
from easygui import *
from re import search
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re
import json
import base64
import os
import webbrowser
import pyperclip
import win32com.client as comclt
import time
import pyautogui
import discord
from configparser import ConfigParser
import datetime


intents = discord.Intents.all()
client = discord.Client(command_prefix='/', intents=intents)


# Creates or checks for config
if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f) 
else:
    print("Please enter your token and the channel ID of the Discord channel you'd like to use.")
    print("If left blank, you'll need to go to the config.json to set them.")
    token = str(input("Bot Token: ") or "token goes here...")
    discordChannel = str(input("Channel ID:  ") or "000000000000000000")
    configTemplate = {"Token": (token), "Prefix": "!","discordChannel": (discordChannel)}
    print("The script will now crash and show an error. Run 'python QualityYouTube.py' again.")
    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f) 
token = configData["Token"]
prefix = configData["Prefix"]
discordChannel = configData["discordChannel"]
# Boots up the bot 
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
# Bot is checking messages
@client.event
async def on_message(message):
    if message.author == client.user:
       return    
    if message.content.startswith('/channel '):
        print (message.content)
        channelURL = message.content
        channelURL = channelURL.replace("/channel ", "")
        print(channelURL)
        discordChannelInt = int(discordChannel)
        if (discordChannelInt == message.channel.id):
            if re.search("http", channelURL):
                if re.search("://", channelURL):
                    if re.search("youtu", channelURL):
                        
                        
                        soup = BeautifulSoup(requests.get(channelURL, cookies={'CONSENT': 'YES+1'}).text, "html.parser")
                        data = re.search(r"var ytInitialData = ({.*});", str(soup.prettify())).group(1)
                        json_data = json.loads(data)
                        
                        # Finds channel information #
                        channel_id   = json_data["header"]["c4TabbedHeaderRenderer"]["channelId"]
                        channel_name = json_data["header"]["c4TabbedHeaderRenderer"]["title"]
                        channel_logo = json_data["header"]["c4TabbedHeaderRenderer"]["avatar"]["thumbnails"][2]["url"]
                        channel_id_link = "https://www.youtube.com/channel/"+channel_id
                        # Prints Channel information to console #
                        print("Channel ID: "+channel_id)
                        print("Channel Name: "+channel_name)
                        print("Channel Logo: "+channel_logo)
                        print("Channel ID: "+channel_id_link)
                        author = message.author
                        #Messages
                        Message_1 = channel_name+" was posted by "+(author.mention)+"(now.shifttime(""))"+""
                        timeOutMessage10 = " This message will be deleted in 10 seounds."
                        timeOutMessage60 = " This message will be deleted in 60 seounds."
                        noURL = " This does not contain a URL."
                        invalidURL = " This URL is not supported. Please enter a valid URL."
                        notChannel =  """Make sure the channel follows one of the following formats starting with http or https. 
                        \r - http:://youtube.com/user/username
                        \r - http://youtube.com/channel/username
                        \r - http://youtube.com/@username\r\r
                        ***We hope to add video support soon***"""
                        num60 = 60
                        num10 = 10
                        
                        
                        
                        await message.channel.send(channel_id_link)
                    elif message.content.endswith('.com/'):
                        await message.channel.send(author.mention+notChannel+timeOutMessage60, delete_after=num60)
                    elif not message.content.includes('channel') or message.content('user') or message.content('@'):
                        author = message.author
                        await message.channel.send(author.mention+invalidURL+timeOutMessage60, delete_after=num60)
                    elif message.content.excludes('.com') or message.content.excludes('wwww') or message.content.excludes(''):
                        author = message.author
                        await message.channel.send(author.mention+noURL+timeOutMessage10, delete_after=num10)
            else:
                
                print("incorrect channel")
                

    

client.run(token)