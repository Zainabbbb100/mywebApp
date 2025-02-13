from flask import *
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb

app = Flask(__name__)
app.secret_key = "secret"

# Creates a database connection
def get_db_connection():
    return MySQLdb.connect(
        host="192.168.1.223",  
        user="user",  
        passwd="password", 
        db="movies_db",  
        port=3306  
    )

# Home Page (Main Landing Page)
@app.route("/")
def index():
    return render_template("index.html")

# Route to Add a Movie
@app.route("/add_movie", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        movie_name = request.form.get("movie_name")
        description = request.form.get("description")

        db = get_db_connection()
        with db.cursor() as cursor:
            sql = "INSERT INTO movies (name, description) VALUES (%s, %s)"
            cursor.execute(sql, (movie_name, description))
            db.commit()
        db.close()

        return redirect(url_for("list_movies"))

    return render_template("add_movie.html")

# Search Movie Route
@app.route("/search_movie", methods=["GET", "POST"])
def search_movie():
    if request.method == "POST":
        movie_name = request.form.get("movie_name")

        db = get_db_connection()
        with db.cursor() as cursor:
            sql = "SELECT * FROM movies WHERE name = %s"
            cursor.execute(sql, (movie_name,))
            movie = cursor.fetchone()
        db.close()

        return render_template("movie_details.html", movie=movie)

    return render_template("search_movie.html")

# List All Movies Route
@app.route("/list_movies")
def list_movies():
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM movies")
        movies = cursor.fetchall()
    db.close()

    return render_template("list_movies.html", movies=movies)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')