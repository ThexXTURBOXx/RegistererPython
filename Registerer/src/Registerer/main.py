#!/usr/bin/env python
#-*- coding: UTF-8 -*-
'''
Hauptprogramm
'''
import qrcode
while (True):
    print "1: qrcode erstellen"
    print "2: qrcode anzeigen"
    print "3: exit"
    select=int(raw_input("Treffen Sie eine Auswahl: "))
    if select == 1:
        qrcode.erzeugenRawIn()
    elif select == 2:
        result=qrcode.lesen().strip()
        print result
    elif select == 3:
        print "beende Programm..."
        break