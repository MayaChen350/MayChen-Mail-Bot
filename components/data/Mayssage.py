import math


class Mayssage:
    """Instance of a Mayssage"""
    def __init__(self, file : str = "", title : str = "", messages : list = list, author_name : str = "", time : float = 0):
        self.file_name = file
        # If the file argument is included and not null, initialized the object from the lines in the file
        if self.file_name != "":
            mayssage_file = open(self.file_name, "r")

            self._read = mayssage_file.readline().strip("\n") == 'R'
            self.title = mayssage_file.readline().strip("\n")
            self.author_name = mayssage_file.readline().strip("\n")
            self.time = float(mayssage_file.readline().strip("\n"))

            self.mayssage_content = mayssage_file.read()

            mayssage_file.close()
        # Otherwise use the included parameters
        else:
            self._read = False
            self.title = title
            self.author_name = author_name
            self.time = time

            self.mayssage_content = "\n\n".join(messages)

    def get_read(self):
        return self._read
    
    def set_read(self, value: bool):
        if (value == True):
            self._read = False
            mayssage_file = open(self.file_name, "w")
            mayssage_file.write(str(self))
            mayssage_file.close()
        else:
            raise ValueError("The read value can only be set to True.")

    read = property(fget=get_read,fset=set_read)

            
    def split_content_in_pages(self) -> list[str]:
        """Split the content in strings of less than 1000\n
        Return a list of them"""

        mayssage_length: int = len(self.mayssage_content)
        mayssage_pages : list[str] = []
        mayssage_index: int = 0

        wordLength : int = 0

        def offset(): 
            return 1000 - wordLength

        while mayssage_length - mayssage_index > 1000: 
            if self.mayssage_content[mayssage_index + offset()] == ' ': # If it finds a space after 1000 characters after the current index
                mayssage_pages.append(self.mayssage_content[mayssage_index:mayssage_index + offset()]) # Add the characters in a page
                mayssage_index += offset() # Increase the index
                wordLength = 0 # Reset the recorded length of the current word
            elif wordLength == 1000: # If the recorded length of the word without a space is 1000
                mayssage_pages.append(self.mayssage_content[mayssage_index:mayssage_index + 1000]) # append the first 1000 characters of the more than 1k chars word
                mayssage_index += 1000 # Increment the index at the end of the 1000 characters word
                wordLength = 0
            else: # If it didn't find a space nor the word was 1000+ characters long
                wordLength += 1 # Increment the length of the current word

        mayssage_pages.append(self.mayssage_content[mayssage_index:mayssage_length])

        return mayssage_pages

    # toString override
    def __str__(self) -> str:
        return ("R\n" if self._read else "\n") + self.title + "\n" + self.author_name + "\n" + str(math.floor(self.time)) + "\n"  + self.mayssage_content