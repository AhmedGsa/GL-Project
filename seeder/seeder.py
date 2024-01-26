import mysql.connector
from dotenv import load_dotenv
import os
import json

f = open("index.json", "r")


data = json.load(f)
# print(data)

load_dotenv()
mydb = mysql.connector.connect(
  host=os.getenv("DB_HOST"),
  user=os.getenv("DB_USERNAME"),
  password=os.getenv("DB_PASSWORD"),
  database=os.getenv("DB_NAME"),
  port=os.getenv("DB_PORT")
)

availabilities = [
    {
        "start": "08:00",
        "end": "10:00"
    },
    {
        "start": "10:00",
        "end": "12:00"
    },
    {
        "start": "13:00",
        "end": "15:00"
    },
    {
        "start": "15:00",
        "end": "17:00"
    }
]
 
mycursor = mydb.cursor()
 
sql = "INSERT INTO availability (start, end) VALUES (%s, %s)"

for availability in availabilities:
    val = (availability["start"], availability["end"])
    mycursor.execute(sql, val)
    mydb.commit()

for item in data:
    sql = "INSERT INTO user (nom, prenom, email, password, role, isGoogleUser) VALUES (%s, %s, %s, \"$2b$12$QtJx.my/zVE1DEM9ZFz83eop5EyJEIt0rzu0BF9WRrEKYY27BNDq.\", \"avocat\", 0)"
    val = (item["name"], item["fname"], item["email"])
    mycursor.execute(sql, val)
    mydb.commit()
    sql = "INSERT INTO avocat (address, wilaya, phoneNumber, facebookUrl, description, categories, rate, imageUrl, longitude, latitude, userId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (item["address"], item["wilaya"], item["phone"], item["social"], item["description"], json.dumps(item["categories"]), item["rating"], item["avocat_image"], item["longitude"], item["latitude"], mycursor.lastrowid)
    mycursor.execute(sql, val)
    mydb.commit()