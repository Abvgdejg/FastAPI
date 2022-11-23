from fastapi import FastAPI, File, Request
from fastapi.responses import FileResponse, RedirectResponse
import shutil
from fastapi import UploadFile
import mysql_tools as mysql
import random 
import string
import os
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="public")

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
    mysql.SelectFromTable(save_name)
    return mysql.GetID(save_name)

app = FastAPI()
 
@app.get("/")
def root(request: Request, status = None, uploadid = None, ptime = None ):
    return templates.TemplateResponse("index.html", {'status': status, 'link': f'/result/{uploadid}', 'ptime': ptime, 'request': request})

@app.post("/")
def postdata(request: Request, image: UploadFile = File(...)):
    uploadid = UploadImage(image)
    # return templates.TemplateResponse("index.html", {'status': 'New', 'link': f'/result/{uploadid}', 'ptime': 'None', 'request': request}, status_code=303)
    return RedirectResponse(f'/?status=New&uploadid={uploadid}&ptime=None', status_code=303)
@app.get('/result/{id}')
def abab(id: str, request: Request):
    result = mysql.SelectWithID(int(id))
    if result == 'Error':
        return 'Error'
    path = f'/{result.path}'

    return templates.TemplateResponse("result.html", {"request": request,'img': path})

print(__name__)

if __name__ == "api": 
    mysql.init_db()