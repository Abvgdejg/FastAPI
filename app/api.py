from fastapi import FastAPI, File, Request
from fastapi.responses import FileResponse, RedirectResponse
import shutil
from fastapi import UploadFile
import lib.mysql_tools as mysql
import random 
import string
import os
from fastapi.templating import Jinja2Templates

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

templates = Jinja2Templates(directory='public')

app = FastAPI(

    title='AnprAPI',
    description="# API Usage " + '\n ### 1) Post image on site \n ### 2) Get "result_link" from JSON \n ### 3) Get "path" from JSON \n #Просмотр фото: /result/id?UI=1',
    version='1.0')
 
@app.get("/")
def root():

    return FileResponse('public/index.html')

@app.post("/")
def postdata(request: Request, image: UploadFile = File(...)):
    uploadid = UploadImage(image)
    print(uploadid)
    print(request.headers)
    return {'status': 'new', 'result_link': f'/result/{uploadid}', 'estime': 'None'}

@app.get('/result/{id}')
def result(id: str, request: Request):
    result = mysql.SelectWithID(int(id))
    if result == 'Error':
        return 'Error'
    path = f'/{result.path}'
    print(request.headers)
    if request.headers.get('accept') == 'application/json':
        return {"status" : result.status, 
            "type" : "ru-1-1", 
            "type_conf" : 0.9,
            "number" : "A001AA77", 
            "number_conf" : 0.87,
            "estimate" : 0,
            'path': path}
    
    return templates.TemplateResponse('result.html', {'request': request, 'img': path})
    

print(__name__)

if __name__ == "api": 
    mysql.init_db()