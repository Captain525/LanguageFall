import pandas as pd
import numpy as np
import re
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils
import matplotlib.pyplot as plt
import seaborn as sea

from keras_visualizer import visualizer
import scikeras
from scikeras.wrappers import KerasClassifier, KerasRegressor


from sklearn.feature_extraction.text import CountVectorizer
#import warningswarnings.simplefilter("ignore")
from sklearn.inspection import permutation_importance
from sklearn.metrics import confusion_matrix,accuracy_score
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

"""
Put the data into the right form, make and train the neural network, test it. 
"""
class machineLearningLanguages():
    def __init__(self, listLangs):
        self.languageList = listLangs
        self.trainingPercent = .7
        self.validationPercent = .2
        self.testPercent = .1
        self.train =pd.DataFrame(columns = ['text', 'language'])
        self.validation = pd.DataFrame(columns = ['text', 'language'])
        self.test = pd.DataFrame(columns = ['text', 'language'])
        self.trainFM = None
        self.validFM = None
        self.testFM = None
        self.modelTrained = None
        self.encoder= None
        self.trig = None



    #make the data set.
    def makeDataSet(self):
        #header = 0 to show to skip the first line bc those are names of columns.
        data = pd.read_csv('languageData.csv', header=0,skip_blank_lines=True, encoding='utf-8')
        #does this matter?
        conditionalLength = [True if 10<=len(s) else False for s in data['text']]
        data = data[conditionalLength]
        print(data)

        dataRandom = pd.DataFrame(columns = ['text', 'language'])
        #print(len(self.languageList))
        for lang in self.languageList:
            langSubset = data[data['language']==lang]
            print("Num lines for: " + lang + " is " + str(len(langSubset)) )
            #not using all the data.
            dataSubset = langSubset.sample(5000, random_state=120)
            dataRandom = dataRandom.append(dataSubset)
        dataRandom = dataRandom.sample(frac = 1)
        trainCount = int(self.trainingPercent*len(dataRandom))
        validationCount = int(self.validationPercent*len(dataRandom)) + trainCount

        self.train= dataRandom[0:trainCount]
        self.validation = dataRandom[trainCount:validationCount]
        self.test = dataRandom[validationCount:]

