# This file initializes db and db_cursor in order to control data
# contained in the database

import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="amin",
  password="amin2004"
)

db_cursor = db.cursor()