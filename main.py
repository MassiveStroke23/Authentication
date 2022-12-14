from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
#Line below only required once, when creating DB. 
db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["POST","GET"])
def register():
    if request.method =="GET":
        return render_template("register.html")
    elif request.method == "POST":
        new_user = User(email=request.form['email'],
                        password=generate_password_hash(password=request.form['password'],method='pbkdf2:sha256',salt_length=8),
                        name=request.form['name'])
        db.session.add(new_user)
        db.session.commit()
        global temp_name
        temp_name = request.form['name']
        return redirect(url_for("secrets"))


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/secrets')
def secrets():
    temp_name = "Sen"
    return render_template("secrets.html", isim=temp_name)


@app.route('/logout')
def logout():
    pass


@app.route('/download')
def download():
    return send_from_directory('static/files', filename="cheat_sheet.pdf")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
