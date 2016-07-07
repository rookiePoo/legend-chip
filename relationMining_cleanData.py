# -*- coding: utf-8 -*-
"""
Created on Mon July 04 22:53:09 2016

@author: Paul_J
"""


import pandas as pd

def Age2Stage(age):
    if age == -1:
        return ''
    if age < 18:
        return 'underage'
    elif age < 45:
        return 'middleage'
    else:
        return 'oldage'
        
#def Survived2LiveorDead(survive):
#    if survive = ''

if __name__ == '__main__':
    colsNeed = ['Survived','Pclass','Sex','Age','SibSp','Parch']
    dataTable = pd.read_table(r"E:\\Code\\python\\DataMining\\train.csv",sep = ',',index_col = 'PassengerId')
    dataNeedTable = dataTable[colsNeed]
    dataNeedTable.fillna(-1,inplace = True)
    dataNeedTable['Kinsfolk'] = dataNeedTable['SibSp'] + dataNeedTable['Parch']
    #dataNeedTable['Stage'] = ''
    
    
    for eachPerson in dataNeedTable.index:
        # change age representation
        dataNeedTable.loc[eachPerson,'Age'] = Age2Stage(dataNeedTable['Age'][eachPerson])
#    dataNeedTable['Age'][dataNeedTable['Age'] == -1] = ''
#    dataNeedTable['Age'][dataNeedTable['Age'] < 18] = 'underage'
#    dataNeedTable['Age'][dataNeedTable['Age'] < '45'] = 'middleage'
#    dataNeedTable['Age'][dataNeedTable['Age'] >='45'] = 'oldage'
    dataNeedTable['Survived'][dataNeedTable['Survived'] == 0] = 'dead'
    dataNeedTable['Survived'][dataNeedTable['Survived'] == 1] = 'live'
    dataNeedTable['Kinsfolk'][dataNeedTable['Kinsfolk'] != 0] = 'withfolk'
    dataNeedTable['Kinsfolk'][dataNeedTable['Kinsfolk'] == 0] = 'withoutfolk'
    
    dataNeedTable = dataNeedTable[['Survived','Pclass','Sex','Age','Kinsfolk']]
    print dataNeedTable
    dataNeedTable.to_csv(r"E:\\Code\\python\\DataMining\\dataProed.txt",sep='|')
    
        

