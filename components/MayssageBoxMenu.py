import os
import time
import discord
from discord.ui import View, Button
from datetime import datetime

from MayssageReadMenu import MayssageReadMenu
from components.Mayssage import Mayssage

class MayssageBoxMenu(View):
    def __init__(self, embed, context):
        super().__init__()
        self.value = None
        self.embed = embed
        self.context = context
        
        self.mayssage_box_dir = "data/" + str(context.author.id)

        list_dir = os.listdir(self.mayssage_box_dir)
        list_dir.sort(reverse=True)
        self.mayssage_box_pages = list()

        for i in range(0, len(list_dir), 3):
            self.mayssage_box_pages.append(list_dir[i : i + 3])
        self.page_index = 0
        self.update_embed()
        self.update_button()
    
    def update_button(self):
        self.children[1].disabled = len(self.mayssage_box_pages[self.page_index]) < 2
        self.children[2].disabled = len(self.mayssage_box_pages[self.page_index]) < 3
        self.children[3].disabled = self.page_index == 0
        self.children[4].disabled = self.page_index + 1 == len(self.mayssage_box_pages)

    async def update_embed(self, interaction : discord.Interaction):
        self.embed.timestamp = datetime.fromtimestamp(time.time())
        self.embed.set_footer(text="MayaChen Mail")
        self.embed.set_author(name=self.context.author.display_name + "'s Mayssage box")
        self.embed.clear_fields()

        for mayssageid in self.mayssage_box_pages[self.page_index]:
            mayssage = Mayssage(self.mayssage_box_dir + "/" + mayssageid, "r")
            self.embed.add_field(name=mayssage.title, value=(mayssage.author_name + " \- <t:" + mayssage.time + ":R>").replace("\n", ""))

        orig_footer = self.embed.footer.text
        self.embed.set_footer(text= "Page " + str(self.page_index + 1) + "/" + str(len(self.mayssage_box_pages)) + "\n" + orig_footer)
        await interaction.response.edit_message(embed=self.embed, view=self)

    async def read_mayssage(self, interaction : discord.Interaction, mayssageid : int):
        mayssage_file_name = self.mayssage_box_dir + "/" + str(mayssageid)
        mayssage_to_read = Mayssage(mayssage_file_name)

        mayssage_pages = mayssage_to_read.split_content_in_pages()

        new_embed = discord.Embed(title=mayssage_to_read.title, description = mayssage_pages[0], timestamp=datetime.fromtimestamp(int(time)))
        new_embed.set_footer(text= "Page 1/" + str(len(mayssage_pages)) + "\nBy " + mayssage_to_read.author)

        # Switch to a MayssageReadMenu
        new_embed_menu = MayssageReadMenu(mayssage_to_read.title, mayssage_pages, mayssage_file_name, mayssage_to_read.author, datetime.fromtimestamp(int(time)))
        await interaction.response.edit_message(embed=new_embed,view=new_embed_menu)

    @discord.ui.button(style=discord.ButtonStyle.secondary,label="1")
    async def first(self, interaction : discord.Interaction, button : Button):
        await self.read_mayssage(interaction, self.mayssage_box_pages[self.page_index][0])

    @discord.ui.button(style=discord.ButtonStyle.secondary,label="2")
    async def second(self, interaction : discord.Interaction, button : Button):
        await self.read_mayssage(interaction, self.mayssage_box_pages[self.page_index][1])

    @discord.ui.button(style=discord.ButtonStyle.secondary,label="3")
    async def third(self, interaction : discord.Interaction, button : Button):
        await self.read_mayssage(interaction, self.mayssage_box_pages[self.page_index][2])


    @discord.ui.button(style=discord.ButtonStyle.blurple,label="Prev")
    async def prev(self, interaction : discord.Interaction, button : Button):
        self.page_index -= 1
        self.update_button()
        await self.update_embed(interaction)

    @discord.ui.button(style=discord.ButtonStyle.blurple,label="Next")
    async def next(self, interaction : discord.Interaction, button : Button):
        self.page_index += 1
        self.update_button()
        await self.update_embed(interaction)
