# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 22:50:34 2016

@author: root
"""

import Klassen as k
import qrcode as qc
import datetime
from contextlib import closing

        
def getRoomName(filename = "room.txt"):
    with closing(open(filename)) as fileroomname:
        return fileroomname.readline()

def getRoomID(filename = "room.txt"):
    room = getRoomName(filename)
    roomID = d.getID("room", "room", room)
    return roomID

now = datetime.datetime.now()
d = k.Database()
courseActive = False
currentCourse = None
while True:
    print "Started. Waiting for scan."
    scan = qc.lesen()
    scan = scan.split("_")
    if scan[0] == "course":
        if courseActive:
            d.saveCourse(currentCourse)
        else:
            print "Scanned course no. " + scan[1] + "."
            courseID = scan[1]
            date = now.strftime("%Y-%m-%d")
            room = getRoomID()
            print "Scan teacher now."
            scanTeacher = qc.lesen().split("_")
            while not scanTeacher[0] == "teacher":
                print "No Teacher scanned."
                scanTeacher = qc.lesen().split("_")
            teacher = scanTeacher[1]
            courseTitle = d.getValue("course", courseID)["course"]
            currentCourse = k.Course(courseID, courseTitle, date, teacher, room)
            courseActive = True        
            print "Course logged."
            print currentCourse
    
    elif scan[0] == "student":
        if courseActive:
            currentCourse.loginStudent(scan[1])
        else:
            print "No active course. Scan course first."
        
    elif scan[0] == "ctrl":
        pass
    else:
        print "No active course. Scan course first."
        
