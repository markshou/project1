DROP TABLE IF EXISTS "accounts" CASCADE;
DROP SEQUENCE IF EXISTS accounts_id_seq CASCADE;

CREATE TABLE "accounts" (
    "id" SERIAL NOT NULL,
    "username" VARCHAR PRIMARY KEY NOT NULL,
    "password" VARCHAR NOT NULL,
)

DROP TABLE IF EXISTS "books" CASCADE;
DROP SEQUENCE IF EXISTS books_id_seq CASCADE;

CREATE TABLE "books" (
    "id" SERIAL NOT NULL,
    "isbn" VARCHAR  PRIMARY KEY NOT NULL,
    "title" VARCHAR NOT NULL,
    "author" VARCHAR NOT NULL,
    "year" INTEGER NOT NULL,
)

DROP TABLE IF EXISTS "reviews" CASCADE;
DROP SEQUENCE IF EXISTS reviews_id_seq CASCADE;

CREATE TABLE "reviews" (
    "id" SERIAL PRIMARY KEY NOT NULL,
    "acc_id" VARCHAR NOT NULL,
    "book_id" VARCHAR NOT NULL,
    "comment" VARCHAR NOT NULL,
    "rating" FLOAT NOT NULL,
    "date" timestamp DEFAULT now() NOT NULL,
)