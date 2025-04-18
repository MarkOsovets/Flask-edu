from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///blog.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=False)
    psw = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<users {self.id}>"

class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


    def __repr__(self):
        return f"<profiles {self.id}>"   


@app.route("/register", methods=["POST","GET"])
def register():
    try:
        hash = generate_password_hash(request.form['psw'])
        u = Users(email=request.form['email'], psw=hash)
        db.session.add(u)
        db.session.flush()

        p = Profiles(name=request.form['name'], old=request.form['old'], city = request.form['city'], user_id = u.id)
        db.session.add(p)
        db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка добавления в БД")

    return render_template("register.html", title="Регистрация")

@app.route("/")
def index():
    return render_template("index.html",title="Главная")

if __name__ == '__main__':
    with app.app_context():   # Активируем контекст приложения
        db.create_all()     # Создание всех таблиц
    app.run(debug=True)