#! /usr/bin/env python

"""
roster-mysql.py

"Many students in many courses" assignment from "Using databases with python" coursera course (week 4)

Goal: create db from JSON file with a junction table

Implementation with MySQL instead of SQLite.
"""

import mysql.connector
from subprocess import call
import json
from pprint import pprint

# create database and tables for this exercise
cnx = mysql.connector.connect(option_files='/Users/rmuraglia/.my.cnf')
cur = cnx.cursor()

cur.execute('create database if not exists rosterdb;')
cur.execute('use rosterdb;')

# pull in SQL commands from external file
call('mysql rosterdb < rosterdb.mysql', shell=True)

# read json file
filename = 'roster_data.json'
with open(filename) as f :
    json_data = json.load(f)

# optional
# pprint(json_data[0:5]) # look at some of the json data
# len(json_data) # see how many entries there are
# type(json_data) # see that it has been parsed into a list

# add entries to db
for entry in json_data :
    name = entry[0]
    title = entry[1]
    role = entry[2]

    # add student name and course title if not already in db
    cur.execute('insert ignore into user (name) values (%s);', (name, ))
    cur.execute('insert ignore into course (title) values (%s);', (title, ))

    # get unique IDs for student name and course titles for junction table
    cur.execute('select id from user where name = %s ;', (name, ))
    user_id = cur.fetchone()[0]
    cur.execute('select id from course where title = %s ;', (title, ))
    course_id = cur.fetchone()[0]

    # insert data to junction table
    cur.execute('replace into member (user_id, course_id, role) values (%s, %s, %s);', (user_id, course_id, role))

cnx.commit()

cur.execute('select hex(concat(user.name, course.title, member.role)) as x from user join member join course on user.id = member.user_id and member.course_id = course.id order by x limit 1;')
cur.fetchone()
