from discord.ext import commands
import os
import math
import time # Exact date and time of the mayssage is stored in UNIX format

from components.Mayssage import Mayssage

# When this command is used, all messages of the user who did the command starting to the first message the user sent
# after the last message the bot sent
# will be saved in a mayssage_file in the local directory of the receiver (with for name the receiver id)
@commands.hybrid_command()
async def send(ctx, receiverid : str , title : str):
    if not receiverid.isdigit():
        raise Exception("The receiverid must have digits only. (Try copying the User ID of the person you want to send the mayssage to.)")

    mayssage_directory = "data/" + receiverid + "/" # the local directory of the messages of the receiver
    os.makedirs(name=mayssage_directory, exist_ok=True) # create the directory if it doesn't exist

    # Determine the name (id) of the mayssage file (a text file)
    if os.listdir(mayssage_directory) == []:
       file_name = "1"
    else:
        file_name = str(int(max(os.listdir(mayssage_directory))) + 1)


    messages = list() # list of the discord messages to be saved in a single mayssage
    
    # Check for every discord messages from the user who did the command from their first after the last message the bot sent
    # From the most recent to the oldest (reversed chronological order)
    # And add them to the list made above
    async for message in ctx.channel.history(limit=200):
        if message.author.id == 1250539685567008880: # Bot ID
            break # Stop saving
        elif message.author == ctx.author: # Sender of the command
            messages.append(message.content)

    messages.reverse() # Reverse the order of the list to have the oldest messages first (chronological order)

    # Create a Mayssage instance with the title of the mayssage specified when done the command,
    # the above list of messages
    # and the current time and day (in UNIX format)
    mayssage = Mayssage("", title, messages, ctx.author.display_name, math.floor(time.time()))

    # Write the mayssage in a text file in the good directory
    mayssage_file = open(mayssage_directory + "/" + file_name, "w")
    mayssage_file.write(str(mayssage))
    mayssage_file.close()

    await ctx.send("Your mayssage has been sent! They can read it with the `check_mayssages` command! Thank you for using MayChen Mail.")
    print(str(ctx.author.id) + " sent a message to " + receiverid + "!") # personal logs hehe
