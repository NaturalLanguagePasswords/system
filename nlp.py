#!/usr/bin/python3

# Version 1
# This utility connects to a Natural Language Passwords database.
# Since the database doe not have a cryptographically secure random number generator, passwords generated by this script are inferior to those selected by dice.
# Sorry for the ugly code; I'm not a python programmer.


# Configuration ################################################################

DEBUG = 0
DEBUGENTROPY = 0

# Adjust connection parameters for your system.
DB_SERVER_ADDRESS = 'localhost'
DB_DATABASE = 'nlp'
DB_USER = 'user'
DB_PASSWORD = 'password'

################################################################################


import pymysql
import sys

global list
list = 'no'
wordpairs = 2

# Check command line arguments
if len(sys.argv) == 1:
  print( sys.argv[0] + " [1,2,3,4,adjectives,nouns]")
  quit() 
elif sys.argv[1] == '1':
  wordpairs = 1 
elif sys.argv[1] == '2':
  wordpairs = 2
elif sys.argv[1] == '3': 
  wordpairs = 3
elif sys.argv[1] == '4': 
  wordpairs = 4 
elif sys.argv[1] == 'adjectives': 
  wordpairs = 1 
  list = 'adjectives'
elif sys.argv[1] == 'nouns': 
  wordpairs = 1 
  list = 'nouns'
else:
  print( sys.argv[0] + " [1,2,3,4,adjectives,nouns]")
  quit()

# Open database connection
db = pymysql.connect(DB_SERVER_ADDRESS,DB_USER,DB_PASSWORD,DB_DATABASE)

# Prepare a cursor object using cursor() method
cursor = db.cursor()

# Generate temporary tables that are lists of words, one table for each word type.
# The first table is of adjectives, and the second table is of nouns.
if (DEBUG):
  print ("Create the database tables.") 

for i in range(1, (2 * wordpairs) + 1):
  if (i % 2) == 1:
    sql = "CREATE TEMPORARY TABLE t" + str(i) + " AS (SELECT word FROM wordlist WHERE adjective=1 ORDER BY LENGTH(word), RAND()) LIMIT 1296"
  else:
    sql = "CREATE TEMPORARY TABLE t" + str(i) + " AS (SELECT word FROM wordlist WHERE noun=1 ORDER BY LENGTH(word), RAND()) LIMIT 7776"
  if (DEBUG):
    print(sql)
  cursor.execute(sql)

# Make sure there are enough adjectives.
sql = "SELECT COUNT(*) FROM t1"
if (DEBUG):
  print(sql)
count = db.cursor()
count.execute(sql)
numberofrows = count.fetchone()
if (numberofrows[0] != 1296):
  print("Only " + str(numberofrows[0]) + " adjectives available.")
  quit()

# Make sure there are enough nouns.  
sql = "SELECT COUNT(*) FROM t2"
if (DEBUG):
  print(sql)
count = db.cursor()
count.execute(sql)
numberofrows = count.fetchone()
if (numberofrows[0] != 7776):
  print("Only " + str(numberofrows[0]) + " nouns available.")
  quit()
  

if (DEBUG):
  print ("Finished creating the database tables.\n") 

# Calculate the entropy of the password selection method
if (DEBUGENTROPY):
  sql = ''
  for i in range(1, (2 * wordpairs) + 1):
    if (len(sql) == 0):
      sql = "SELECT ROUND(LOG2((SELECT COUNT(*) FROM t" + str(i) + "))"
    else:
      sql = sql + " + LOG2((SELECT COUNT(*) FROM t" + str(i) + "))"
      
  sql = sql + ", 2) AS entropy"
  if (DEBUG):
    print(sql)
  cursor.execute(sql)
  data = cursor.fetchone()
  print("Password entropy: %s\n" % data)

# Decide to print a list of words or an actual password
if (list == 'adjectives' or list == 'nouns'):
  if (list == 'adjectives'):
    if (DEBUG):
      print("Printing list of adjectives.\n")
    sql = "SELECT word FROM t1 ORDER BY RAND() LIMIT 1296"
    sqlrolls = "SELECT roll FROM dice WHERE LENGTH(roll) = '4'"
  else:
    if (DEBUG):
      print("Printing list of nouns.\n")
    sql = "SELECT word FROM t2 ORDER BY RAND() LIMIT 7776"
    sqlrolls = "SELECT roll FROM dice WHERE LENGTH(roll) = '5'"
  cursor.execute(sql)
  row = cursor.fetchone()

  # Also get the dice rolls
  rolls = db.cursor()
  rolls.execute(sqlrolls)
  roll = rolls.fetchone()


  while row is not None:
    print("%s " % roll + "%s" % row)
    row = cursor.fetchone()
    roll = rolls.fetchone()
else:
  password = ''

  if (DEBUG):
    print ("Select words to form a password.") 

  for n in range(1, 6):
    password = ''
    # Repeatedly select words from the tables.
    for t in range(1, (2 * wordpairs) + 1):
      sql = "SELECT word FROM t" + str(t) + " ORDER BY RAND() LIMIT 1"
      if (DEBUG):
        print(sql)
      cursor.execute(sql)
      data = cursor.fetchone()
      if (len(password) == 0):
        password = data[0]
      else:
        password = password + " " + data[0]
    print(password)

  if (DEBUG):
    print ("Finished selecting words.\n") 

# disconnect from database
db.close()
