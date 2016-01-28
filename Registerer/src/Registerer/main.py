#!/usr/bin/env python
#-*- coding: UTF-8 -*-
'''
Hauptprogramm
'''
import qrcode as qc
import dbTools as dbt
import Klassen as k

d = k.Database()
c = k.Course(5, "test", "testteacher", "2015-05-22", "R001")
c.loginStudent(5)
c.loginStudent(10)
c.loginStudent(30)
c.loginStudent(30)
print c
c.checkForDuplicates()
print c
c.logoutStudent(5)
print c
d.saveCourse(c)