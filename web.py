from flask import *
import MySQLdb

app = Flask(__name__)
app.secret_key = "secret"

#creates a  database connection
def get_db_connection():
    return MySQLdb.connect(
        host="192.168.1.223",  
        user="user",  
        passwd="password", 
        db="movies_db",  
        port=3306  
    )
# def get_db_connection():
#    return MySQLdb.connect(
#        host="localhost",  
#        user="root",  
#        passwd="password", 
#        db="movies_db",  
#        port=3306  
#     )


#  Login Page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db = get_db_connection()
        with db.cursor() as cursor:
            sql = "SELECT * FROM users WHERE username = %s AND password = %s"
            cursor.execute(sql, (username, password))
            user = cursor.fetchone()
        db.close()

        if user:
            session["user"] = username
            return redirect(url_for("home"))  # Redirect to home after login
        else:
            return "Invalid username or password. <a href='/'>Try Again</a>"

    return render_template("index.html")

#  Home Page (Redirects to login if not logged in)
@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("home.html")

#  Registration Route
@app.route("/register", methods=["POST"])
def register():
    new_username = request.form.get("new_username")
    new_password = request.form.get("new_password")

    db = get_db_connection()
    with db.cursor() as cursor:
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(sql, (new_username, new_password))
        db.commit()
    db.close()

    return "Account created! <a href='/'>Go to Login</a>"

# Route to Add a Movie
@app.route("/add_movie", methods=["GET", "POST"])
def add_movie():
    if "user" not in session:
        return redirect(url_for("login"))

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

#  Search Movie Route
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
    if "user" not in session:
        return redirect(url_for("login"))

    db = get_db_connection()
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM movies")
        movies = cursor.fetchall()
    db.close()

    return render_template("list_movies.html", movies=movies)

#  Logout Route
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
