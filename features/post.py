import discord
from discord.ext import commands
from discord.ui import View, Button
import time

@commands.hybrid_command()
async def write(ctx):
    await ctx.send(f"Welcome to MayChen Mail! Write all your messages you want to send to your destinataire, and use the `send` command to send all your messages. (The limit of messages is 200)")

class Embed_Menu(View):
        def __init__(self, title, messages : list):
            super().__init__()
            self.value = None
            self.title = title
            self.messages = messages
            self.update_button()

        page_index = 0
        def update_button(self):
            self.children[0].disabled = self.page_index == 0
            self.children[1].disabled = self.page_index + 1 == len(self.messages)

        async def update_embed(self, interaction : discord.Interaction):
            embed = discord.Embed()
            embed.clear_fields()
            embed.add_field(name=self.title, value=self.messages[self.page_index])
            embed.set_footer(text= str(self.page_index + 1) + "/" + str(len(self.messages))) 
            await interaction.response.edit_message(embed=embed, view=self)


        @discord.ui.button(style=discord.ButtonStyle.primary,label="Prev")
        async def prev(self, interaction : discord.Interaction, button : Button):
            self.page_index -= 1
            self.update_button()
            await self.update_embed(interaction)

        @discord.ui.button(style=discord.ButtonStyle.primary,label="Next")
        async def next(self, interaction : discord.Interaction, button : Button):
            self.page_index += 1
            self.update_button()
            await self.update_embed(interaction)

@commands.hybrid_command()
async def send(ctx, receiverid : int, title : str):
    messages_to_send = ""
    messages = list()
    async for message in ctx.channel.history(limit=5):
        if message.author.id == 1250539685567008880:
            break
        elif message.author == ctx.author:
            messages.append(message.content)

    messages.reverse()
    for msg in messages:
        messages_to_send += msg + "\n"

    message_length = len(messages_to_send)
    messages.clear()
    message_index = 0

    while message_length > 1000:
        messages.append(messages_to_send[message_index:message_index + 1000])
        message_index += 1000
        message_length -= 1000

    messages.append(messages_to_send[message_index:-1])

    await ctx.send("Your message has been sent! They can read it with the `check_mayssages` command! Thank you for using MayChen Mail.")

    embed = discord.Embed()

#    embed_menu.add_item(Button(style=discord.ButtonStyle.primary, label="smth the sequel"))
    embed.add_field(name=title, value=messages[0])
    embed_menu = Embed_Menu(title, messages)
    await ctx.send(embed=embed,view=embed_menu)
