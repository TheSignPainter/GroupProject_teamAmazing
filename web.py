from flask import Flask
from flask import render_template, redirect, url_for
import os
import json
from flask import safe_join, send_from_directory, request, flash
from backend.hive_remote import getQueryResults, getBondInfoDetail, getSubscribe_, addSubscribe_
from flask_login import LoginManager,login_user,login_required,current_user, logout_user
from flask_wtf.form import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import Length,DataRequired,Optional
from backend.user import User_Dal, User_Signup
from backend.util import calculate_
from datetime import datetime, date, timedelta

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__,
    template_folder=os.path.join(PROJECT_PATH, 'templates'),
    static_folder=PROJECT_PATH)

login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = '234rsdf34523rwsf'

class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(message='用户名不能为空'), Length(2, 30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    remember_me = BooleanField('remenber me', validators=[Optional()], default=False)


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('User Name', validators=[DataRequired(), Length(2, 30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 20)])
    #confirm = PasswordField('密码：', validators=[DataRequired(), Length(1, 64)])


@app.route('/assets/<any(css, i, js, sound,fonts):folder>/<path:filename>')
def toplevel_static(folder, filename):
    folder = safe_join('assets/'+folder)
    filename = safe_join(folder, filename)
    cache_timeout = app.get_send_file_max_age(filename)
    return send_from_directory(app.static_folder, filename,
                               cache_timeout=cache_timeout)


@app.route('/')
def index():
    #print(current_user.is_authenticated)
    return render_template("mainpage.html")


@app.route('/Yieldcurve')
def yieldcurve():
    #date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    yesterday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")  # 昨天日期
    return render_template("yieldCurvePage.html", update_date=yesterday)


@app.route('/calculator')
def calculator():
    return render_template("calculatorPage.html")


@app.route('/search', methods=['POST', 'GET'])
def search():
    return json.dumps(getQueryResults(request.args.get('q', '')), ensure_ascii=False)


@app.route('/detail', methods=['POST', 'GET'])
def bondDetail():
    return json.dumps(getBondInfoDetail(request.args.get('q', '')), ensure_ascii=False)


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        result = User_Dal.login_auth(username, password)
        model = result[1]
        if result[0]['isAuth']:
            login_user(model)
            #print('登陆成功')
            #print(current_user.username)  # 登录成功之后可以用current_user来取该用户的其他属性，这些属性都是sql语句查来并赋值给对象的。
            return redirect('/')
        else:
            #print('登陆失败')
            return render_template('loginPage.html', action='/login', method='post', form=form)
    return render_template("loginPage.html", action='/login', method='post', form=form)


@login_manager.user_loader
def load_user(id):
    return User_Dal.load_user_byid(id)


@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        result = User_Signup.signup(username, email, password)
        model = result[1]
        login_user(model)
        return redirect('/')
    return render_template("SignUpPage.html", action='/signup', method='post', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/t')
@login_required
def hello_world():
    return 'Hello ' + current_user.username


@app.route('/admin')
@login_required
def admin():
    return render_template("userInfoPage.html")


@app.route('/admin/Detail')
@login_required
def admin_detail():
    return render_template("userInfoDetailPage.html")


@app.route('/admin/Book')
@login_required
def admin_book():
    bonds = getSubscribe_(current_user.id)
    bonds = [{'bond_name': bond[0], 'bond_short_name': bond[1], 'bond_id': bond[2]} for bond in bonds]
    num = len(bonds)
    return render_template("userInfoBookPage.html", subscribe_bonds=bonds, num=num)

@app.route('/admin/News')
@login_required
def admin_news():
    return render_template("userInfoNewsPage.html")


@app.route('/addSubscribe', methods=['GET','POST'])
def addSubscribe():
    if request.method == 'POST':
        result = addSubscribe_(request.form['user_id'], request.form['bond_id'])
        return result


@app.route('/calculate', methods=['GET','POST'])
def calculate():
    if request.method == 'POST':
        if request.form['type'] == 'ytm':
            return str(calculate_(request.form))
        elif request.form['type'] == 'pricing' or 'risk':
            return json.dumps(calculate_(request.form), ensure_ascii=False)


@app.route('/oops')
def under_construction():
    return render_template("error.html")


if __name__ == "__main__":
    app.debug = True
    app.run(port=31540, host='0.0.0.0')