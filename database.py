# This file initializes db and db_cursor in order to control data
# contained in the database

# This file assumes the database Latte is created and all of the
# tables are created as well

# If not, to create database, execute
# CREATE DATABASE Latte;
# Inside cmd folder after logging into mysql

# After that, uncomment the commented part of the code below
# and execute it once

import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="amin",
    password="amin2004",
    database="Latte"
)

db_cursor = db.cursor()

# with open("./static/db/LatteTables.sql", "r") as file:
#     command = file.read()
#     db_cursor.execute(command)