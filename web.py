from flask import Flask


app = Flask("myFlaskApp")


@app.route("/sayHello")
def greet():
    return "<h3> Hello from Flask APP - looks like we are connected ;)</h3> <hr/>"

app.run(debug=True)