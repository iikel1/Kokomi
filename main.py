import discord
from discord.ext import commands
import json
import pymongo
from dec import *
import random

with open("env.json", "r") as f :
    version = json.load(f)


client = commands.Bot(command_prefix="k?", case_sensitive=True)
myclient = pymongo.MongoClient(version['mongo'])
mydb = myclient["Players"]
mycol = mydb["coins"]
mycol2 = mydb["accounts"]






@client.event
async def on_ready():
    print("ready")


@client.event
async def on_message(message):
    print(message.author.id)
    await updatedata(message.author.id)
    coinlist = random.choice([0, 2, 0, 0, 1, 0, 0, 0, 1, 0, 3, 0, 0, 0])
    await add_coins(message.author.id, coinlist)
    await client.process_commands(message)

@client.command()
async def clear(ctx, amount: int = None):
	await ctx.channel.purge(limit=amount)




async def updatedata(author):
    try :
        
        mycol.find_one({"_id": author})
        pass
    except :
        newuser = {
            "_id": author,
            "coins" : 0
        }
        new_account = {
            "_id": author,
        }
        mycol2.insert_one(new_account)
        mycol.insert_one(newuser)

async def add_coins(author, coins):

    find = {"_id": author}
    a = mycol.find_one(find)
    currentcoins = a['coins']
    newcoins = currentcoins + coins
    updateuser = {"$set": { "coins": newcoins } }
    x = mycol.update_one(find, updateuser)




client.run(version['token'])

