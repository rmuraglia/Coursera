#! /usr/bin/env python

"""
trackdb.py

"Multi-table database - tracks" assignment from "Using databses with python" coursera course (week 3)

Goal: create db from xml file and show results from test query

Implementation with MySQL instead of SQlite.
Convert end database to SQlite for submission with utility from 
http://stackoverflow.com/questions/3890518/convert-mysql-to-sqlite
https://github.com/dumblob/mysql2sqlite
"""

import mysql.connector
import xml.etree.ElementTree as ET
from subprocess import call

# create database and tables for this exercise
cnx = mysql.connector.connect(option_files='/Users/rmuraglia/.my.cnf')
cur = cnx.cursor()

cur.execute('create database if not exists trackdb;')
cur.execute('use trackdb;')

# pull in SQL commands from external file
call('mysql trackdb < trackdb.mysql', shell=True) # source trackdb.sql, use on trackdb

"""
alternate version: more system independent, probably safer to get around shell issues

for line in open('trackdb-oneline.mysql'):
    cur.execute(line)

issues with this version: cannot deal with blank lines, all commands must be contained on a single line. (cannot break up create table into lines for readability)

solution from http://stackoverflow.com/questions/4408714/execute-sql-file-with-python-mysqldb

import re
def exec_sql_file(cursor, sql_file):
    print "\n[INFO] Executing SQL script file: '%s'" % (sql_file)
    statement = ""

    for line in open(sql_file):
        if re.match(r'--', line):  # ignore sql comment lines
            continue
        if not re.search(r'[^-;]+;', line):  # keep appending lines that don't end in ';'
            statement = statement + line
        else:  # when you get a line ending in ';' then exec statement and reset for next statement
            statement = statement + line
            #print "\n\n[DEBUG] Executing SQL statement:\n%s" % (statement)
            try:
                cursor.execute(statement)
            except (OperationalError, ProgrammingError) as e:
                print "\n[WARN] MySQLError during execute statement \n\tArgs: '%s'" % (str(e.args))

            statement = ""

function cleans up text input to skip comment lines (starts with '--'), and glues together lines until a statement ends with ';' 
""" 

filename = 'Library.xml'

# looking at structure of XML file, we see that the information of interest is contained in the third layer 'dict' field
# structure of data: there are alternating <key> tags whose text denotes what the next element represents
# ex: <key>Artist</key><string>Queen</string> <key>Composer</key>...

tree = ET.parse(filename)
root = tree.getroot()
trackdata = root.findall('dict/dict/dict')
print 'Total number of tracks:', len(trackdata)

# look for the 'field' data in the song dictionary 'd'
def lookup(d, field) :
    found = False
    for child in d : # iterate through child nodes of song dictionary
        if found : # (2) once condition (1) has been met, the next element will contain the text we desire
            return child.text
        if child.tag == 'key' and child.text == field : # (1) search for the element of type 'key' corresponding to the 'field' we are querying for
            found = True
    return None

for track in trackdata :
    if ( lookup(track, 'Track ID') is None ) : continue # skip poorly defined entries with no track id

    name = lookup(track, 'Name')
    artist = lookup(track, 'Artist')
    album = lookup(track, 'Album')
    count = lookup(track, 'Play Count')
    rating = lookup(track, 'Rating')
    length = lookup(track, 'Total Time')
    genre = lookup(track, 'Genre')

    if None in [name, artist, album, genre] : continue # skip tracks missing a required field

    # if passes all checks, add to database
    cur.execute('insert ignore into artist (name) values (%s)', (artist, )) # if doesn't violate unique, add. otherwise ignore
    cur.execute('select id from artist where name = %s', (artist, )) # get artist id
    artist_id = cur.fetchone()[0]

    cur.execute('insert ignore into album (title, artist_id) values (%s, %s)', (album, artist_id))
    cur.execute('select id from album where title = %s', (album, ))
    album_id = cur.fetchone()[0]

    cur.execute('insert ignore into genre (genre) values (%s)', (genre, ))
    cur.execute('select id from genre where genre = %s', (genre, ))
    genre_id = cur.fetchone()[0]

    cur.execute('replace into track (title, album_id, genre_id, len, rating, count) values (%s, %s, %s, %s, %s, %s)', (name, album_id, genre_id, length, rating, count))

    cnx.commit()

cur.execute('select track.title, artist.name, album.title, genre.genre from track join genre join album join artist on track.genre_id = genre.id and track.album_id = album.id and album.artist_id = artist.id order by artist.name, track.title limit 3')
cur.fetchall()

cur.close()
cnx.close()

