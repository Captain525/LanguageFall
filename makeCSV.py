import csv
import pandas as pd
import os

#want to make a csv with 2 columns. First column is text, second is language.
def makeCSV(listOfTuples):
    headers = ["text", "language"]
    listLines = []
    for tuple in listOfTuples:
        category = tuple[0]
        listOfFiles = tuple[1]
        for file in listOfFiles:
            #list of tuples of text line and category, want to concatenate these for all of them.
            listLines += getListLinesFile(getPath(category, file), category)

    print(listLines)
    data = pd.DataFrame(listLines, columns=headers)
    return data.to_csv('languageData.csv', index=False)

def getListLinesFile(file, category):
    listOfLineTuples = []
    try:
        with open(file, "r") as f:
            line= f.readline()
            while line:
                element = [line, category]
                listOfLineTuples.append(element)
                line =f.readline()
    except Exception as e:
        print(str(e))
    return listOfLineTuples



def makeTuple(category, listFiles):
    pair= (category, listFiles)
    return pair



#returns the path to a given file in a give category.
def getPath(category, file):
    subDirectory = os.getcwd() + "/" + category
    path = subDirectory + "/" + file
    return path
