from manipulateText import manipulateText



def runTests():
        testAddNewLine()
        testParenthesesRemove()


def testAddNewLine():
        string =  "hello there. I don't know what your problem is, but i want it to stop!\n"
        text = manipulateText()

        newString = text.addNewLine(string)
        print(newString)
        assert(newString == "hello there.\nI don't know what your problem is,\nbut i want it to stop!\n")

def testParenthesesRemove():
        string = "howdy i don't (   r3242353 )want to be a hero ()\n"
        text = manipulateText()
        newString = text.removeParentheses(string)
        print(newString)
        assert(newString == "howdy i don't want to be a hero \n")