#character 3 trigram method.
    def makeTrigrams(self,data, amount):
        """
        Returns a set of the most common trigrams.
        Data - training set we wish to make the trigrams out of.

        """
        features = {}
        featureSet = set()

        for language in self.languageList:
            #get only the rows with language == language
            corpus = data['text'][data['language']== language]
            self.getTop10ForEach(corpus, amount, language)
            trigramList = self.getTrigramsLanguage(corpus, amount)
            #add trigrams to dictionary.
            features[language] = trigramList
            featureSet.update(trigramList)
        #print all trigrams to the file.
        with open("TrigramListFull", "w", encoding='utf-8') as file:
            file.write("Total number of trigrams: " + str(len(featureSet)) + "\n")
            for element in featureSet:
                file.write(element + "\n")


        return featureSet


    def getTrigramsLanguage(self,corpus, amount):
        """
        Gets the most common amount trigrams for the data set of the given language.
        returns the list of these most common trigrams.
        corpus - collection of text from a given language.
        amount - how many unique ngrams to produce.

        countVectorizer - convert collection of text into matrix of token counts.
        """

        #analyzer - character ngram or word ngram? Ngram range - what range of length. max features - how many unique ngrams to choose.
        vectorizer = CountVectorizer(analyzer='char', ngram_range=(3,3), max_features=amount)
        #transform the corpus into an array of samples by features, each row being one sample.
        X = vectorizer.fit_transform(corpus)
        #gets the list of those amount most common trigrams.
        featureNames = vectorizer.get_feature_names_out()

        #print(featureNames)
        return featureNames
    def getTop10ForEach(self,corpus,amount, language):
        vectorizer = CountVectorizer(analyzer='char', ngram_range=(3,3), max_features=10)
        X=vectorizer.fit_transform(corpus)
        featureNames =vectorizer.get_feature_names_out()
        with open("TrigramList", "a", encoding='utf-8') as file:
            file.write("language: " + language + "\n")
            for i in range(0, len(featureNames)):
                file.write(featureNames[i])
                file.write("\n")


    """
    Scales the feature matrix using minMax scaling. 
    """
    def scaleFM(self, featureMatrix, min, max):
        #to show its the training set
        """
        if(min is None and max is None):
            min = featureMatrix.min(axis=0)
            print(min)
            print('next')
            max = featureMatrix.max(axis=0)
            print(max)
        #scale the values in the matrix by subtracting the minimum, then dividing by range.
        scaledFeature = (featureMatrix - min)/(max - min)
        print(scaledFeature)
        return scaledFeature

        scaler = MinMaxScaler()
        scaledData = scaler.fit_transform(featureMatrix)

        scaledData = pd.DataFrame(scaledData)
        return scaledData
        """
        arr = featureMatrix.to_numpy()
        if min is None and max is None:
            min = np.amin(arr, axis=None)
            max = np.amax(arr,axis=None)
            #print (min)
            #print(max)
        scaledFeature = (featureMatrix - min) / (max - min)
        #add this? xfinal = scaledFeature *(maxChosen -minChosen) + minChosen - this is range you want them to go to, don't have to do if 0 to 1.
        return scaledFeature

    """
    Given some data and a vectorizer, it makes a feature matrix of the given 
    data. The vectorizer has already been set up with the vocab list, so all it does 
    is just create the feature matrix, turn it into a dataframe, scale the values, 
    then add the languages back. 
    """
    def makeFeatureMatrix(self, data, vectorizer,featureNames, min, max):
        corpus = data['text']
        X = vectorizer.fit_transform(corpus)

        #not sure if only do this once, or many times?
        if featureNames is None:
            featureNames= vectorizer.get_feature_names_out()
        # get the feature matrix as a dataframe.
        dataFeat = pd.DataFrame(data=X.toarray(), columns=featureNames)
        dataScaled = self.scaleFM(dataFeat, min, max)
        #add the result variable back
        dataScaled['language'] = list(data['language'])
        return dataScaled
    """
    Makes the 3 feature matrices, one for training, one for validation, 
    and one for testing. 
    """
    def makeAllFeatureMatrices(self, featureSet):

        vocabList = self.getVocabList(featureSet)
        vectorizer = CountVectorizer(analyzer='char', ngram_range=(3, 3), vocabulary=vocabList)
        self.trainFM = self.makeFeatureMatrix(self.train, vectorizer,None, None, None)
        # doing this just to pass the min and max of train to the other functions.
        x = vectorizer.fit_transform(self.train['text'])
        dataArr = pd.DataFrame(data=x.toarray())
        arr = dataArr.to_numpy()
        min = np.amin(arr, axis=None)
        max = np.amax(arr, axis=None)
        print("min is : " + str(min))
        print("max is: " + str(max))

        featureNames = vectorizer.get_feature_names_out()
        self.validFM = self.makeFeatureMatrix(self.validation, vectorizer, featureNames, min, max)
        self.testFM = self.makeFeatureMatrix(self.test, vectorizer, featureNames, min, max)

    def getVocabList(self, featureSet):
        vocabList = dict()
        # enumerate
        # what does this do?
        for count, value in enumerate(featureSet):
            # dictionary with keys as the string and the value as the index in the feature matrix.
            vocabList[value] = count
        return vocabList
    """
    Makes a categorical variable into something the model can use by encoding them 
    as vectors, with the number of dimensions being the number of categories and each
    index having a value of 0 or 1, 1 meaning it is the given language. A OHE vector
    can only have ONE 1 in this scenario, since you can't be two languages. 
    so, "Old English" becomes [1 0 0], "Old French" becomes [0 1 0], and "Old latin" becomes
    [0 0 1]. 
    """
    def oneHotEncode(self, dataList):
        encoder = LabelEncoder()
        #fits the encoder based on the list of languages we have established.
        encoder.fit(self.languageList)
        #this turns each category into a number between 0 and num_cat -1, so OE is 0, OF is 1, OL is 2.
        encoded = encoder.transform(dataList)
        self.encoder = encoder
        #converts list of nums between 0 and numCat-1 to a list of vectors(matrix) with a 1 indicating the category.
        vector = np_utils.to_categorical(encoded)
        return vector

    def trainModel(self, inputDim):
        #this gets the feature matrix of trigrams without the result.
        #why axis = 1?
        x = self.trainFM.drop('language',axis=1)
        #put the category of each input through the encoder, into variable y.
        y = self.oneHotEncode(self.trainFM['language'])

        #sequential model has one input matrix and one output vector
        model = Sequential()
        layerSize = inputDim
        #pick the features of the neural Net.
        model.add(Dense(layerSize, input_dim=inputDim,activation='relu'))
        model.add(Dense(layerSize,activation='relu'))
        model.add(Dense(layerSize/2, activation='relu'))
        model.add(Dense(len(self.languageList), activation='softmax'))
        #model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        clf = KerasClassifier(model=model, loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        #train model. Not sure which parameters to use.
        #model.fit(x,y, epochs=4, batch_size=100)
        clf.fit(x,y,epochs=4, batch_size=100)
        return clf
    def validateModel(self, model):
        """
        use this to fine tune parameters of the model.
        """
        xValidate = self.testFM.drop('language', axis=1)
        yValidate = self.testFM['language']
        labels = model.predict(xValidate)
        label = np.argmax(labels, axis=1)

        #print(model.summary())
        return

    def testModel(self, model):
        """
        test the accuracy of the model.
        """

        xTest = self.testFM.drop('language', axis=1)
        yTest = self.testFM['language']
        #for each test data, it gets a list of the relative probabilities it gives to each. This is a matrix.
        labels = model.predict(xTest)
        #gets just the maximum result of that list of relative probabilities to get the formal "guess".
        label = np.argmax(labels, axis=1)
        #gets the guesses back into the language string, like "Old English" or "Old French", from [1 0 0]
        predictions = self.encoder.inverse_transform(label)

        self.printTestsToFile(predictions, yTest)

        accuracy = accuracy_score(yTest, predictions)
        """
        confusionMatrix = confusion_matrix(yTest, predictions)
        confusionMatrixDF = pd.DataFrame(confusionMatrix, columns=self.languageList, index=self.languageList)
        plt.figure(figsize=(10,10), facecolor='w', edgecolor='k')
        sea.set(font_scale=1.5)
        sea.heatmap(confusionMatrixDF, cmap='coolwarm', annot=True, fmt='.5g', cbar=False)
        plt.xlabel('Predicted', fontsize=22)
        plt.ylabel('Actual', fontsize=22)
        plt.show()
        """

        return accuracy

    def doClassification(self):
        self.makeDataSet()
        #make trigrams only works if self.train is set, which comes from makeDataSet.
        trigramSet = self.makeTrigrams(self.train, 200)
        inputDim =len(trigramSet)
        self.makeAllFeatureMatrices(trigramSet)
        trainedModel = self.trainModel(inputDim)
        self.modelTrained = trainedModel

        self.validateModel(trainedModel)
        #self.calcImportance()
        #self.visualize(trainedModel)
        testResults = self.testModel(trainedModel)
        print("accuracy is: " + str(testResults))
    def inputModel(self):
        text1 = input("Enter a string of  text, we will guess the language\n")
        text2 = input("Enter more text")
        text = [text1, text2]
        #print(text)
        trigramSet = self.trainFM.columns
        self.trig = trigramSet
        vocabList = self.getVocabList(trigramSet)
        vectorizer = CountVectorizer(analyzer='char', ngram_range=(3, 3), vocabulary=vocabList)
        featureNames = vectorizer.get_feature_names_out()
        transformed = pd.DataFrame(vectorizer.fit_transform(text).toarray(), columns=featureNames)
        #print(transformed)
        labels = self.modelTrained.predict(transformed.drop('language', axis=1))
        print(labels)
        label = np.argmax(labels, axis=1)

        predictions = self.encoder.inverse_transform(label)
        print(text,predictions)
    def visualize(self,model):
        visualizer(model, format='png', view=True)
    def printTestsToFile(self, predictions, yTest):
        text = self.test
        with open("testPredictions", "w", encoding='utf-8')as file:
            listWrong = []
            file.write("each string, then guess, then actual result.\n")
            for i in range (0, len(text)):
                string = "Text :" + str(text['text'].iloc[i] )+ " , prediction: " + str(predictions[i]) + " , actual: " +str(yTest.iloc[i]) + "\n"

                if predictions[i] !=yTest.iloc[i]:
                    listWrong.append(string)
                else:
                    file.write(string)
            file.write("Wrong guesses: \n")
            for string in listWrong:
                file.write(string)
        return
    def countTrigrams(self):
        self.makeDataSet()
        data = self.train
        print(data)
        for language in self.languageList:
            # get only the rows with language == language
            corpus = data['text'][data['language'] == language]
            # we want to count how many trigrams were in all of these samples as a whole.
            vectorizer = CountVectorizer(analyzer='char', ngram_range=(3, 3),max_features=200)
            x=vectorizer.fit_transform(corpus)
            #print(x)
            textDoc = pd.DataFrame(x.todense())
            textDoc.columns = vectorizer.get_feature_names_out()
            textDocMatrix = textDoc.T
            textDocMatrix.columns = ["Line" + str(i) for i in range(0,len(corpus))]
            textDocMatrix['total_count'] = textDocMatrix.sum(axis=1)
            textDocMatrix = textDocMatrix.sort_values(by="total_count", ascending=False)[:50]
            with open("trigramCounts", "a", encoding='utf-8') as file:
                file.write("Language: " + language + '\n')
                file.writelines(str(textDocMatrix['total_count']))
                file.write("\n")
            print(textDocMatrix['total_count'].head(50))

            #new = vectorizer.inverse_transform(x)
           #print(new)
    def calcImportance(self):
        xVal = self.validFM.drop('language', axis=1)

        yVal = self.oneHotEncode(self.validFM['language'])
        print(yVal)
        set = self.trainFM.columns
        print(set)
        r = permutation_importance(self.modelTrained, xVal, yVal, n_repeats=5, random_state=0)
        print("got here\n")
        print(r.importances_mean)

        for i in r.importances_mean.argsort()[::-1]:
            print("iteration " + str(i))
            if r.importances_mean[i]-2*r.importances_std[i]>0:
                print(f"{set[i]:<8}"
                      f"{r.importances_mean[i]:.3f}"
                      f"+/-{r.importances_std[i]:.3f}")

def main():
    mll = machineLearningLanguages(["Old English", "Old French", "Old Latin"])
    #mll.countTrigrams()
    mll.doClassification()
    #mll.inputModel()

if __name__== "__main__":
    main()