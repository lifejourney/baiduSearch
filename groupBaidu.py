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

def listFromFile(filename):
    f = open(filename,'r')
    dataList = f.readlines()
    f.close()
    
    return dataList

########################################
########################################
gClearCmd = ''
gOutputDir = './'
gKeywordFileName = ''

sysstr = platform.system()
if (sysstr =="Windows"):
    gClearCmd = 'cls'
else:
    gClearCmd = 'clear'
            
if len(sys.argv) > 1:
    index = 1
    while index < len(sys.argv):
        argValue = sys.argv[index]
        
        if index == 1:
            gKeywordFileName = argValue
        
        index = index + 1

    baseName = os.path.basename(gKeywordFileName)
    extName = baseName.split('.')[-1]
    baseName = baseName.strip('.' + extName)
    dirName = os.path.dirname(gKeywordFileName)
    if dirName == None or dirName == '':
        dirName = '.'
    curDate = time.strftime('%Y-%m-%d\ ',time.localtime(time.time()))

    gOutputDir = dirName + '/' + curDate + baseName + '/result/'
else:
    exit()

keywordArray = listFromFile(gKeywordFileName)
for gKeyWordString in keywordArray:
    gKeyWordString = gKeyWordString.strip("\n")
    gKeyWordString = gKeyWordString.strip()
    if len(gKeyWordString) <= 0:
        continue

    baiduString = 'python ./baidu.py --output' + gOutputDir + ' ' + gKeyWordString
    os.system(baiduString)

mergeString = 'python ./merge.py ' + gOutputDir
os.system(mergeString)

print '已完成'




