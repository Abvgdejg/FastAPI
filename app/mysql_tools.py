from mysql.connector import connect, Error
import enum

class Table(enum.Enum):
    UploadedFiles = "UploadedFiles"

def init_db():
    try:
        with connect(
            host='db',
            user='root',
            password='root'
        ) as connection:
            create_db_query = "CREATE DATABASE IF NOT EXISTS ml_test"
            create_table = "CREATE TABLE IF NOT EXISTS UploadedFiles (ID int AUTO_INCREMENT NOT NULL, UploadedName varchar(1000), SavedName varchar(1000), Path varchar(1000), PRIMARY KEY (ID))"
            with connection.cursor() as cursor:
                cursor.execute(create_db_query)
                cursor.execute('USE ml_test')
                cursor.execute(create_table)
    except Error as e:
        print(e)

def add_to_table(image, name, path):
    try:
        with connect(
            host='db',
            user='root',
            password='root', 
            database = 'ml_test'
        ) as connection:
            connection.cursor().execute('USE ml_test')
            connection.cursor().execute(f'INSERT INTO UploadedFiles (UploadedName, SavedName, Path) VALUES ("{image.filename}", "{name}", "{path}")')
            connection.commit()
    except: 
        init_db()
        add_to_table(image, name, path)

def SelectFromTable(tableName, condition = None, column = "*"):

    if condition != None:
        condition = "WHERE " + condition
    else:
        condition = ""

    with connect(
            host='db',
            user='root',
            password='root', 
            database = 'ml_test'
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT {column} FROM {tableName} {condition}")
                for row in cursor:
                    print(row)
                

def GetID(tableName, condition):

    if condition != None:
        condition = "WHERE " + condition
    else:
        condition = ""

    with connect(
            host='db',
            user='root',
            password='root', 
            database = 'ml_test'
        ) as connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT ID FROM {tableName} {condition}")
                for row in cursor:
                    return row[0]