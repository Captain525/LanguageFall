from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
from urllib.request import Request
# Class which extracts text from websites and puts them into text files.
class textData:

    def __init__(self, category):
        self.category = category
        self.listFiles = []
    def getData(self):
        # gets list of websites to examine.
        websites = self.getWebsiteList()
        print(websites)
        count = 0;
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
            try:
                filename = "file_ " + str(count) + ".txt"
                self.listFiles.append(filename)
                with open(filename, "w", encoding='utf-8') as file:
                    for data in parse.find_all("p"):
                        text = data.get_text()
                        file.writelines(text)
                count += 1

            except Exception as e:
                print(str(e))
        return self.listFiles


    # gets the list of websites from the websites file.
    def getWebsiteList(self):
        try:
            # list of websites from the Websites file.
            with open('Websites', 'r') as f:  # with closes the file automatically once it's done.
                # gets rid of newline characters gotten from file.
                list = [line.strip() for line in f.readlines()]
                # gets rid of last extra empty line in list.
                del list[-1]
                return list
        except Exception as e:
            print(str(e))




def main():
    language = "Old English"
    text = textData(language)
    fileList = text.getData()
    print(fileList)

if __name__== "__main__":
    main()
