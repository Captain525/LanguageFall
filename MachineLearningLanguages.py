import pandas as pd
import numpy as np
import re

from sklearn.feature_extraction.text import CountVectorizer
#import seaborn as sns
#import matplotlib.pyplot as plt
#import warningswarnings.simplefilter("ignore")
class machineLearningLanguages():
    def __init__(self, listLangs):
        self.languageList = listLangs
        self.trainingPercent = .7
        self.validationPercent = .2
        self.testPercent = .1
        self.train =pd.DataFrame(columns = ['text', 'language'])
        self.validation = pd.DataFrame(columns = ['text', 'language'])
        self.test = pd.DataFrame(columns = ['text', 'language'])
        self.trainFM
        self.validFM
        self.testFM
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
        global languageList

        #does this matter?
        conditionalLength = [True if 10<=len(s) else False for s in data['text']]
        data = data[conditionalLength]
        print(data)

        dataRandom = pd.DataFrame(columns = ['text', 'language'])
        print(len(languageList))
        for lang in languageList:
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
        featureNames = vectorizer.get_feature_names()
        print(featureNames)
        return featureNames
    """
    Scales the feature matrix using minMax scaling. 
    """
    def scaleFM(self, featureMatrix, min, max):
        #to show its the training set
        if(min==None and max==None):
            min = featureMatrix.min()
            max = featureMatrix.max()
        #scale the values in the matrix by subtracting the minimum, then dividing by range.
        scaledFeature = (featureMatrix - min)/(max - min)
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
        if featureNames==None:
            featureNames= vectorizer.get_feature_names()
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

        vectorizer = CountVectorizer(analyzer='char', ngram_range=(3, 3), vocabulary=vocabList)
        self.trainFM = self.makeFeatureMatrix(self.train, vectorizer,None, None, None)
        min = self.trainFM.min()
        max = self.trainFM.max()
        featureNames = vectorizer.get_feature_names
        self.validFM = self.makeFeatureMatrix(self.validation, vectorizer, featureNames, min, max)
        self.testFM = self.makeFeatureMatrix(self.test, vectorizer, featureNames, min, max)



    def doClassification(self):
        self.makeDataSet()
        trigramSet = self.makeTrigrams(self.train, 200)

def main():
    mll = machineLearningLanguages(["Old English", "Old French", "Old Latin"])
    mll.doClassification()

if __name__== "__main__":
    main()