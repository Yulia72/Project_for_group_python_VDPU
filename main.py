from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(1000), nullable=False, unique=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/user/<name>')
def user(name):
    return render_template('index.html', user_name=name)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/form',methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        return  f"Thank you, {user} We got our email and password"

    return render_template('form.html')


if __name__ == '__main__':
    app.run(port=5001)

