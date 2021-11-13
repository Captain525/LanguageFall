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
             #print("file :" + file + " num sentences: " + str(countSentences) +", num chars: " + str(countCharacters) +", num lines: " + str(countLines) + ", numWords = " + str(countWords) +"\n")
             return countWords

    # removes numbers from a file, changing the file itself.
    # used to format files pre putting them into csvs.
    def remove(self, file, choice):
        try:
            with open(file, "r", encoding="utf-8") as f:
                print(file)
                list = f.readlines()
            with open(file, "w", encoding="utf-8") as f:
                print(len(list))
                for i in range(0, len(list)):
                    list[i] = self.chooseFunction(list[i], choice)
                    f.write(list[i])
        except Exception as e:
            print(str(e))
    #choose which helper function to call, ie, what you want to remove.
    def chooseFunction(self, string, choice):
        if (choice == 0):
            var_function = self.deleteNums(string)
        elif choice == 1:
            var_function = self.removeBrackets(string)
        else:
            print("Not a valid choice\n")
        return var_function
    # helper method to removeNumbers, it cuts out all the nums from a string and returns it.
    def deleteNums(self, string):
        result = ''.join([i for i in string if not i.isdigit()])
        return result

    #removes the brackets from a given string.
    def removeBrackets(self, string):
        result = ''.join([ i for i in string if not (i=='[' or i==']')])
        return result