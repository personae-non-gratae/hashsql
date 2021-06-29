#!/usr/bin/python3

import MySQLdb
import csv
import bcrypt
import json
import sys

if len(sys.argv) != 4:
    print("Usage: ./hashsql.py <username> <password> <database>")
    sys.exit(1)

def exception_handler(x):
    template = "An exception of type {0} occured. Arguements:\n{1!r}"
    message = template.format(type(x).__name__, x.args)
    print(message)
    exit(1)

try:
    dbConnect = MySQLdb.connect(host='localhost', user=sys.argv[1], passwd=sys.argv[2], db=sys.argv[3])
    cursor = dbConnect.cursor()
except Exception as ex:
    exception_handler(ex)

def csv_to_list():
    #Takes a csv file as input, returns the data as a list
    print("enter file name: ")
    file_name = input()

    try:
        with open(file_name, newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
        f.close()
    except Exception as ex:
        exception_handler(ex)
    
    return data

def generate_hash():
    #Create hashes for data in the second field of each list item
    #Upload hashes along with an ID to mysql.
    data = csv_to_list()
    sql = "INSERT INTO users (email, password) VALUES (%s, %s)"
    try:
        for item in data:
            ID = item[0]
            to_hash = item[1]
            x = bcrypt.hashpw(to_hash.encode(), bcrypt.gensalt())
            val = (ID, x.decode())
            cursor.execute(sql, val)
            dbConnect.commit()
            print(cursor.rowcount, "record inserted")
    except Exception as ex:
        exception_handler(ex)

def check_hash():
    #user enters UserID and password string, query database, pull password hash
    #check password hash against entered string, return something if true / false

    print('please enter password')
    password = input().encode()

    f = open('secret.txt', 'r')
    myHash = f.read()
    myHash = myHash.rstrip('\n')
    myHash = myHash.encode()
    
    if bcrypt.checkpw(password, myHash):
        print('access granted')
        sql_connect(password.decode())
    else:
        print('access denied')
 

generate_hash()
