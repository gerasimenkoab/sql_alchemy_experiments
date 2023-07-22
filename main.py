import sqlalchemy
from sqlalchemy import create_engine  # basic object for DB interaction
from sqlalchemy import URL # url automated generation
from sqlalchemy import text # construct for text SQL commands
from werkzeug.security import generate_password_hash
from names_generator import generate_name 
from password_generator import PasswordGenerator


passGen = PasswordGenerator()

numUsers = 10

db_url = URL.create(drivername = "sqlite",
                        database = "exp.db")
print("Database URL: ",db_url)

engine = create_engine(db_url,echo = True)

with engine.connect() as conn:

    if conn.dialect.has_table(conn,"users"):
        conn.execute(text("drop table users"))

    try:
        conn.execute(text( "CREATE TABLE users (id int primary_key, \
                        username varchar(64), \
                        aboutme varchar(256),\
                        email varchar(128),\
                        password varchar(128))"))
    except Exception as e:
        print(str(e))

    for i in range(numUsers):
        max_id = conn.execute(text("select max(id) as maxId from users"))
        # max_id contain one row. Execute() returns CursorResult object and Cursor.Result.all() returns list of all rows
        try:
            new_id = max_id.scalar_one()+1
        except:
            new_id = 0
        conn.execute(text("INSERT INTO users(id,username,aboutme,email,password)\
                                VALUES (:id,:username,:aboutme,:email,:password)"),\
                                [{"id" : new_id,"username": generate_name(),"aboutme":'goodguy', \
                                "email":'ggog@mail.ru',"password":generate_password_hash(passGen.generate())}])
    conn.commit()
    result = conn.execute(text("select id,username,password from users"))
    print(result.all())

