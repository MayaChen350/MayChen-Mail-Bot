import discord
from discord.ext import commands
import os

@commands.hybrid_command()
async def send_second_version(ctx, receiverid : int, title : str):
    mayssage_directory = "data/" + str(receiverid) + "/" + str(ctx.author.id)
    os.makedirs(name=mayssage_directory, exist_ok=True)
    if not os.path.isfile(mayssage_directory + "/1"):
        open(mayssage_directory + "/1", "x")
    file_name = str(int(max(os.listdir(mayssage_directory))) + 1)
    print(file_name)

    messages_to_send = ""
    messages = list()
    async for message in ctx.channel.history(limit=200):
        if message.author.id == 1250539685567008880:
            break
        elif message.author == ctx.author:
            messages.append(message.content)

    messages.reverse()
    for msg in messages:
        messages_to_send += msg + "\n"

    mayssage_file = open(mayssage_directory + "/" + file_name, "w")
    mayssage_file.write(title + "\n" + messages_to_send)
    mayssage_file.close()

    await ctx.send("Your message has been sent! They can read it with the `check_mayssages` command! Thank you for using MayChen Mail.")
