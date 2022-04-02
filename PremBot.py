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

# -----------------------------Setup functions-----------------------------------


async def UpdatePoints(ctx):
        while RunLoop:

            embed = discord.Embed(title="Current Team points", colour=0x87CEEB)
            try:
                points = pd.read_csv(point)
            except:
                print("Error retrieving point spreadsheet link")
            for i in range(len(points)):
                embed.add_field(name=f"{points.values[i][0]}", value=f"{points.values[i][1]}", inline="False")

            last_msg = await ctx.send(embed=embed)
            await asyncio.sleep(60)
            await last_msg.delete()




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
    await ctx.message.channel.purge(limit=20)
    await pm_person("Started", ctx.author.id)
    loop = bot.loop.create_task(UpdatePoints(ctx))
    loop_list.append(loop)


@bot.command()
@commands.check(check_channel)
async def stop(ctx):
    await ctx.message.channel.purge(limit=20)
    await pm_person("Stopped", ctx.author.id)
    for i in loop_list:
        i.cancel()
    loop_list.pop()






bot.run(bot_auth)

