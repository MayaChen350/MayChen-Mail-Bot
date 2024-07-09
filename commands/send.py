from discord.ext import commands
import os
import time
import math

from components.Mayssage import Mayssage

@commands.hybrid_command()
async def send(ctx, receiverid : str , title : str):
    if not receiverid.isdigit():
        raise Exception("The receiverid must have digits only. (Try copying the User ID of the person you want to send the mayssage to.)")

    mayssage_directory = "data/" + receiverid + "/"
    os.makedirs(name=mayssage_directory, exist_ok=True)
    if os.listdir(mayssage_directory) == []:
       file_name = "1"
    else:
        file_name = str(int(max(os.listdir(mayssage_directory))) + 1)

    mayssages = list()
    async for message in ctx.channel.history(limit=200):
        if message.author.id == 1250539685567008880:
            break
        elif message.author == ctx.author:
            mayssages.append(message.content)

    mayssages.reverse()
    mayssage = Mayssage(title, mayssages, ctx.author.display_name, math.floor(time.time()))

    mayssage_file = open(mayssage_directory + "/" + file_name, "w")
    mayssage_file.write(mayssage)
    mayssage_file.close()

    await ctx.send("Your mayssage has been sent! They can read it with the `check_mayssages` command! Thank you for using MayChen Mail.")
    print(str(ctx.author.id) + " sent a message to " + receiverid + "!")
