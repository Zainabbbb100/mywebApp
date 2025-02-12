from flask import *
import MySQLdb

app = Flask(__name__)
app.secret_key = "secret"

def get_db_connection():
    """Create a new database connection for each request"""
    return MySQLdb.connect(
        host="localhost",
        user="root",  
        passwd="password",  
        db="movies_db"
    )

@app.route("/")
def index():
    return render_template('index.html')

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

        if movie is None:
            print("Movie not found")  
            return render_template("movies.html", movie=None)  

        print(movie) 
        return render_template("movies.html", movie=movie)

    return render_template("search_movie.html")



@app.route("/list_movies")
def list_movies():
    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute("select * from movies")  
        movies = cursor.fetchall()  
    db.close()

    print(movies)  

    return render_template("list_movies.html", movies=movies)


if __name__ == "__main__":
    app.run(debug=True)
