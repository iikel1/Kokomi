import discord
from discord.ext import commands
import json


client = commands.Bot(command_prefix="k?", case_sensitive=True)


@client.event
async def on_ready():
    print("ready")





with open("env.json", "r") as f :
    version = json.load(f)

client.run(version['token'])

