import mysql.connector

mycon = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="1234",
    database="xiia"
)

if mycon.is_connected():
    print("Successfully connected")
