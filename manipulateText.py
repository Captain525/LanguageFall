class manipulateText():
    def __init__(self):
        pass

    def countWords(self, listFiles,folderPath):
        sum = 0
        for file in listFiles:
            num = self.count(folderPath + "/" + file)
            sum += num

        return sum
    def count(self, file):
         with open(file, "r", encoding="utf-8") as f:
             countWords = 0
             countSentences = 0
             countCharacters = 0
             countLines = 0
             for line in f:
                 countSentences+=line.count(".")
                 #gets length in chars
                 countCharacters+=len(line)
                 line = line.split()
                 #length in words after split.
                 countWords += len(line)
                 countLines+=1
             print("file :" + file + " num sentences: " + str(countSentences) +", num chars: " + str(countCharacters) +", num lines: " + str(countLines) + ", numWords = " + str(countWords) +"\n")
             return countWords

