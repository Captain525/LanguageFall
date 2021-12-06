# LanguageFall

FILE SUMMARIES: 

textData.py - gets data from list of websites. Puts it into an array then returns the list of file names. copies the html
files into files in the respective language folders. Also does some cutting and editing of thse files. 
Then, converts it into a csv which other functions can read to do the machine learning. 

makeCSV.py - makes the csv from the different folders of data. This gets the data ready for ML. 
manipulateText - cuts things out of text files to make it fit for use. Does this automatically. Called from textData. 

machineLearningLanguages - does the main machine learning. Uses a deep sequential neural network and splits the data from 
the csv into training, validation and test data, trains the training data on the model, then tests it to see how it works. 
