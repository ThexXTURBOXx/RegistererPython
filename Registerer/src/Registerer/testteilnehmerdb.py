# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 10:44:58 2016

@author: root
"""

import MySQLdb

connection = MySQLdb.connect(host="localhost", db="teilnehmer", user="sfz", passwd="pass1234")
print "Connected"
cursor = connection.cursor()
print cursor.execute("SELECT * FROM teilnehmer")
print cursor.fetchall()