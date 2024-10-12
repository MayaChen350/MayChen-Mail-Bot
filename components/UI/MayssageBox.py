import math
import os
import time
import discord
from discord.ui import View, Button
from datetime import datetime

from .MayssageReader import MayssageReader
from ..data.Mayssage import Mayssage

class MayssageBox(View):
    """UI displaying the Mayssages"""
    def __init__(self, context):
        super().__init__()
        # self.value = None # I saw this line in a yt video idk if it really changes smth
        self.embed = discord.Embed() 
        """Embed with the menu"""
        self.context = context
        """ctx"""
        
        self.mayssage_box_dir = "data/" + str(context.author.id)
        """(Calculated)\n
        The user directory with the Mayssages """

        # List the Mayssage files of the directory
        # from the most recent to the oldest
        list_dir = os.listdir(self.mayssage_box_dir)
        list_dir.sort(reverse=True)

        self.mayssage_box_pages : list[list[str]] = list()
        """Splitted list of Mayssages"""

        # Split all the Mayssage list
        # A "page" displays 3 Mayssages at once
        # They're displayed in reverse chronological order
        for i in range(0, len(list_dir), 3):
            self.mayssage_box_pages.append(list_dir[i : i + 3])
        self.page_index = 0

        # Set the embed and set the menu buttons
        self.set_embed()
        self.update_button()
    
    def set_embed(self):
        """Set the embed with displaying the Mayssages"""
        self.embed.timestamp = datetime.fromtimestamp(time.time()) # UNIX timestamp of the message
        self.embed.set_author(name=self.context.author.display_name + "'s Mayssage box") # Maysssage Box's owner
        
        # Clear the previous fields (if any)
        self.embed.clear_fields()
        # Display the Mayssage infos in the splitted (3 each pages) list of Mayssage
        for mayssageid in self.mayssage_box_pages[self.page_index]:
            mayssage = Mayssage(file = self.mayssage_box_dir + "/" + mayssageid) # Instantiate a Mayssage object by reading a Mayssage file
            self.embed.add_field(name=("( NEW ) " if not mayssage.read else "" ) + mayssage.title, value=(mayssage.author_name + " - <t:" + str(math.floor(mayssage.time)) + ":R>").replace("\n", ""))

        # Set the footer
        self.embed.set_footer(text= "Page " + str(self.page_index + 1) + "/" + str(len(self.mayssage_box_pages)) + "\nMayaChen Mail")

    def update_button(self):
        """Depending of the page index, enable or disable the buttons"""
        self.children[1].disabled = len(self.mayssage_box_pages[self.page_index]) < 2
        self.children[2].disabled = len(self.mayssage_box_pages[self.page_index]) < 3
        self.children[3].disabled = self.page_index == 0
        self.children[4].disabled = self.page_index + 1 == len(self.mayssage_box_pages)

    async def update_embed(self, interaction : discord.Interaction):
        """Update the embed from the message on discord"""
        self.set_embed()
        await interaction.response.edit_message(embed=self.embed, view=self)

    async def read_mayssage(self, interaction : discord.Interaction, mayssageid : int):
        """Read a message from a file (Also switch to display a MayssageReadMenu instance)"""

        # Instantiate a Mayssage object by reading a Mayssage file
        mayssage_file_name = self.mayssage_box_dir + "/" + str(mayssageid)
        mayssage_to_read = Mayssage(mayssage_file_name)

        # Mark the Mayssage as "read" in its file
        if mayssage_to_read.read == False:
            mayssage_to_read.read = True
        
        self.set_embed()

        # Switch to a MayssageReadMenu
        new_ui = MayssageReader(mayssage_file_name, mayssage_to_read, self)
        # Update the embed from the message on discord
        await interaction.response.edit_message(embed=new_ui.embed,view=new_ui)

    ######
    # Those buttons let you choose a Mayssage in the displayed ones based on their order
    @discord.ui.button(style=discord.ButtonStyle.secondary,label="1")
    async def first(self, interaction : discord.Interaction, button : Button):
        await self.read_mayssage(interaction, self.mayssage_box_pages[self.page_index][0])

    @discord.ui.button(style=discord.ButtonStyle.secondary,label="2")
    async def second(self, interaction : discord.Interaction, button : Button):
        await self.read_mayssage(interaction, self.mayssage_box_pages[self.page_index][1])

    @discord.ui.button(style=discord.ButtonStyle.secondary,label="3")
    async def third(self, interaction : discord.Interaction, button : Button):
        await self.read_mayssage(interaction, self.mayssage_box_pages[self.page_index][2])
    ######

    ######
    # Those buttons switch up the pages displaying other Mayssages
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
    ######