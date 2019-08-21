# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 11:38:48 2019
@author: Elizabeth Ighodaro
Student ID:999993862
NOTE: The bonus part has been implemented. This takes about 3 minutes to run because
the length of the list after removing stopwords is over two hundred thousand.
"""
import sys
import os
from email.parser import Parser
import re
import json
import urllib.request
from nltk import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


rootdir = 'emailfor/Data'
run = True

def option():
    print('1 Word Search')
    print('2 Find Contacts')
    print('3 Track an Email message')
    print('4 Find an IP location')
    print('5 Content Analysis')
    print('0 Exit')
    print('Your Choice?')
    x = int(input())
    if x == 1:
        wordsearch()
    elif x==2:
        findContacts()
    elif x == 3:
        trackEmail()
    elif x ==4:
        ipLookup()
    elif x == 5:
        frequentWords()
    elif x == 0:
        sys.exit()
    else:
        print('Wrong choice. Please enter 1,2,3,4 or 5 accordingly')
email_body = []
#wordsearch
def wordsearch():
    print('Enter search query')
    word = str(input())
    for directory, subdirectory, filenames in  os.walk(rootdir):
        for filename in filenames:
            inputfile = os.path.join(directory, filename)
            with open(inputfile, 'r', encoding = 'latin-1') as f:
                data = f.read()
                mail = Parser().parsestr(data)
                content = mail.get_payload()
                email_body.append(content)
                if word in content:
                    print(filename)
 
#wordsearch()

def findContacts():
    print('Enter EMail address eg "godo <goran@dobosevic.com>" or debian-user@lists.debian.org ')
    mail_Id = str(input())
    for directory, subdirectory, filenames in  os.walk(rootdir):
        for filename in filenames:
            inputfile = os.path.join(directory, filename)
            with open(inputfile, 'r', encoding = 'latin-1') as f:
                data = f.read()
                mail = Parser().parsestr(data)
                to = mail['to']
                #to = re.findall(r'([\w0-9._-]+@[\w0-9._-]+\.[\w0-9_-]+)',to)
                from_id = mail['from']
                #from_id = re.findall(r'([\w0-9._-]+@[\w0-9._-]+\.[\w0-9_-]+)',from_id)
                
                if mail_Id == to:
                    print('Received Email from:' + from_id)
                elif mail_Id == from_id:
                    print('Sent Email to: ' + to)
                else: print('Email address not found')
                break

                
def trackEmail():
    print('Enter file Name. File extension is optional')
    file = str(input())
    if file.endswith('.eml'):
        eml_file = os.path.join(rootdir,file)
    else: 
        x = file + '.eml'
        eml_file =os.path.join(rootdir,x)
    try:
        with open(eml_file, 'r', encoding = 'latin-1') as f:
            data = f.read()
            msg = Parser().parsestr(data, headersonly = True) 
            #11 Apr 2010 10:18:05
            ipAddress = re.findall(r'(?<![.\d])\b\d{1,3}(?:\.\d{1,3}){3}\b(?![.\d])', str(msg))
            timeStamp = re.findall(r'\w*[,] [\d]{1,2} [ADFJMNOS]\w* [\d]{4} [\d]{1,2}[:][\d]{1,2}[:][\d]{1,2}', str(msg))
            print(ipAddress + timeStamp)
    except FileNotFoundError:
        print('Wrong file name specified. Please retry')
        
    
def ipLookup():
    print('Enter IP Address')
    ip = str(input())
    api = 'http://api.ipstack.com/' + ip + '?access_key=5c5f30c57427e2b43307201b9cffc007' + '&format=1'
    result = urllib.request.urlopen(api).read()
    result = result.decode()
    result = json.loads(result)
    print('Country: ' + str(result['country_name']))
    print('City: ' + str(result['city']))
    print('Latitude: ' + str(result['latitude']))
    print('Longitude: ' + str(result['longitude']))


iterList = []
wordList = []
    
def extractWords():
    for k in email_body:
        words = re.sub("[^a-zA-Z]", " ",str(k))
        no_single = re.sub(r'(?:^| )\w(?:$| )', ' ', words).strip()
        words = word_tokenize(words.lower())
        iterList.append(words)
    for sublist in iterList:
        for value in sublist:
            wordList.append(value)
    
def frequentWords():
    extractWords()
    corpus = [word for word in wordList if word not in stopwords.words('english') ]
    freq = FreqDist(corpus)
    print(freq.most_common(5))
        
while run:
    option()
    


