# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 00:20:01 2016

@author: root
"""

import MySQLdb as db
import MySQLdb.cursors
import qrcode as qc

dbHost="localhost"
dbName="teilnehmer"
dbUser="sfz"
dbPasswd="pass1234"


def getTeilnehmerListeIDName():
    """Gibt Numpyarray mit allen IDs und Namen der Teilnehmer aus.
        Ohne Ansprechpartner und Kategorie."""
    
    connection = db.connect(
        host=dbHost,
        db=dbName,
        user=dbUser,
        passwd=dbPasswd,
        cursorclass=MySQLdb.cursors.DictCursor,
        use_unicode=True,
        charset="utf8"
        )
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM teilnehmer;")
    teilnehmerListeTmp = cursor.fetchall()
    cursor.close()

    return teilnehmerListeTmp


def createQRCodesTeilnehmer(teilnehmerListe):
    """Speichert für jeden Teilnehmer einen QRCode im Unterverzeichnis
        "/studentcodes" ab. QRCode-Text: "student_<ID>"."""

    for student in teilnehmerListe:
        filename = "studentcodes/" + student["name"].encode("utf-8") + "_" \
            + student["vorname"].encode("utf-8")
        qrtext = "student_" + (str)(student["ID"])
        qc.erzeugen(text=qrtext, filename=filename)
        print "Saved QR-Code for student no. " + (str)(student["ID"]) + "."
        

createQRCodesTeilnehmer(getTeilnehmerListeIDName())
