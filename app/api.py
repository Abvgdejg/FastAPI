from fastapi import FastAPI, File, Form
from fastapi.responses import FileResponse
import shutil
from fastapi import UploadFile
import uvicorn
from mysql.connector import connect, Error
import random 
import string
import os

def generate_random_name(image):
    letters = string.ascii_letters

    rand_name = ''.join(random.choice(letters) for i in range(4))
    rand_name2 = ''.join(random.choice(letters) for i in range(4))

    os.makedirs(f"UploadedFiles/{rand_name}/{rand_name2}", exist_ok=True)
    
    tmp_name = image.filename.split(".")[1]
    name = f"{rand_name}{rand_name2}.{tmp_name}"
    path = f"UploadedFiles/{rand_name}/{rand_name2}/{name}"
   
    shutil.copyfileobj(image.file, open(path, 'wb'))
    print(path)

    add_to_table(image, name, path)

def init_db():
    try:
        with connect(
            host='db',
            user='root',
            password='root'
        ) as connection:
            create_db_query = "CREATE DATABASE IF NOT EXISTS ml_test"
            create_table = "CREATE TABLE IF NOT EXISTS UploadedFiles (ID int, UploadedName varchar(1000), SavedName varchar(1000), Path varchar(1000))"
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
                cursor.execute('USE ml_test')
                cursor.execute(create_table)
    except Error as e:
        print(e)

def add_to_table(image, name, path):
    with connect(
        host='db',
        user='root',
        password='root', 
        database = 'ml_test'
    ) as connection:
        connection.cursor().execute('USE ml_test')
        connection.cursor().execute(f'INSERT INTO UploadedFiles (ID, UploadedName, SavedName, Path) VALUES (7, "{image.filename}", "{name}", "{path}")')
        connection.commit()
        
init_db()
app = FastAPI()
 
@app.get("/")
def root():
    return FileResponse("public/index.html")

@app.post("/")
def postdata(text: str = Form(...), image: UploadFile = File(...)):
    generate_random_name(image)
    return {'file_name': image} 