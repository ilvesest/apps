from flask import Flask, render_template

app = Flask(__name__) # __name__ refs to the current local py file


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')



