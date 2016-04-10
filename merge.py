#!/usr/bin/python
#-*-coding:utf-8-*-

import pycurl
import re
import sys
import os
import time
import datetime
import random
import json
import pprint
import cStringIO
import cPickle

import platform

########################################
########################################

gBaiduHostURL = 'http://www.baidu.com'
gResultFileName = ''
gKeyWordString = ''
gSearchURL = ''

########################################
########################################

def TestPlatform():
    print ("----------Operation System--------------------------")
    #Windows will be : (32bit, WindowsPE)
    #Linux will be : (32bit, ELF)
    print(platform.architecture())

    #Windows will be : Windows-XP-5.1.2600-SP3 or Windows-post2008Server-6.1.7600
    #Linux will be : Linux-2.6.18-128.el5-i686-with-redhat-5.3-Final
    print(platform.platform())

    #Windows will be : Windows
    #Linux will be : Linux
    print(platform.system())

    print ("--------------Python Version-------------------------")
    #Windows and Linux will be : 3.1.1 or 3.1.3
    print(platform.python_version())

def UsePlatform():
  sysstr = platform.system()
  if(sysstr =="Windows"):
    print ("Call Windows tasks")
  elif(sysstr == "Linux"):
    print ("Call Linux tasks")
  else:
    print ("Other System tasks")


########################################
########################################

def GetParentPath(strPath):
    if not strPath:
        return None
    
    lsPath = os.path.split(strPath)
    print(lsPath)
    print("lsPath[1] = %s" %lsPath[1])
    if lsPath[1]:
        return lsPath[0]
    
    lsPath = os.path.split(lsPath[0])

    return lsPath[0]

def GetSameFileNameOnParentPath(strPath):
    if not strPath:
        return None
    
    lsPath = os.path.split(strPath)
    if lsPath[1]:
        return os.path.join(lsPath[0], lsPath[1]+".txt")
    else:
        return lsPath[0]+".txt"

def filesInPath(parentDir):
    filesArray = []
    for parent,dirnames,filenames in os.walk(parentDir):
        for filename in filenames:
            filesArray.append(os.path.join(parent, filename))

    return filesArray

def listFromFile(filename):
    f = open(filename,'r')
    dataList = f.readlines()
    f.close()
    
    return dataList

def mergedListFromFileArray(filesArray):
    mergedSet = set([])
    
    for fileName in filesArray:
        if (fileName.find(".txt") == -1):
            continue
        
        dataList = listFromFile(fileName)
        mergedSet = mergedSet.union(set(dataList))
    
        print dataList

    return list(mergedSet)
########################################
########################################
gClearCmd = ''

sysstr = platform.system()
if (sysstr =="Windows"):
    gClearCmd = 'cls'
else:
    gClearCmd = 'clear'

gFilesArray = []

if len(sys.argv) > 1:
    searchDir = sys.argv[1]

    if os.path.exists(searchDir):
        gFilesArray = filesInPath(searchDir)

if (len(gFilesArray) <= 0):
    exit()

mergedArray = mergedListFromFileArray(gFilesArray)

os.system(gClearCmd)

mergedArrayB = []
for i in mergedArray:
    strValue = str(i)
    strValue = strValue.strip("\n")
    mergedArrayB.append(strValue)
mergedArrayB = list(set(mergedArrayB))


resultPath = GetSameFileNameOnParentPath(searchDir)

f=open(resultPath,'w')
for i in mergedArrayB:
    strValue = str(i)
    f.write(strValue+"\n")
f.close()





