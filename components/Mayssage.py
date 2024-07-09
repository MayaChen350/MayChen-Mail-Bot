import math
import time

class Mayssage:
    def __init__(self, title : str, messages : list, author_name : str, time : float):
        self.title = title
        self.author_name = author_name
        self.time = time
        self.mayssage_content = ""
        for msg in messages:
            self.mayssage_content += msg + "\n\n"

    def __init__(self, file):
        mayssage_file = open(file, "r")

        self.title = mayssage_file.readline()
        self.author_name = mayssage_file.readline()
        self.time = mayssage_file.readline()
        self.mayssage_content = mayssage_file.read()

        mayssage_file.close()

    def split_content_in_pages(self) -> list:
        mayssage_length = len(self.mayssage_content)
        mayssage_pages = list()
        mayssage_index = 0

        while mayssage_length > 1000:
            mayssage_pages.append(self.mayssage_content[mayssage_index:mayssage_index + 1000])
            mayssage_index += 1000
            mayssage_length -= 1000

        mayssage_pages.append(self.mayssage_content[mayssage_index:-1])
        return mayssage_pages

    def __str__(self) -> str:
        return self.title + "\n" + self.author_name + "\n" + str(math.floor(time.time())) + "\n"  + self.mayssage_content