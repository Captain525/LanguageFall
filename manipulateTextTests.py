from manipulateText import manipulateText



def runTests():
        pass


def testAddNewLine():
        string =  "hello there. I don't know what your problem is, but i want it to stop!\n"
        text = manipulateText()

        newString = text.addNewLine(string)
        print(newString)
        assert(newString == "hello there.\nI don't know what your problem is,\nbut i want it to stop!\n")