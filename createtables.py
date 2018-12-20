import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():

    # CREATE TABLE "users"
    db.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR NOT NULL, password VARCHAR NOT NULL);")
    print("create table users")
    db.commit()

    # CREATE TABLE "books"
    db.execute("CREATE TABLE books (id SERIAL PRIMARY KEY, isbn VARCHAR NOT NULL, title VARCHAR NOT NULL, \
                author VARCHAR NOT NULL, year INTEGER NOT NULL);")
    print("create table books")
    db.commit()

if __name__ == "__main__":
    main()