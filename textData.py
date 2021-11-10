from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import pathlib
import os
from urllib.request import Request
# Class which extracts text from websites and puts them into text files.
class textData:

    def __init__(self, category, lines):
        self.category = category
        self.listFiles = []
        self.lines = lines
    def getData(self):
        # gets list of websites to examine.
        websites = self.getWebsiteList()
        print(websites)
        count = 0;
        newDirName = self.category
        newDir = pathlib.Path(os.getcwd(), newDirName)
        newDir.mkdir(parents=True,exist_ok=True)
        for website in websites:
            # retrieves html and puts it into a file.
            # urllib.request.urlretrieve(website,"C:\Users\dheff\PycharmProjects\LanguageFallOfRome\htmlFiles\file_" + str(count))
            try:
                req = Request(website, headers={'User-Agent': 'Mozilla/5.0'})
                html = urllib.request.urlopen(req)
            except Exception as e:
                print(str(e) + " website : " + website)
            parse = BeautifulSoup(html, "lxml")
            # unicode encoding to deal with weird characters.
           # for script in parse(["script", "style"]):
                #script.extract()
            try:
                filename = "file_ " + str(count) + ".txt"
                self.listFiles.append(filename)
                with open(newDir/filename, "w", encoding='utf-8') as file:
                    divider = "p"
                    #zero because beowulf is 0.
                    if count ==0:
                        divider = "div"
                    for data in parse.find_all(divider):
                        text = data.get_text()
                        file.writelines(text)
                count += 1

            except Exception as e:
                print(str(e))
        return self.listFiles


    # gets the list of websites from the websites file.
    def getWebsiteList(self):
        try:
            # list of websites from the Websites OE file.
            with open('Websites OE', 'r') as f:  # with closes the file automatically once it's done.
                # gets rid of newline characters gotten from file.
                list = [line.strip() for line in f.readlines()]
                # gets rid of last extra empty line in list.
                del list[-1]
                return list
        except Exception as e:
            print(str(e))




def main():
    language = "Old English"
    text = textData(language, False)
    fileList = text.getData()
    print(fileList)

if __name__== "__main__":
    main()
