from flask import * 

app = Flask("myFlaskApp")
app.secret_key = "secret"

@app.route("/")  
def index():
    return render_template('index.html')

@app.route("/add_movie", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        session["Movie_ID"] = request.form.get("movie_id")
        session["Movie_Name"] = request.form.get("movie_name")
        session["Description"] = request.form.get("description")
        return render_template("movies.html", movie=session)
    return render_template("add_movie.html")

@app.route("/search_movie", methods=["GET", "POST"])
def search_movie():
    if request.method == "POST":
        movie_id = request.form.get("movie_id")
        return render_template("movies.html", movie_id=movie_id)
    return render_template("search_movie.html")

@app.route("/list_movies")
def list_movies():
    return render_template("list_movies.html")

if __name__ == "__main__":
    app.run(debug=True)
