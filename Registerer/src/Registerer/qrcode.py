#!/usr/bin/env python
#-*- coding: UTF-8 -*-
'''
erzeugt QR-Codes: muss dazu ausgedruckt werden
liest QR-Codes
'''
import os, signal, subprocess
import platform as p

def erzeugenRawIn(strfile1="qrcode"):
    text=raw_input("Geben Sie einen Text für den QRCode an: ")
    os.system("qrencode -o "+strfile1+".png '"+text+"'")
    print "QRCode unter: "+strfile1+".png"


def erzeugen(text="", filename="qrcode"):
    """Speichert den in "text" übergebenen Text als QRCode in einem png Bild ab
        "filename" ohne Dateiendung."""
    
    os.system("qrencode -o "+filename+".png '"+text+"'")
    print "QRCode erzeugt. (Datei: "+filename+".png Text: "+text+")"


def lesen():
    sys = p.system()
    zbarcam=subprocess.Popen("zbarcam --raw /dev/video0", stdout=subprocess.PIPE, shell=True)
    print "zbarcam erfolgreich gestartet..."
    while True:
        qrcodetext=zbarcam.stdout.readline()
        if qrcodetext!="":
            print "success"
            print "QR-Code: " + qrcodetext
            if sys=="Windows":
                subprocess.check_output("Taskkill /F /IM zbarcam.exe", shell=True).decode
            else:
                os.killpg(zbarcam.pid, signal.SIGTERM)  # Prozess stoppen
            print "zbarcam erfolgreich gestoppt"
            return qrcodetext