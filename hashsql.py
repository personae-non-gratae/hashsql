#!/usr/bin/python3

import MySQLdb
import csv
import bcrypt
import json
import sys

if len(sys.argv) != 4:
    print("Usage: ./hashsql.py <username> <password> <database>")
    sys.exit(1)

dbConnect = MySQLdb.connect(host='localhost', user=sys.argv[1], passwd=sys.argv[2], db=sys.argv[3])

cursor = dbConnect.cursor()

def csv_to_list():
    print("enter file name: ")
    file_name = input()

    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    f.close()

    return data

def generate_hash():
    data = csv_to_list()

    for item in data:
        ID = item[0]
        to_hash = item[1]
        x = bcrypt.hashpw(to_hash.encode(), bcrypt.gensalt())

        
        #print(ID)
        #print(x)

def check_hash():
    #user enters UserID and password string, query database, pull password hash
    #check password hash against entered string, return something if true / false

    print('please enter password')
    password = input().encode()

    f = open('secret.txt', 'r')
    myHash = f.read()
    myHash = myHash.rstrip('\n')
    myHash = myHash.encode()

    #print(myHash)
    

    if bcrypt.checkpw(password, myHash):
        print('access granted')
        sql_connect(password.decode())
    else:
        print('access denied')
 

generate_hash()


