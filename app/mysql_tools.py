from mysql.connector import connect, Error
from sqlalchemy import create_engine, MetaData, Table, String, Integer, Column, Text, DateTime, Boolean


class Tables():
    class uploadedImagesClass():
        TableTitle = "uploadedImages"

        ID = "id"
        UPLOADEDNAME = "uploadedName"
        SAVEDNAME = "savedName"
        PATH = "path"

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
    Column(Tables.uploadedImages.PATH, String(200))
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

def add_to_table(image, name, path):
    
    insert = uploadedImages.insert().values(
        uploadedName = image.filename,
        savedName = name,
        path = path
    )
    connection.execute(insert)
    

def SelectFromTable(name, is_return = False):

    select = uploadedImages.select().where(
        uploadedImages.c.savedName == name
    )
    result = connection.execute(select)
    
    if is_return:
        return result
    
    print(result.fetchall())
                

def GetID(name):

    result = SelectFromTable(name, True)
    return result.fetchall()[0][0]