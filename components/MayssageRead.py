import discord
from discord.ui import View, Button
from datetime import datetime

from .DeleteButton import DeleteButton
from .Mayssage import Mayssage

class MayssageRead(View):
        def __init__(self, mayssage_file_name : str, mayssage: Mayssage):
            super().__init__()
            # self.value = None # idk if it's useful

            # Mayssage informations
            self.mayssage_file_name = mayssage_file_name
            self.title = mayssage.title
            self.author = mayssage.author_name
            self.time : float = mayssage.time

            # Pages of the Mayssage (>1000 Characters each)
            self.mayssage_pages = mayssage.split_content_in_pages()
            # Index for the current page
            self.page_index = 0

            self.embed = discord.Embed()

            # Set the embed and set the menu buttons
            self.set_embed()
            self.update_button()

        # Set the embed with the informations of the Mayssage
        def set_embed(self):
            self.embed = discord.Embed(title=self.title, description=self.mayssage_pages[self.page_index], timestamp=datetime.fromtimestamp(self.time))
            self.embed.clear_fields()
            self.embed.set_footer(text= "Page " + str(self.page_index + 1) + "/" + str(len(self.mayssage_pages)) + "\nBy " + self.author)

        # Depending of the page index, enable or disable the buttons
        def update_button(self):
            self.children[0].disabled = self.page_index == 0
            self.children[1].disabled = self.page_index + 1 == len(self.mayssage_pages)

        # Update the embed from the message on discord
        async def update_embed(self, interaction : discord.Interaction):
            self.set_embed()
            await interaction.response.edit_message(embed=self.embed, view=self)

        ######
        # Those buttons switch up the pages displaying other Mayssages
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
        ######

        # This button ask to delete the file of my computer
        # It sends another message with another button
        @discord.ui.button(style=discord.ButtonStyle.danger, label="Delete")
        async def delete(self, interaction : discord.Interaction, button : Button):
            view_del = View(timeout=60.0)
            view_del.add_item(DeleteButton(style=discord.ButtonStyle.danger,label="Delete from Maya's computer", mayssage_file_name = self.mayssage_file_name))
            await interaction.response.send_message(content="Are you sure you want to delete this Mayssage?", view=view_del)
