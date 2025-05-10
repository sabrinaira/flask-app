from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()  # This reads the .env file and loads the variables

secret_key = os.getenv("SECRET_KEY")
debug_mode = os.getenv("DEBUG", "False") == "True"
db_password = os.getenv("DB_PASSWORD")
db_port = os.getenv("PORT")

app = Flask(__name__)
app.config["SECRET_KEY"] = secret_key
app.config["DEBUG"] = debug_mode
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://postgres:{db_password}@localhost:{db_port}/bmi_db"
)
db = SQLAlchemy(app)


class Data(db.Model):
    __tablename__ = "userinfo"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)

    def __init__(self, pname, pemail, pweight, pheight):
        self.full_name = pname
        self.email = pemail
        self.weight = pweight
        self.height = pheight


with app.app_context():
    db.create_all()


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

        new_entry = Data(full_name, user_email, user_weight, user_height)
        db.session.add(new_entry)
        db.session.commit()

        return render_template(
            "thankyou.html",
            name=full_name,
            email=user_email,
            weight=user_weight,
            height=user_height,
        )


if __name__ == "__main__":
    app.debug = debug_mode
    app.run()
