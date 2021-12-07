import csv
import pandas as pd
import os
"""
This file makes the csv(sheet with data on it), by going through the folders for each language, copying the text by 
line, and pairing that with the line's classification, then doing this for ALL the specified files. This then puts these
pairs into the languageData.csv
"""
#want to make a csv with 2 columns. First column is text, second is language.
def makeCSV(listOfTuples):
    headers = ["text", "language"]
    listLines = []
    for tuple in listOfTuples:
        listOfFiles = tuple[0]
        category = tuple[1]
        for file in listOfFiles:
            print(file + "\n")
            print(getPath(category, file))
            #list of tuples of text line and category, want to concatenate these for all of them.
            listLines += getListLinesFile(getPath(category, file), category)
           # print(listLines)
            print("\n")

    #print(listLines)
    data = pd.DataFrame(listLines, columns=headers)
    nan_value = float("NaN")
    data.replace('', nan_value, inplace=True)
    data.dropna(subset=["text"], inplace=True)
    return data.to_csv('languageData.csv', index=False)

#gets the list of tuples containing each line, combined with its classification.
def getListLinesFile(file, category):
    listOfLineTuples = []
    try:
        with open(file, "r",encoding='utf-8') as f:
            list = f.readlines()
            for line in list:
                newline = line.strip()
                print(newline)
                element = [newline, category]
                print(element)
                listOfLineTuples.append(element)

    except Exception as e:
        print(str(e))
    return listOfLineTuples


#makes pairs of (category, listFiles)
def makeTuple(category, listFiles):
    pair= (category, listFiles)
    return pair



#returns the path to a given file in a given category.
def getPath(category, file):
    subDirectory = os.getcwd() + "/" + category
    path = subDirectory + "/" + file
    return path
