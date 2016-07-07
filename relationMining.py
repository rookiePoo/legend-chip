# -*- coding: utf-8 -*-
"""
Created on Mon July 04 22:53:09 2016

@author: Paul_J
"""

import pandas as pd
import numpy as np
import copy

class FrequentItemSet():
    def __init__(self,count):
        self.countNum = count
    def initNextFISDict(self,nFISDict):
        self.nextFISDict = nFISDict


def DataFrame2TransList(dataTable):
    transList = []
    for eachPerson in dataTable.index:
        personAttriList = []
        for i in range(len(dataTable.ix[eachPerson])):
            if dataTable.ix[eachPerson,i] != '':
                personAttriList.append(dataTable.ix[eachPerson,i])
        transList.append(personAttriList)
    return transList,len(dataTable.ix[1])

def removeUnderSupOrConf(thisKList,k):
    for eachAttr in thisKList:
#        print eachAttr,freItemSet_dict[eachAttr]
        support = float(freItemSet_dict[eachAttr])/transNumber
        
        if support<minSup:
#            print eachAttr,support
            freItemSet_dict.pop(eachAttr)
            freItemSet_list[k].remove(eachAttr)
            
def BuildFrequentItemSet1(allAttriList,transList):
    tempOneList = []
    freItemSet_list.append(copy.deepcopy(allAttriList))
#    print freItemSet_list
    for eachList in transList:
        tempOneList.extend(eachList)
    for eachAttri in allAttriList:
        freItemSet_dict[eachAttri] = tempOneList.count(eachAttri)
#    print freItemSet_dict
#    print allAttriList
    removeUnderSupOrConf(allAttriList,0)
    #print freItemSet_list
    #print freItemSet_dict

def strList2StringWithSpace(strList):
    return ' '.join(strList)
    
def findNextListInAttriList(allAttriList,lastEle):
    index = allAttriList.index(lastEle)
    return allAttriList[index:]

def ifSubList(listAll,listSub):
    for eachEle in listSub:
        if eachEle in listAll:
            listAll.remove(eachEle)
        elif eachEle not in listAll:
            return 0
    return 1

def BuildFrequentItemSetK(allAttriList,transList,transWide):
    for i in range(1,transWide):
        tempListKminus1 = freItemSet_list[i-1]
        if len(tempListKminus1)<2:
            break
        tempListK = []
        for eachFISKminus1 in tempListKminus1:
            fisEleList = eachFISKminus1.split(' ')
            lastEle = fisEleList[-1]
            nextList = findNextListInAttriList(allAttriList,lastEle)
            if len(nextList)!=0:
                for eachNextEle in nextList:
                    listFISk = copy.deepcopy(fisEleList)
                    listFISk.append(eachNextEle)
                    strFISk = strList2StringWithSpace(listFISk)
                    tempListK.append(strFISk)
        for eachFISk in tempListK:
            freItemCount = 0
            FISkList = eachFISk.split(' ')
            for eachTrans in transList:
                #print eachTrans,FISkList
                eachTransCopy = copy.deepcopy(eachTrans)
                if ifSubList(eachTransCopy,FISkList):
                    freItemCount = freItemCount + 1
            freItemSet_dict[eachFISk] = freItemCount
        freItemSet_list.append(copy.deepcopy(tempListK))
        removeUnderSupOrConf(tempListK,i)
        #print freItemSet_list
        #print 
    #print freItemSet_dict

def sortAccToAttriList(allAttriList,sortingList):
    return sorted(sortingList, key=lambda x:allAttriList.index(x))

def GenRulesWithPost1(strFISEle,allAttriList):
    strFISEleList = strFISEle.split(' ')
    post1List = list(strFISEleList)
    usefulPostList = []
    for eachPost in post1List:
        tempPriorList = list(strFISEleList)
        tempPriorList.remove(eachPost)
        sortedTempPriorList = sortAccToAttriList(allAttriList,tempPriorList)
        tempPriorStr = strList2StringWithSpace(sortedTempPriorList)
        conf = float(freItemSet_dict[strFISEle])/float(freItemSet_dict[tempPriorStr])
        if conf<minConf:
            continue
        supp = float(freItemSet_dict[strFISEle])/transNumber
        rule = tempPriorStr + '=>' + eachPost
        usefulPostList.append(eachPost)
        rules_dict[rule] = [supp,conf]
    return usefulPostList

