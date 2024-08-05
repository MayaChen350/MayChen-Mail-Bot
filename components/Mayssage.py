import math
import time

from datetime import datetime

class Mayssage:
    def __init__(self, file : str = "", title : str = "", messages : list = list, author_name : str = "", time : float = 0):
        # If the file argument is included and not null, initialized the object from the lines in the file
        if file != "":
            mayssage_file = open(file, "r")

            self.read = mayssage_file.readline().strip("\n") == 'R'
            self.title = mayssage_file.readline().strip("\n")
            self.author_name = mayssage_file.readline().strip("\n")
            self.time = float(mayssage_file.readline().strip("\n"))

            self.mayssage_content = mayssage_file.read()

            mayssage_file.close()
        # Otherwise use the included parameters
        else:
            self.read = False
            self.title = title
            self.author_name = author_name
            self.time = time

            self.mayssage_content = ""
            for msg in messages:
                self.mayssage_content += msg + "\n\n"
            
    # Split the content in strings of less than 1000
    # Return a list of them
    def split_content_in_pages(self) -> list[str]:
        mayssage_length = len(self.mayssage_content)
        mayssage_pages : list[str] = []
        mayssage_index = 0

        # Split the Mayssage into pages of less than 1000 characters
        while mayssage_length > 1000:
            mayssage_pages.append(self.mayssage_content[mayssage_index:mayssage_index + 1000])
            mayssage_index += 1000
            mayssage_length -= 1000

        mayssage_pages.append(self.mayssage_content[mayssage_index:-1])

        return mayssage_pages

    # toString override
    def __str__(self) -> str:
        return ("R\n" if self.read else "\n") + self.title + "\n" + self.author_name + "\n" + str(math.floor(self.time)) + "\n"  + self.mayssage_content