# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 00:25:26 2016

@author: root
"""
import MySQLdb as db
import MySQLdb.cursors as dbcursors
from contextlib import closing

class Database(object):
    
    def __init__(self, dbHost = "localhost", dbName = "students",
                 dbUser = "sfz", dbPasswd = "pass1234"):
        self.connection = db.connect(
            host=dbHost,
            db=dbName,
            user=dbUser,
            passwd=dbPasswd,
            cursorclass=dbcursors.DictCursor,
            use_unicode=True,
            charset="utf8"
            )
        self.host = dbHost
        self.name = dbName
        self.user = dbUser


    def __del__(self):
        self.connection.close()
        
        
    def __str__(self):
        infoStr = "MySQL Database\n"
        infoStr += "Name: %s\nHost: %s\nUser: %s\n-----------" % (self.name, self.host, self.user)
        #with closing(self.connection.cursor()) as c:
        #    c.execute("SELECT TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS;")
        #    print c.fetchall()
        return infoStr
        
        
    def getStudentList(self):
        """Returns a list of dicts each containing the information of one student."""
        
        with closing(self.connection.cursor()) as c:
            c.execute("SELECT * FROM student;")
            studList = c.fetchall()
            
        return studList
        
        
    def saveCourse(self, course, archiveTable = "attendance"):
        """Saves a given course to the archiveTable.
        ArchiveTable is 'attendance' per default."""        

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
        """Executes a SQL Query on the Database.
        Raises ExecuteError."""
        
        with closing(self.connection.cursor()) as c:
            try:                
                c.execute(query)
                self.connection.commit()
            except TypeError:
                raise ExecuteError("Query has to be a string.")
            except db.OperationalError:
                raise ExecuteError("Check Query.")
                
    def getDataType(self, tableName, columnName):
        """Returns the SQL-Datatype of the specified column in the database."""
        
        query = "SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE \
                 + TABLE_NAME = '" + tableName + "' AND COLUMN_NAME = '"\
                 + columnName + "';"
        with closing(self.connection.cursor()) as c:
            nbRowsAffected = c.execute(query)
            dtype = c.fetchall()
            if nbRowsAffected == 0:
                raise ExecuteError("The given column does not exist.")
            dtype = dtype[0]["DATA_TYPE"]
            return dtype
            
    def getID(self, table, column, value):
        """Returns the ID of the given value in the specified table and column.
        Returns -1 if value is not found."""
        
        with closing(self.connection.cursor()) as c:
            nbRowsAffected = c.execute("SELECT id FROM %s WHERE %s = '%s';"\
                                        % (table, column, value))
            if nbRowsAffected == 0:
                return -1
            else:
                return c.fetchall()[0]["id"]
                
    def getValue(self, table, ID):
        """Returns a dicts with all values where table.id = ID."""

        with closing(self.connection.cursor()) as c:
            query = "SELECT * FROM %s WHERE %s.id = %d;" % (table, table, ID)
            nbRows = c.execute(query)
            values = c.fetchall()
        if nbRows == 0:
            raise ExecuteError("No entry with the specified ID found.")
        else:            
            return values[0]
        
                
    def newEntry(self, table, entry):
        """Adds entry to table. Entry has to be a dict of the form:
        {"columnName1":"value1", "columnName2":"value2", ...}"""
        
        with closing(self.connection.cursor()) as c:
            queryStart = "INSERT INTO %s (" % table
            queryEnd = ") VALUES ("
            for key in entry:
                queryStart = queryStart + "%s, " % key
                try:           
                    if self.getDataType(table, key) == "int":
                        queryEnd = queryEnd + "%s, " % entry[key]
                    else:
                        queryEnd = queryEnd + "'%s', " % entry[key]        
                except ExecuteError:
                    raise ExecuteError("One or more of the given columns do not exist.")
            queryEnd = queryEnd[:-2] + ");"
            query = queryStart[:-2] + queryEnd
            c.execute(query)
            self.connection.commit()
            

class Course(object):
    
    def __init__(self, ID, title, date, teacher, room):
        """Creates a course of a specified type (ID).
        Date has to be of the form YYYY-MM-DD. title has to be a string,
        teacher and room are IDs."""
        
        self.ID =  ID
        self.date = "'" + date + "'"
        self.title = title
        self.teacher = teacher
        self.room = room
        self.attendance = []
        
    def __str__(self):
        courseInfo = "ID: " + (str)(self.ID) + "\n" + \
            "Teacher: " + (str)(self.teacher) + "\n" + \
            "Title: " + (str)(self.title) + "\n" + \
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
            student.update({"course":self.ID, "date":self.date, "teacher":self.teacher})
        return self.attendance

                
class ExecuteError(Exception):
    
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)