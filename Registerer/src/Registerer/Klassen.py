# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 00:25:26 2016

@author: root
"""
import MySQLdb as db
from contextlib import closing

class Database(object):
    
    def __init__(self, dbHost = "localhost", dbName = "students",
                 dbUser = "sfz", dbPasswd = "pass1234"):
        self.connection = db.connect(
            host=dbHost,
            db=dbName,
            user=dbUser,
            passwd=dbPasswd,
            cursorclass=db.cursors.DictCursor,
            use_unicode=True,
            charset="utf8"
            )
        self.host = dbHost
        self.name = dbName
        self.user = dbUser


    def __del__(self):
        self.connection.close()
        
        
    def getStudentList(self):
        
        with closing(self.connection.cursor()) as c:
            c.execute("SELECT * FROM student;")
            studList = c.fetchall()
            
        return studList
        
        
    def saveCourse(self, course, archiveTable = "attendance"):                  #todo: letztes ", " bei queryStart und queryEnd löschen
        
        with closing(self.connection.cursor()) as c:
            for student in course.getAttendanceList():
                queryStart = "INSERT INTO " + archiveTable + " ("
                queryEnd = ") VALUES ("
                for key in student:
                    queryStart = queryStart + key + ", "
                    queryEnd = queryEnd + (str)(student[key]) + ", "
                queryEnd = queryEnd[:-2] + ");"
                query = queryStart[:-2] + queryEnd
                c.execute(query)
                self.connection.commit()

        
    def execQuery(self, query):
        
        with closing(self.connection.cursor()) as c:
            try:                
                c.execute(query)
            except TypeError:
                raise ExecuteError("Query has to be a string.")
            except db.OperationalError:
                raise ExecuteError("Check Query.")
                
    def getDataType(self, tableName, columnName):
        query = "SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE \
                 + TABLE_NAME = '" + tableName + "' AND COLUMN_NAME = '"\
                 + columnName + "';"
        with closing(self.connection.cursor()) as c:
            c.execute(query)
            return c.fetchall()

class Course(object):
    
    def __init__(self, ID, title, teacher, date, room):
        self.ID = ID
        self.title = title
        self.teacher = teacher
        self.date = "'" + date + "'"
        self.room = room
        self.attendance = []
        
    def __str__(self):
        courseInfo = "ID: " + (str)(self.ID) + "\n" + \
            "Title: " + (str)(self.title) + "\n" + \
            "Teacher: " + (str)(self.teacher) + "\n" + \
            "Date: " + (str)(self.date) + "\n" + \
            "Room: " + (str)(self.room) + "\n"
        courseInfo += "--------\n"
        for student in self.attendance:
            courseInfo += "Student: " + (str)(student["student"]) + "\n"
        return courseInfo
    
    def loginStudent(self, studentID):
        student = {"student":studentID}
        self.attendance.append(student)
    
    def logoutStudent(self, studentID):
        self.checkForDuplicates()
        self.attendance.remove({"student":studentID})
    
    def checkForDuplicates(self, deleteDuplicates = True):                      #Zu verbessern (zB Bubblesort)
        """Nonperformant but only small numbers"""
        duplicateEntries = []
        for stud1 in range(len(self.attendance)-1):                             #Warum muss hier ein -1 hin?
            idTemp = self.attendance[stud1]["student"]
            for stud2 in range(stud1 + 1, len(self.attendance)):
                if idTemp == self.attendance[stud2]["student"]:
                    if deleteDuplicates:
                        duplicateEntries.append(self.attendance.pop(stud2))
                    else:
                        duplicateEntries.append(self.attendance[stud2]["student"])
        return duplicateEntries
    
    def getAttendanceList(self):
        for student in self.attendance:
            student.update({"course":self.ID, "date":self.date})
        return self.attendance
        

                
class ExecuteError(Exception):
    
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)