from mysql.connector import connect, Error
from sqlalchemy import create_engine, MetaData, Table, String, Integer, Column, Text, DateTime, Boolean


class Tables():
    class uploadedImagesClass():
        TableTitle = "uploadedImages"

        ID = "id"
        UPLOADEDNAME = "uploadedName"
        SAVEDNAME = "savedName"
        PATH = "path"
        STATUS = 'status'
        PTIME = 'ptime'

    uploadedImages = uploadedImagesClass

connection = None
uploadedImages = None
    

def init_sqlalchemy():
    engine = create_engine("mysql+mysqlconnector://root:root@db:3306/ml_test")
    global connection
    connection = engine.connect()
    print(engine)

    metadata = MetaData()

    global uploadedImages
    uploadedImages = Table(Tables.uploadedImages.TableTitle, metadata, 
    Column(Tables.uploadedImages.ID, Integer(), primary_key=True, autoincrement=True), 
    Column(Tables.uploadedImages.UPLOADEDNAME, String(200)), 
    Column(Tables.uploadedImages.SAVEDNAME, String(200)), 
    Column(Tables.uploadedImages.PATH, String(200)),
    Column(Tables.uploadedImages.STATUS, String(200)), 
    Column(Tables.uploadedImages.PTIME, String(200)),
    )

    metadata.create_all(engine)

def init_db():
    try:
        with connect(
            host='db',
            user='root',
            password='root'
        ) as connection:
            create_db_query = "CREATE DATABASE IF NOT EXISTS ml_test"
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
        init_sqlalchemy()
    except Error as e:
        print(e)

def add_to_table(image, name, path, ptime = 'None'):
    
    insert = uploadedImages.insert().values(
        uploadedName = image.filename,
        savedName = name,
        path = path,
        status = 'new',
        ptime = ptime
    )
    connection.execute(insert)
    

def SelectFromTable(name, id = None, is_return = False):

    if id != None:
        select = uploadedImages.select().where(
        uploadedImages.c.id == id
        )
        result = connection.execute(select)
    
        return result.fetchall()[0]

    select = uploadedImages.select().where(
        uploadedImages.c.savedName == name
    )
    result = connection.execute(select)
    
    if is_return:
        return result
    
    print(result.fetchall())
                
def SelectWithID(id):
    try:
        return SelectFromTable(None, id = id)
    except:
        return 'Error'
def GetID(name):

    result = SelectFromTable(name, is_return = True)
    return result.fetchall()[0].id