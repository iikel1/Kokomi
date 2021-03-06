import discord
import time
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
    print("[-] Ready as {}".format(client.user))


@client.event
async def on_message(message):
    if message.author.bot :
        return
    elif message.author.id == 942127864248156211 : 
        return
    else :
        
        await updatedata(message.author.id)
        coinlist = random.choice([0, 2, 0, 0, 1, 0, 0, 0, 1, 0, 3, 0, 0, 0, 0])
        await add_coins(message.author.id, coinlist)
        await client.process_commands(message)



@client.command()
async def shop(ctx):
    await updatedata(ctx.author.id)
    embed = discord.Embed(title='Ko Shop', description='Pet.\n<:Fish:942440582922518568> Fish - 550 <:SweetCake:942902488225443890>')
    embed.set_footer(text='use k?buy to buy itmes')
    await ctx.send(embed=embed)

# @client.command()
# async def buy(ctx, args):
#     if args == 'fish' :
#         Pet = 'Fish'

#     find = {"_id": f"{ctx.author.id}"}
#     x = mycol.find_one(find)


@client.command()
async def flip(ctx, args):
    await updatedata(ctx.author.id)
    find = {"_id": f"{ctx.author.id}"}
    x = mycol.find_one(find)
    ran = random.randint(1, 2)
    if ran == 1 :
        wincoins = x['coins'] + (int(args) * 2)
        newcoins = {"$set": { "coins": wincoins } }
        mycol.update_one(find, newcoins)
        embed = discord.Embed(title='Congrats <:KokomiWin:945760725740183572>', description=f'You won {int(args) * 2} <:SweetCake:942902488225443890>', color=0xd4f1f9)
        await ctx.send(embed=embed)
    else :
        losecoins = x['coins'] - (int(args))
        newcoins = {"$set": { "coins": losecoins } }
        mycol.update_one(find, newcoins)
        embed = discord.Embed(title='Sad <:kokomiSad:945764630947561482>', description=f'You Lost {int(args)} <:SweetCake:942902488225443890>', color=0xd4f1f9)




    
@client.command()
async def bal(ctx, member : commands.MemberConverter = None):
    if member is None:
        await updatedata(ctx.author.id)
        idh = ctx.author.id
    else :
        idh = member.id
        await updatedata(member.id)
    
    find = {"_id": f"{idh}"}
    x = mycol.find_one(find)
    embed = discord.Embed(title="**Your Bal**", color=0xd4f1f9)
    embed.add_field(name="Coins", value=f"{x['coins']} <:SweetCake:942902488225443890>")
    await ctx.send(embed=embed)
    

@client.command()
async def daily(ctx):
    await updatedata(ctx.author.id)
    dcoins = random.randint(10, 40)
    find = {"_id": f"{ctx.author.id}"}
    curr_time = time.time()
    a = mycol.find_one(find)
    delta = float(curr_time) - float(a['daily_block'])

    if delta >= 86400.0 and delta>0:
        rncoins = a['coins'] + dcoins
        newcoins = {"$set": { "coins": rncoins } }
        newtime = {"$set": { "daily_block": curr_time } }
        mycol.update_one(find, newcoins)
        mycol.update_one(find, newtime)
        await ctx.send(f"?????? ???????? ???????????? ??????????????!\n+ {dcoins} <:SweetCake:942902488225443890>")
    else :
        seconds = 86400 - delta
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        await ctx.send(f"???? ?????????? ?????? ???????????? ????????!\n- ?????????? ??????????????:\n- {int(h)} ??????????, {int(s)} ??????????, ?? {int(m)} ??????????")


async def updatedata(author):
    if mycol.count_documents({'_id': f"{author}"}):
        print("[-] User already in the database")
        return
    else :
        newuser = {
            "_id": f"{author}",
            "coins" : 0,
            "daily_block" : 0,
            "feed" : 0,
            "play" : 0,       
        }
        new_account = {
            "_id": f"{author}",
            "guild" : "None"
        }   
        mycol.insert_one(newuser)
        mycol2.insert_one(new_account)
        

        

async def add_coins(author, coins):
    find = {"_id": f"{author}"}
    a = mycol.find_one(find)
    currentcoins = a['coins']
    newcoins = currentcoins + coins
    updateuser = {"$set":{"coins":newcoins}}
    x = mycol.update_one(find, updateuser)




client.run(version['token'])

