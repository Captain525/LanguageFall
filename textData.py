from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import pathlib
import os
from urllib.request import Request
# Class which extracts text from websites and puts them into text files.
import manipulateTextTests
import makeCSV
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
        count = 0
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
                #accidentally put a space after _.
                filename = "file_ " + str(count) + ".txt"
                self.listFiles.append(filename)
                with open(newDir/filename, "x", encoding='utf-8') as file:
                    divider = "p"
                    #checks for the texts which don't work the other way.
                    if (self.category == "Old English" and count ==0) or (self.category =="Old French" and count<24):
                        divider = "div"
                    for data in parse.find_all(divider):
                        text = data.get_text()
                        file.writelines(text)
                count += 1
            #if file already exists, don't overwrite .
            except FileExistsError:
                print("file " + filename + " exists\n");
                count+=1;
                continue;
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

            directory = pathlib.Path(os.getcwd(), self.category)
            with open(directory/(self.category + " list"), "x", encoding='utf-8') as file:
                for fileName in list:
                    #write the names to this new file.
                    var = "\n" + fileName
                    file.writelines(var)
        except FileExistsError:
            print("Didn't write new list\n");
        except Exception as e:
            print(str(e))


    def getListFromFile(self):
        list =[];
        try:
            subDirectory = os.getcwd() + "/" + self.category
            with open(subDirectory + "/" + (self.category + " list"), "r", encoding='utf-8') as file:
                list = [line.strip() for line in file.readlines()]
        except Exception as e:
            print(str(e))
            return None

        return list
#does the creation of the text files with the sources and writes the list of websites to a file.
def initialize_files(list):
    listOfFileLists = []
    for text in list:
        specList = text.getData()
        listOfFileLists.append(specList)
        text.writeListToFile(specList)
def remove(list, category):
    man = manipulateText()
    subDirectory = os.getcwd() + "/" + category
    file = list[4]
    man.remove(subDirectory + "/" + file, -1)
    print("done " + file + "\n")
def main():
    text = textData("Old English", False)
    text2 = textData("Old French", True)
    text3 = textData("Old Latin", False)
    list = [text,text2,text3]
    fileList = text.getListFromFile();
    #print(fileList)
    frenchList = text2.getListFromFile()
    #frenchList = text2.getData()
    #print(frenchList)
    latinList = text3.getListFromFile()
    #print(latinList);
    #remove(frenchList, "Old French")
    #remove(fileList, "Old English")
    count = manipulateText()
    #test = manipulateTextTests.runTests()
    subDirectory = os.getcwd() + "/" + "Old English"
   # for i in range (24,28):
        #count.remove(subDirectory + "/" + frenchList[i], 2)
    #file = subDirectory + "/" + frenchList[1]
    #count.remove(file, 3)
    #count.removeNumbers(subDirectory + "/" + frenchList[16])
    #print(count.countWords(fileList, os.getcwd() + "/Old English"))
    #print(count.countWords(frenchList, os.getcwd() + "/Old French"))
    #print(count.countWords(frenchList, os.getcwd() + "/Old Latin"))
    for i in range(0, 25):
        count.remove(subDirectory +"/"+ fileList[i],6)
        if i ==1:
            count.remove(subDirectory + "/" +fileList[i], 4)
        count.remove(subDirectory + "/" + fileList[i], 5)

    cv = makeCSV
    list = []
    list.append(cv.makeTuple(fileList, "Old English"))
    list.append(cv.makeTuple(frenchList, "Old French"))
    list.append(cv.makeTuple(latinList, "Old Latin"))
    csv = cv.makeCSV(list)
if __name__== "__main__":
    main()
