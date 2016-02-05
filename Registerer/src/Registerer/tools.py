# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 10:28:02 2016

@author: root
"""



def readStudentInfoFromFile(filename = "teilnehmer.txt"):
    studentFile = open(filename)
    rows = studentFile.readlines()
    studentFile.close()
    keys = ("lastname", "firstname", "mobile", "phone", "email", "contactlname", "contactfname")
    data = []
    i = 0    
    rowDict = {}
    for entry in rows[8:]:
        entry = entry.strip("\n")
        entry = entry.replace(" ", "")
        if i > 5:
            data.append(rowDict)
            rowDict={}
            i = 0        
        if i <= 4:
            rowDict.update({keys[i]:entry})
            i += 1
        elif i == 5:
            entry = entry.split(",")
            rowDict.update({keys[5]:entry[0], keys[6]:entry[1]})
            i += 1
    for entry in data:
        print entry
        
readStudentInfoFromFile()