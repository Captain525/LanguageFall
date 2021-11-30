import pandas as pd
import numpy as np
import re
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import np_utils


from sklearn.feature_extraction.text import CountVectorizer
#import seaborn as sns
#import matplotlib.pyplot as plt
#import warningswarnings.simplefilter("ignore")
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler, LabelEncoder


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
    """
        
    trainingPercent = .7
    validationPercent = .2
    testPercent = .1
    train = pd.DataFrame(columns = ['text', 'language'])
    validation = pd.DataFrame(columns = ['text', 'language'])
    test = pd.DataFrame(columns = ['text', 'language'])
    languageList = ["Old English", "Old French", "Old Latin"]
    """


    #make the data set.
    def makeDataSet(self):
        #header = 0 to show to skip the first line bc those are names of columns.
        data = pd.read_csv('languageData.csv', header=0,skip_blank_lines=True, encoding='utf-8')
        #does this matter?
        conditionalLength = [True if 10<=len(s) else False for s in data['text']]
        data = data[conditionalLength]
        print(data)

        dataRandom = pd.DataFrame(columns = ['text', 'language'])
        print(len(self.languageList))
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
            trigramList = self.getTrigramsLanguage(corpus, amount)
            #add trigrams to dictionary.
            features[language] = trigramList
            featureSet.update(trigramList)
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
        vocabList = dict()
        # enumerate
        # what does this do?
        for count, value in enumerate(featureSet):
            # dictionary with keys as the string and the value as the index in the feature matrix.
            vocabList[value] = count

        #print(vocabList)
        vectorizer = CountVectorizer(analyzer='char', ngram_range=(3, 3), vocabulary=vocabList)
        self.trainFM = self.makeFeatureMatrix(self.train, vectorizer,None, None, None)
        # doing this just to pass the min and max of train to the other functions.
        x = vectorizer.fit_transform(self.train['text'])
        dataArr = pd.DataFrame(data=x.toarray())
        arr = dataArr.to_numpy()
        print(self.trainFM)
        min = np.amin(arr, axis=None)
        max = np.amax(arr, axis=None)
        print(min)
        print(max)

        featureNames = vectorizer.get_feature_names_out()
        self.validFM = self.makeFeatureMatrix(self.validation, vectorizer, featureNames, min, max)
        self.testFM = self.makeFeatureMatrix(self.test, vectorizer, featureNames, min, max)

        print(self.validFM)
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
        layerSize = 500
        #pick the features of the neural Net.
        model.add(Dense(layerSize, input_dim=inputDim,activation='relu'))
        model.add(Dense(layerSize,activation='relu'))
        model.add(Dense(layerSize/2, activation='relu'))
        model.add(Dense(len(self.languageList), activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        #train model. Not sure which parameters to use.
        model.fit(x,y, epochs=4, batch_size=100)
        return model
    def validateModel(self):
        """
        use this to fine tune parameters of the model.
        """
    def testModel(self, model):
        """
        test the accuracy of the model.
        """
        xTest = self.testFM.drop('language', axis=1)
        yTest = self.testFM['language']

        labels = model.predict(xTest)
        label = np.argmax(labels, axis=1)
        predictions = self.encoder.inverse_transform(label)

        accuracy = accuracy_score(yTest, predictions)
        return accuracy

    def doClassification(self):
        self.makeDataSet()
        #make trigrams only works if self.train is set, which comes from makeDataSet.
        trigramSet = self.makeTrigrams(self.train, 200)
        inputDim =len(trigramSet)
        self.makeAllFeatureMatrices(trigramSet)
        trainedModel = self.trainModel(inputDim)
        self.modelTrained = trainedModel
        testResults = self.testModel(trainedModel)
        print("accuracy is: " + str(testResults))


def main():
    mll = machineLearningLanguages(["Old English", "Old French", "Old Latin"])
    mll.doClassification()

if __name__== "__main__":
    main()