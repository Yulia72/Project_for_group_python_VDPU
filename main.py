from flask import Flask #імпортуємо flask/термінал pip install flask
from flask import render_template, request, url_for, flash, redirect #відкриває HTML-шаблони,отримання даних з форми, посилання на декоратор, показує повідомлення (накриклад про нвірні введені дані), перенаправлення користувача
from flask_sqlalchemy import SQLAlchemy #ORМ для робот з базою даних/pip install flask-sqlalchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
#головний менеджер логіну, додає методи користувача, логінить користувача, поточний користувач, вихід з акаунту/ pip install flask-login
from werkzeug.security import generate_password_hash, check_password_hash #хешування паролю

app = Flask(__name__) #створення flask
app.config['SECRET_KEY'] = 'your-very-secret-key'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///side.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #вимикає зайве відстеження змін

db = SQLAlchemy(app)#створюємо об'єкт бази даних
login_manager = LoginManager()#створюємо менеджер логіну
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):#створення таблиця бази даних
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)#не можна пустим залишати рядок, унікальне ім'я
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
with app.app_context():
    db.create_all()

@login_manager.user_loader #логін менеджер шукає користувача у базі по його id
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    users = User.query.all() #отримуємо інформацію користувачів у терміналі
    for user in users:
        print(user.id, user.name, user.email, user.password)
    return render_template('index.html', users=users)

@app.route('/<name>')
def user_index(name):
    return render_template('index.html', user_name = name)

@app.route('/Articles')
def articles():
    new_articles = ['How to avoid expensive travel mistakes', 'Top 5 places to experience supernatural forces',
                    'Three wonderfully bizarre Mexican festivals', 'The 20 greenest destinations on Earth',
                    'How to survive on a desert island']
    return render_template('articles.html', articles = new_articles)


@app.route('/details')
def details():
    return render_template('details.html')

@app.route('/form', methods=['GET', 'POST'])
def user_form():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'),
        method= 'pbkdf2:sha256')
        user = User(name=name, email=email, password=password)

        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
        except:
            return "Помилка при реєстрації"
    return render_template('form.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Користувача з таким email не існує", "danger")
            return redirect(url_for('login'))
        if not check_password_hash(user.password, password):
            flash("Невірний пароль", "danger")
            return redirect(url_for('login'))

        login_user(user)
        flash("Вхід успішний", "success")
        return redirect(url_for('index'))


    return render_template('login.html')



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == "__main__":
   app.run(debug=True, port=5001)