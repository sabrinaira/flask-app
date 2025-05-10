from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql"
# db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/thankyou", methods=["POST"])
def thankyou():
    if request.method == "POST":
        full_name = request.form["full_name"]
        user_email = request.form["user_email"]
        user_weight = request.form["user_weight"]
        user_height = request.form["user_height"]
        print(full_name, user_email)
        return render_template(
            "thankyou.html",
            name=full_name,
            email=user_email,
            weight=user_weight,
            height=user_height,
        )


if __name__ == "__main__":
    app.debug = True
    app.run()
