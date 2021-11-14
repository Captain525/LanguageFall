from manipulateText import manipulateText



def runTests():
        testAddNewLine()
        testParenthesesRemove()
        testBracketsRemove()
        testRemoveBlankLine()

def testAddNewLine():
        string =  "hello there. I don't know what your problem is, but i want it to stop!\n"
        text = manipulateText()
        newString = text.addNewLine(string)
        assert(newString == "hello there.\nI don't know what your problem is,\nbut i want it to stop!\n")

def testParenthesesRemove():
        string = "howdy i don't (   r3242353 )want to be a hero ()\n"
        text = manipulateText()
        newString = text.removeParentheses(string)
        assert(newString == "howdy i don't want to be a hero \n")
def testBracketsRemove():
        string = "howdy i don't [] how [ 54]three"
        text = manipulateText()
        newString = text.removeBrackets(string)
        assert(newString=="howdy i don't  how three")

def testRemoveBlankLine():
        string = "      \n Hi hello how are you"
        text= manipulateText()
        newString = text.removeBlankLine(string)
        //print(newString)
        assert(newString == "Hi hello how are you")