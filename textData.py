from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import pathlib
import os
from urllib.request import Request
# Class which extracts text from websites and puts them into text files.
from manipulateText import manipulateText


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
                #sometimes error bc website doesn't respond in time.
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
                    #checks for the texts which don't work the other way.
                    if (self.category == "Old English" and count ==0) or (self.category =="Old French" and count<24):
                        divider = "div"
                    for data in parse.find_all(divider):
                        text = data.get_text()
                        file.writelines(text)
                count += 1

            except Exception as e:
                print(str(e))
                continue
        return self.listFiles


    # gets the list of websites from the websites file.
    def getWebsiteList(self):
        try:
            # list of websites from the Websites Old English file.
            with open('Websites ' + self.category, 'r') as f:  # with closes the file automatically once it's done.
                # gets rid of newline characters gotten from file.
                list = [line.strip() for line in f.readlines()]
                # gets rid of last extra empty line in list.
                del list[-1]
                return list
        except Exception as e:
            print(str(e))

    def writeListToFile(self, list):
        try:
            subDirectory = os.getcwd() + "/" + self.category
            with open(subDirectory/(self.category + " list"), "x", encoding='utf-8') as file:
                for fileName in list:
                    #write the names to this new file.
                    file.writelines(fileName)
        except Exception as e:
            print(str(e))


    def getListFromFile(self):
        try:
            subDirectory = os.getcwd() + "/" + self.category
            with open(subDirectory/(self.category + " list"), "r", encoding='utf-8') as file:




def main():
    text = textData("Old English", False)
    text2 = textData("Old French", True)
    text3 = textData("Old Latin", False)
    fileList = text.getData()
    frenchList = text2.getData()
    latinList = text3.getData();
    text.writeListToFile(fileList)
    text2.writeListToFile(frenchList)
    text3.writeListToFile(latinList)
    print(fileList)
    print(frenchList)
    print(latinList);

    count = manipulateText()
    print(count.countWords(fileList, os.getcwd() + "/Old English"))
    print(count.countWords(frenchList, os.getcwd() + "/Old French"))
    print(count.countWords(frenchList, os.getcwd() + "/Old Latin"))
if __name__== "__main__":
    main()
