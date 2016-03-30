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

def responseFromURL(url):
    buf = cStringIO.StringIO()

    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.perform()

    responseString = buf.getvalue()
    buf.close()

    return responseString


def hrefFromBufWithAnchor(anchorString, buf, fromPos, endPos):
    hrefStartAnchor = 'href=\"'
    hrefEndAnchor = '\"'

    nextPageURL = ''
    anchorPos = buf.find(anchorString, fromPos, endPos)
    if anchorPos >= 0:
        hrefPosStart = searchBuf.rfind(hrefStartAnchor, 0, anchorPos)
        if hrefPosStart >= 0:
            hrefPosStart = hrefPosStart + len(hrefStartAnchor)
            hrefPosEnd = searchBuf.find(hrefEndAnchor, hrefPosStart, anchorPos)
            if hrefPosEnd >= 0:
                nextPageURL = searchBuf[hrefPosStart : hrefPosEnd]

    retData = []
    if nextPageURL <> '':
        retData = [anchorPos, nextPageURL]

    return retData

def weixinFromBufWithAnchor(anchorString, buf, fromPos, endPos):
    retData = []
    weixinIDString = ''
    bufLen = len(buf)
    
    anchorPos = buf.find(anchorString, fromPos, endPos)
    if anchorPos >= 0:
        checkEndPos = anchorPos + 50
        if checkEndPos > bufLen:
            checkEndPos = bufLen
        
        searchString = buf[anchorPos : checkEndPos]
        weixinReg = re.compile('[a-zA-Z\d_]{5,}')
        retP = weixinReg.search(searchString)
        if retP:
            weixinIDString = retP.group(0)
        else:
            weixinIDString = ''
        retData = [anchorPos, weixinIDString]

    return retData

def addWeixinIDsToArray(idArray, buf):
    startPos = 0
    bufLen = len(buf)
    weixinAnchorString = '<em>微信</em>'
    while (startPos >= 0):
        idData = weixinFromBufWithAnchor(weixinAnchorString, buf, startPos, bufLen)
        if len(idData) >= 2:
            startPos = idData[0] + len(weixinAnchorString)
            weixinString = idData[1]
            if weixinString <> '' and weixinString <> 'class':
                idArray.append(weixinString)
        else:
            startPos = -1

########################################
########################################
gClearCmd = ''
gResultPath = './result/'

sysstr = platform.system()
if (sysstr =="Windows"):
    gClearCmd = 'cls'
else:
    gClearCmd = 'clear'
            
if len(sys.argv) > 1:
    index = 1
    
    gResultFileName = gResultPath
    
    while index < len(sys.argv):
        gKeyWordString = gKeyWordString + sys.argv[index]
        gResultFileName = gResultFileName + sys.argv[index]
        index = index + 1

        if (index < len(sys.argv)):
            gKeyWordString = gKeyWordString + '%20'
            gResultFileName = gResultFileName + ' '
        else:
            gResultFileName = gResultFileName + '.txt'

else:
    exit()

snapURLArray = []
weixinIDArray = []

gSearchURL = gBaiduHostURL + '/s?wd=' + gKeyWordString
pageIndex = 1

os.system(gClearCmd)
if not os.path.exists(gResultPath):
    os.mkdir(gResultPath)

while (gSearchURL <> '' and pageIndex <= 100):
    print "page %d: " %pageIndex,
    #print gSearchURL

    searchBuf = responseFromURL(gSearchURL)
    bufLen = len(searchBuf)
    #print gSearchURL
    #print '.....:'
    #print searchBuf

    nextPageURLData = hrefFromBufWithAnchor('>下一页&gt;</a>', searchBuf, 0, bufLen)
    if len(nextPageURLData) >= 2:
        gSearchURL = gBaiduHostURL + nextPageURLData[1]
        pageIndex = pageIndex + 1
    else:
        gSearchURL = ''

    snapStartPos = 0
    snapAnchorString = '>百度快照</a>'
    while (snapStartPos >= 0):
        snapURLData = hrefFromBufWithAnchor(snapAnchorString, searchBuf, snapStartPos, bufLen)
        if len(snapURLData) >= 2:
            snapStartPos = snapURLData[0] + len(snapAnchorString)
            snapURLString = snapURLData[1]
            snapURLArray.append(snapURLString)
        else:
            snapStartPos = -1

    addWeixinIDsToArray(weixinIDArray, searchBuf)
    print len(weixinIDArray)
    time.sleep(random.randrange(1, 3, 1))

'''
for snapURLString in snapURLArray:
    print snapURLString
    print ''
    searchBuf = responseFromURL(snapURLString)
    bufLen = len(searchBuf)
    print searchBuf

    weixinString = weixinFromBufWithAnchor(weixinAnchorString, searchBuf, 0, bufLen)
    weixinIDArray.append(weixinString)
    
    a = raw_input('...')
'''

#print "ID Array"
#print weixinIDArray

deIDArray = list(set(weixinIDArray))
#print "去重"
os.system(gClearCmd)
print 'count: ',
pprint.pprint(len(deIDArray))
print ''
pprint.pprint(deIDArray)


f=open(gResultFileName,'w')
for i in deIDArray:
    f.write(str(i)+"\n")
f.close()





