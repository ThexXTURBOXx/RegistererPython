# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 00:20:01 2016

@author: root
"""

import MySQLdb as db
import numpy as np
import qrcode as qc

dbHost="localhost"
dbName="teilnehmer"
dbUser="sfz"
dbPasswd="pass1234"


def getTeilnehmerListeIDName():
    """Gibt Numpyarray mit allen IDs und Namen der Teilnehmer aus. Ohne Ansprechpartner und Kategorie."""
    
    connection = db.connect(host=dbHost, db=dbName, user=dbUser, passwd=dbPasswd)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM teilnehmer;")
    teilnehmerListeTmp = cursor.fetchall()
    cursor.close()
    teilnehmerListe = np.array(teilnehmerListeTmp)

    return teilnehmerListe[:,0:3]


def createQRCodesTeilnehmer(teilnehmerListe):
    """Speichert für jeden Teilnehmer einen QRCode im Unterverzeichnis
        "/studentcodes" ab. QRCode-Text: "student_<ID>"."""

    for student in teilnehmerListe:
        filename = "studentcodes/" + student[1] + "_" + student[2]
        qrtext = "student_" + student[0]
        qc.erzeugen(text=qrtext, filename=filename)
        print "Saved QR-Code for student no. " + student[0] + "."
        

