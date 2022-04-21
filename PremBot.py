import os
import discord
import asyncio
import gc
import pandas as pd

from discord.ext import commands

bot_auth = os.environ.get('BOT_TOKEN')
point = os.environ.get('POINT')

bot = commands.Bot(command_prefix='!')
gc.collect()

loop_list = []

RunLoop = True

check_func = lambda msg: not msg.pinned

# -----------------------------Setup functions-----------------------------------


async def UpdatePoints(ctx):
        last_sort1 = []
        last_sort2 = []
        while RunLoop:
            embed1 = discord.Embed(title="Current Team Points", colour=0x87CEEB)
            embed2 = discord.Embed(title="Current Team Sweets", colour=0x6A0DAD)
            try:
                points = pd.read_csv(point)
            except:
                print("Error retrieving point spreadsheet link")
            list1 = {}
            list2 = {}
            for i in range(len(points)):
                list1[points.values[i][0]] = points.values[i][1]
                list2[points.values[i][0]] = points.values[i][2]
            #print(list)
            sorts1 = sorted(list1.items(), key=lambda x: x[1], reverse=True)
            sorts2 = sorted(list2.items(), key=lambda x: x[1], reverse=True)
            #print("here")
            #print(sorts)
            #print(last_sort)
            if sorts1 != last_sort1 or sorts2 != last_sort2:
                await ctx.message.channel.purge(limit=20,check=check_func)
                for i in sorts1:
                    embed1.add_field(name=f"{i[0]}", value=f"{i[1]}", inline="False")
                for i in sorts2:
                    embed2.add_field(name=f"{i[0]}", value=f"{i[1]}", inline="False")
                await ctx.send(embed=embed1)
                await ctx.send(embed=embed2)
            last_sort1 = sorts1
            last_sort2 = sorts2
            await asyncio.sleep(60)




async def check_channel(ctx):
    try:
        if ctx.guild.id == 793827726687076394:
            if ctx.channel.id == 861695150890942524:
                return True

    except:
        await ctx.send("please use this command only in the correct channel")
        return False
    return False

async def pm_person(msg, disc_id):
    user = await bot.fetch_user(disc_id)
    # print(str(user.dm_channel))
    dm = user.dm_channel
    if dm == None:
        dm = await user.create_dm()
    await dm.send(msg)



# ------------Actually Commands------------------
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')



@bot.command()
@commands.check(check_channel)
async def start(ctx):
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Ba Services Bingo Event Spring 2022"))
    await ctx.message.channel.purge(limit=20,check=check_func)
    await pm_person("Started", ctx.author.id)
    loop = bot.loop.create_task(UpdatePoints(ctx))
    loop_list.append(loop)


@bot.command()
@commands.check(check_channel)
async def stop(ctx):
    await ctx.message.channel.purge(limit=20,check=check_func)
    await pm_person("Stopped", ctx.author.id)
    for i in loop_list:
        i.cancel()
    loop_list.pop()






bot.run(bot_auth)

