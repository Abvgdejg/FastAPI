from fastapi import FastAPI, File, Form
from fastapi.responses import FileResponse
import shutil
from fastapi import UploadFile
import mysql_tools as mysql
import random 
import string
import os

def UploadImage(image):
    letters = string.ascii_letters

    first_name_part = ''.join(random.choice(letters) for i in range(4))
    second_name_part = ''.join(random.choice(letters) for i in range(4))
    base_directory = "UploadedFiles"
    base_path = f"{base_directory}/{first_name_part}/{second_name_part}"
    uploaded_extension = image.filename.split(".")[1]

    os.makedirs(base_path, exist_ok=True)
    
    save_name = f"{first_name_part}{second_name_part}.{uploaded_extension}"

    save_path = f"{base_path}/{save_name}"
   
    shutil.copyfileobj(image.file, open(save_path, 'wb'))

    mysql.add_to_table(image, save_name, save_path)
    mysql.SelectFromTable(mysql.Table.UploadedFiles.value, f"SavedName = '{save_name}'")
    print(mysql.GetID(mysql.Table.UploadedFiles.value, f"SavedName = '{save_name}'"))

app = FastAPI()
 
@app.get("/")
def root():
    return FileResponse("public/index.html")

@app.post("/")
def postdata(image: UploadFile = File(...)):
    UploadImage(image)
    return FileResponse("public/index.html")
    

if __name__ == "api": 
    mysql.init_db()