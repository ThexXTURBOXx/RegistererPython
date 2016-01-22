#!/usr/bin/env python
#-*- coding: UTF-8 -*-
'''
erzeugt QR-Codes: muss dazu ausgedruckt werden
liest QR-Codes
'''
import os, signal, subprocess
strfile1 = "qrcode"
def erzeugen():
    text=raw_input("Geben Sie einen Text für den QRCode an: ")
    os.system("qrencode -o "+strfile1+".png '"+text+"'")
    print "QRCode unter: "+strfile1+".png"
def lesen():
    zbarcam=subprocess.Popen("zbarcam --raw /dev/video0", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    print "zbarcam erfolgreich gestartet..."
    while True:
        qrcodetext=zbarcam.stdout.readline()
        if qrcodetext!="":
            print "success"
            break
    os.killpg(zbarcam.pid, signal.SIGTERM)  # Prozess stoppen
    print "zbarcam erfolgreich gestoppt"
    return qrcodetext