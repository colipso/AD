# -*- coding: utf-8 -*-
"""
Created on Thu Apr 06 15:24:11 2017

@author: dapenghuang
"""
import numpy as np
import random
import time
from sklearn import linear_model
from sklearn import metrics
from scipy.sparse import csr_matrix
LR = linear_model.LogisticRegression
class LoadData:
    def __init__(self , filePath = u'F:\\AD\\1458\\'):
        self.filePath = filePath
    def loadTrain(self , trainFile = u'train.yzx.txt',maxline = 1000000):
        trainF = self.filePath + trainFile
        Y = []
        P = []
        X = []
        f = open(trainF)
        i = 0
        flag = 0
        for line in f.readlines():
            lineSplit = [int(d) for d in line.replace(':1','').strip('\n').split(' ')]
            y = lineSplit[0]
            if y == 1:
                Y.append(y)
                P.append(lineSplit[1])
                X.append(lineSplit[2:])
                i += 1
                if i > maxline:
                    break
                flag = 1
            elif flag == 1:
                Y.append(y)
                P.append(lineSplit[1])
                X.append(lineSplit[2:])
                i += 1
                if i > maxline:
                    break
                flag = 0
                
        f.close()
        return {'x':X,'y':Y,'p':P}
        
    def loadFeatureLen(self , featureFile = u'featindex.txt'):
        featureF = self.filePath + featureFile
        f = open(featureF)
        featureLen = 0
        for line in f.readlines():
            featureLen += 1
        f.close()
        self.featureLen = featureLen
        return featureLen
        
    def loadTest(self , testFile = u'train.yzx.txt' , maxline = 100000):
        trainF = self.filePath + testFile
        Y = []
        P = []
        X = []
        f = open(trainF)
        i = 0
        for line in f.readlines():
            lineSplit = [int(d) for d in line.replace(':1','').strip('\n').split(' ')]
            y = lineSplit[0]
            Y.append(y)
            P.append(lineSplit[1])
            X.append(lineSplit[2:])
            i += 1
            if i > maxline:
                break
        f.close()
        return {'x':X,'y':Y,'p':P}
        
    def sparseMatrix(self,matrix):
        colNum = self.featureLen
        i = 0
        sx = []
        sy = []
        sd = []
        for line in matrix:
            for d in line:
                sx.append(i)
                sy.append(d)
                sd.append(1)
            i += 1
        X = csr_matrix((sd, (sx, sy)), shape=(i, colNum))
        return X
    def constructTrainData(self):
        self.loadFeatureLen()
        data = self.loadTrain()
        x = data['x']
        y = np.array(data['y'])
        return {'x':self.sparseMatrix(x) , 'y':y}
        
    def constructTestData(self):
        data = self.loadTest()
        x = data['x']
        y = np.array(data['y'])
        return {'x':self.sparseMatrix(x) , 'y':y}
    

class PredictClick:
    def __init__(self):
        self.LD = LoadData()
        self.LD.loadFeatureLen()
    def trainModel(self,trainData):
        trainBeginT = time.time()
        model = LR()
        x = trainData['x']
        y = trainData['y']
        print type(x)
        print y
        model.fit(x,y)
        self.model = model
        trainEndT = time.time()
        print u'train use %f minutes ' % ((trainEndT-trainBeginT)/60)
        return model
    def testModel(self,testData):
        x = testData['x']
        y = testData['y']
        y_pred = self.model.predict(x)
        result = metrics.confusion_matrix(y, y_pred)
        print result
        print self.model.score(x,y)
    def predict(self , data):
        BeginT = time.time()
        result = self.model.predict(self.LD.sparseMatrix(data))
        print result
        EndT = time.time()
        print u'predict use %f seconds ' % (EndT-BeginT)
        return result

#test#
LD = LoadData()
trainData = LD.constructTrainData()
testData = LD.constructTestData()
PC = PredictClick()
PC.trainModel(trainData)
PC.testModel(testData)

data = [[0,27,28,181028,30,31,4253,5762,15,35,36,37,208,39,40,51,1102,1008,77]]
PC.predict(data)
