import mysql.connector as conn

mydb = None
mycursor = None

def initialse():
    global mydb
    mydb = conn.connect(host='localhost', user='root', password='', database='project')
    global mycursor
    mycursor = mydb.cursor()