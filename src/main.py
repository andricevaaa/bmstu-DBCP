from homepage import *
import psycopg2

connection = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="guest",
    password="guest"
)
username = ""
first_hp(connection, username)

connection.close()