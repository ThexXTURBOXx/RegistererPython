# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 00:25:26 2016

@author: root
"""
import MySQLdb as db
from contextlib import closing

class Database(object):
    
    def __init__(self, dbHost = "localhost", dbName = "teilnehmerWIP",
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


    def __del__(self):
        self.connection.close()
        
        
    def getStudentList(self):
        
        with closing(self.connection.cursor()) as c:
            c.execute("SELECT * FROM teilnehmer;")
            studList = c.fetchall()
            
        return studList
        
        
    def saveCourse(self, attendanceList, archiveTable = "anwesenheitTemp"):
        
        with closing(self.connection.cursor()) as c:
            queryStart = "INSERT INTO " + archiveTable + " ("
            queryEnd = ") VALUES ("
            for student in attendanceList:
                for key in student:
                    queryStart = queryStart + key + ", "
                    queryEnd = queryEnd + student[key] + ", "
            queryEnd = queryEnd + ");"
            query = queryStart + queryEnd
            print query
        
    def execQuery(self, query):
        
        with closing(self.connection.cursor()) as c:
            try:                
                c.execute(query)
            except TypeError:
                raise ExecuteError("Query has to be a string.")
            except db.OperationalError:
                raise ExecuteError("Check Query.")
                

class Course(object):
    
    attendance = []
    
    def __init__(self, ID, title, teacher, date, room):
        self.ID = ID
        self.title = title
        self.teacher = teacher
        self.date = date
        self.room = room
    
    def loginStudent(self, studentID):
        student = {"studentid":studentID, "courseid":self.ID}
        attendance.append(student)
    
    def logoutStudent(self, studentID):
        pass
    
    def getAttendanceList(self):
        return attendance
        
                
                
class ExecuteError(Exception):
    
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)