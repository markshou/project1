import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# engine = create_engine("postgres://oydqwwvmfkwawe:3cb6a5a0d105c929fc4695244b25dfbb1458befabddb2b3c85d254549213b656@ec2-107-21-125-209.compute-1.amazonaws.com:5432/dcmoh597l9rarv")
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)

    # INSERT rows into TABLE "books"
    for isbn, title, author, year in reader:
        if year != "year":
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                       {"isbn": isbn, "title": title, "author": author, "year": year})
            print(f"Added \"{title}\" to database.")
    db.commit()

if __name__ == "__main__":
    main()