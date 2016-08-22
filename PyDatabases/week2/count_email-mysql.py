#! /usr/bin/env python

"""
count_email.py

"Counting email in a database" assignment from "Using databases with python" coursera course (week 2)

Implementation with MySQL instead of SQlite. 
Convert end database to SQlite for submission with utility from http://stackoverflow.com/questions/3890518/convert-mysql-to-sqlite
"""

import mysql.connector

# open connection using credentials from my mysql config file
conn = mysql.connector.connect(option_files='/Users/rmuraglia/.my.cnf')
cur = conn.cursor()

# create database for this exercise if it doesn't exist
cur.execute('create database if not exists emaildb;')

# select that database
cur.execute('use emaildb;')

# delete 'counts' table if there already is one
cur.execute('drop table if exists counts;')

# create fresh table
cur.execute('create table counts (org text, count integer)')

# ask for a filename to be read
fname = raw_input('Enter file name: ')

# make a filehandler to read the file
fh = open(fname)

# parse each line in the file one by one, sequentially
for line in fh:
    if not line.startswith('From: ') : continue # if the line doesn't start with 'From: ', then move on to the next line
    pieces = line.split() # split line at every space
    email = pieces[1] # second word in line is full email
    org = email.split('@')[1] # just get domain of email
    cur.execute('select count from counts where org = %s ', (org, )) # do a query for the counts for the domain
    row = cur.fetchone() # fetch from mysql cursor to python
    if row is None : # this means there was no entry for this domain in the table yet
        cur.execute('insert into counts (org, count) values (%s, 1)', (org, )) # make new entry in table for this domain with a count of 1
    else : # otherwise increment count number by 1
        cur.execute('update counts set count=count+1 where org = %s', (org, ))

conn.commit() # commit changes to database

# get the top ten most frequently used domains
sqlstr = 'select org, count from counts order by count desc limit 10'
cur.execute(sqlstr)
for row in cur :
    print str(row[0]), row[1]

"""
alternate print
cur.execute('select org, count from counts order by count desc limit 10')
cur.fetchall()
"""

cur.close()
conn.close()

# after this, dump to mysql file with 'mysqldump --databases emaildb > emaildb.mysql'

# then use conversion script from github './mysql2sqlite.sh emaildb.mysql | sqlite3 emaildb.sqlite'