def unionPost(allAttriList,postList1,postList2,postLen):
    curPostLen = postLen + 1
    newPostList = list(set(postList1).union(set(postList2)))
    if len(newPostList)!=curPostLen:
        return 'NotRequiredLen'
    else:
        newPostList = sortAccToAttriList(allAttriList,newPostList)
        return newPostList
    

       
def GenRulesWithPostMore1(allAttriList,strFISEle,usefulPost1List):
    strFISEleList = strFISEle.split(' ')
    maxPostLen = len(strFISEleList)/2
    prePostList = usefulPost1List
    #curPostList = []
    while len(prePostList)>0:
        postLen = len(prePostList[0].split(' '))
        if postLen>=maxPostLen:
                break
        curPostList = []
        for i in range(len(prePostList)):
            eachPostEle = prePostList[i]
            postList1 = eachPostEle.split(' ')
            for j in range(i+1,len(prePostList)):
                postList2 = prePostList[j].split(' ')
                curPostEleList = unionPost(allAttriList,postList1,postList2,postLen)
                if curPostEleList == 'NotRequiredLen':
                    continue
                curPostEle = strList2StringWithSpace(curPostEleList)
                curPostList.append(curPostEle)
        #对列表去重
        if len(curPostList)==0:
            break
        prePostList = list(set(curPostList))
        for eachPost in prePostList:
            tempstrFISEleList = list(strFISEleList)
            eachPostList = eachPost.split(' ')
            for eachPostListEle in eachPostList:
                tempstrFISEleList.remove(eachPostListEle)
            tempPriorStr = strList2StringWithSpace(tempstrFISEleList)
            conf = float(freItemSet_dict[strFISEle])/float(freItemSet_dict[tempPriorStr])
            supp = float(freItemSet_dict[strFISEle])
            if conf<minConf:
                continue 
            supp = float(freItemSet_dict[strFISEle])/transNumber
            rule = tempPriorStr + '=>' + eachPost
            rules_dict[rule] = [supp,conf]
        #print prePostList
        #print 
                
        
           
            
            
        
  
freItemSet_dict = {}
freItemSet_list = []
rules_dict = {}
minSup = 0.15
minConf = 0.75
transNumber = 0.0
if __name__ == '__main__':
    allAttriList = ['live','dead','1','2','3','male','female','underage','middleage','oldage','withfolk','withoutfolk']
    dataTable = pd.read_table(r"E:\\Code\\python\\DataMining\\dataProed.txt",sep = '|',index_col = 'PassengerId')
    dataTable.fillna('',inplace = True)
    dataTable = dataTable.astype(np.string_)
    #print dataTable
    transList,transWide = DataFrame2TransList(dataTable)
    transNumber = float(len(transList))
    #print transWide
    BuildFrequentItemSet1(allAttriList,transList)
    BuildFrequentItemSetK(allAttriList,transList,transWide)
    for i in range (2,transWide):
        for eachFISEle in freItemSet_list[i]:
            usefulPost1List = GenRulesWithPost1(eachFISEle,allAttriList)
            #print eachFISEle,usefulPost1List
            GenRulesWithPostMore1(allAttriList,eachFISEle,usefulPost1List)
    fisListPath = r'E:\\Code\\python\\DataMining\\freItemSetList15_75.txt'
    fisRulesPath = r'E:\\Code\\python\\DataMining\\freItemSetRules15_75.txt'
    fisListFP = open(fisListPath,'w')
    fisRulesFP = open(fisRulesPath,'w')
    for eachFISList in freItemSet_list:
        for eachFIS in eachFISList:
            fisListFP.write(eachFIS + '|' + str(freItemSet_dict[eachFIS]))
            fisListFP.write('\n')
    for key in rules_dict.keys():
        supp = str(rules_dict[key][0])
        conf = str(rules_dict[key][1])
        fisRulesFP.write(key + '|' + supp + '|' + conf)
        fisRulesFP.write('\n')
    fisListFP.close()
    fisRulesFP.close()
    print freItemSet_dict
    print
    print freItemSet_list
    print
    print rules_dict

    
    
