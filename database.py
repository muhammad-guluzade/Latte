import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="amin",
  password="amin2004"
)

db_cursor = db.cursor()