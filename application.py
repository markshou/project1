import os
import re
import requests

from flask import Flask, session, render_template, request, flash, jsonify, redirect, abort
from flask_session import Session
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from bs4 import BeautifulSoup


app = Flask(__name__)
bcrypt = Bcrypt(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
""" engine = create_engine("postgres://oydqwwvmfkwawe:3cb6a5a0d105c929fc4695244b25dfbb1458befabddb2b3c85d254549213b656@ec2-107-21-125-209.compute-1.amazonaws.com:5432/dcmoh597l9rarv") """
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html", message="Please register a new username & password")

@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("username")
    password = request.form.get("password")

    user = db.execute("SELECT * FROM accounts WHERE username = :username", {"username": username}).fetchone()

    if user is not None:
        if bcrypt.check_password_hash(user['password'], password) is True:
            session["user_id"] = user['id']
            session["username"] = user['username']
            return render_template("search.html")

    return render_template("index.html", message="Invalid Username/Password")

"""     if user is None:
        return render_template("index.html", message="Invalid Username/Password")
    else:
        session["user_id"] = user['id']
        session["username"] = user['username']
        return render_template("search.html")
 """
@app.route("/logout")
def logout():

    session.pop('username', None)
    session.pop('user_id', None)

    return render_template("index.html", message="User logged out. Please sign back in.")

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")
    passw_encrypted = bcrypt.generate_password_hash(password).decode('utf-8')

    if (username is None) or (password is None) or (username == "") or (password is ""):
        return render_template("register.html", message="Please enter a username and password")
    elif not username.isalnum() or not len(username) >= 6 or not len(username) <= 30:
        return render_template("register.html", message="Username must be alphanumeric AND between 6 and 30 characters")
    elif db.execute("SELECT * FROM accounts WHERE username = :username", {"username": username}).fetchone() is None:
        db.execute("INSERT INTO accounts (username, password) VALUES (:username, :password)", {"username": username, "password": passw_encrypted})
        db.commit()
        return render_template("index.html", message="New user registered. Please sign in below.")
    else:
        return render_template("register.html", message="Username already exists. Please choose another.")

@app.route("/search", methods=["POST"])
def search():
    if 'username' not in session:
        return redirect(url_for('login'))

    message=""
    query = request.form.get("searchbox")
    queryLIKE = '%' + query.lower() + '%'
    results = db.execute("SELECT * FROM books WHERE lower(title) LIKE :q OR isbn LIKE :q OR lower(author) LIKE :q", {"q": queryLIKE}).fetchall()

    if len(results) < 1:
        message = "no books found for " + '"' + query + '"'

    return render_template("search.html", results=results, message=message, query=query)

@app.route("/books/<string:isbn>", methods=["GET", "POST"])
def book(isbn):
    if 'username' not in session:
        return redirect(url_for('login'))

    comment_error = ""
    if request.method == "POST":
        if db.execute("SELECT * from reviews WHERE acc_id = :username AND book_id = :isbn", {"username": session["username"], "isbn": isbn}).fetchone() is None:
            comment_error = ""
            comment = request.form.get("comment")
            my_rating = request.form.get("rating")
            book = db.execute("INSERT INTO reviews (acc_id, book_id, comment, rating) VALUES (:a, :b, :c, :r)", {"a": session['username'], "b": isbn, "c": comment, "r": my_rating})
            db.commit()
        elif db.execute("SELECT * from reviews WHERE acc_id = :username AND book_id = :isbn", {"username": session["username"], "isbn": isbn}).fetchone() is not None:
            comment_error = "You've already submitted a review (only 1 allowed)."
        else:
            pass

    book = db.execute("SELECT * FROM books WHERE isbn = :q", {"q": isbn}).fetchone()
    # reviews = db.execute("SELECT * FROM reviews WHERE book_id = :q1", {"q1": isbn}).fetchall()
    reviews = db.execute("SELECT acc_id, rating, comment, to_char((date), 'Mon DD, YYYY HH12:MI AM') AS date2 FROM reviews WHERE book_id = :q1", {"q1": isbn}).fetchall()

    reviewtime = db.execute("SELECT acc_id, to_char((date), 'Mon DD, YYYY HH12:MI AM') AS date2 FROM reviews WHERE book_id = :q1", {"q1": isbn}).fetchall()

    # Good Reads Rating
    response = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "r1E4UhH6xREe17fpAqAu1g", "isbns": isbn})
    data = response.json()
    gr_rating = (data['books'][0]['average_rating'])
    gr_rating_pct = "{0:.0%}".format(float(gr_rating)/5.0)
    gr_ratingcount = (data['books'][0]['work_ratings_count'])
    gr_ratingcountcommas = "{:,}".format(gr_ratingcount)

    # Good Reads Book Blurb
    xml_page = requests.get("https://www.goodreads.com/book/isbn/", params={"key": "r1E4UhH6xREe17fpAqAu1g", "isbn": isbn})
    soup = BeautifulSoup(xml_page.text, features='lxml')
    description = soup.find_all('description')[0]
    blurb = description.get_text()

    return render_template("book.html", book_info=book, reviews=reviews, reviewtime=reviewtime, gr_rating_pct=gr_rating_pct, rating=gr_rating, rcount=gr_ratingcountcommas, blurb=blurb, comment_error=comment_error)

@app.route("/api/<string:isbn>", methods=["GET", "POST"])
def bookapi(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    reviews = db.execute("SELECT COUNT(comment) FROM reviews WHERE book_id = :isbn", {"isbn": isbn}).fetchone()
    avg_rating = db.execute("SELECT AVG(rating) FROM reviews WHERE book_id = :isbn", {"isbn": isbn}).fetchone()

    if not book:
        abort(404)

    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn,
        "review_count": reviews.count,
        "average_score": avg_rating.avg
    })

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", err_type="404", message="Page Not Found")
