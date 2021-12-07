from manipulateText import manipulateText
"""
This file runs tests to test the functions which edit the text to make sure they work properly. 
"""
def main():
        runTests()


def runTests():
        testAddNewLine()
        testParenthesesRemove()
        testBracketsRemove()
        testRemoveBlankLine()
        testRemoveDividers()
        testRemoveQuotes()

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
        #print(newString)
        assert(newString == "Hi hello how are you")
def testRemoveDividers():
        string = "c teh thing is that what i want is b what you can do to stop me."
        text = manipulateText();
        newString = text.removeDividers(string, 'c', 'b')
        print(newString)
        assert(newString == " what you can do to stop me.")

def testRemoveQuotes():
        string = "'hello there'"
        string2 = "hello" + "\"" +" hodwy" + "\""
        text=manipulateText()
        newString2 = text.removeChars(string2, {"\""})

        assert(newString2 == "hello hodwy")
        newString = text.removeChars(string, {"\'"})
        assert(newString == "hello there")
if __name__== "__main__":
    main()
