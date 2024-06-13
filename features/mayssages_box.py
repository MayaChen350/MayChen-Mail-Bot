import discord
from discord.ext import commands
from discord.ui import View, Button
import os

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
async def check_mayssages(ctx, mayssageid : int):
    mayssage_file = open("data/" + str(ctx.author.id) + "/" + str(mayssageid), "r")
    title = mayssage_file.readline()
    mayssage_content = mayssage_file.read()
    mayssage_file.close()

    mayssage_length = len(mayssage_content)
    mayssage_pages = list()
    mayssage_index = 0

    while mayssage_length > 1000:
        mayssage_pages.append(mayssage_content[mayssage_index:mayssage_index + 1000])
        mayssage_index += 1000
        mayssage_length -= 1000

    mayssage_pages.append(mayssage_content[mayssage_index:-1])

    embed = discord.Embed()
    embed.add_field(name=title, value=mayssage_pages[0])
    embed.set_footer(text= "1/" + str(len(mayssage_pages)))
    embed_menu = Embed_Menu(title, mayssage_pages)
    await ctx.send(embed=embed,view=embed_menu)
