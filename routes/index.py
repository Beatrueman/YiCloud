from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint
from flask_bcrypt import Bcrypt  # 使用bcrypt加密
from flask_login import LoginManager, login_user, UserMixin, logout_user, login_required  # 登录认证
import os
import re
import config

SQLALCHEMY_DATABASE_URI_A = 'mysql://'+config.user+':'+config.password+'@'+config.host+':'+str(3306)+'/'+config.database

app = Flask(__name__, template_folder='../templates', static_folder='../static')
index = Blueprint('index', __name__)
bcrypt = Bcrypt()


# 定义配置对象
class Config(object):
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI_A
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


app.config.from_object(Config)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '123'
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# 数据库建表
class User(UserMixin, db.Model):
    __tablename__ = 'cloud_user'  # 设置表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column('username', db.String(100), unique=True, nullable=False)
    password = db.Column('password', db.String(255), nullable=False)
    email = db.Column('email', db.String(255), nullable=True)
    phone = db.Column('phone', db.Integer, nullable=False, doc='电话号码')


# 通过user_id加载已认证的用户对象
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 密码安全规范限制
def vaild_password(password):
    # 密码至少8个字符，包含至少一个大写字母，一个小写字母和一个特殊字符
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%&*]).{8,}$"
    if re.match(pattern, password):
        return True
    else:
        return False


@index.route('/regist', methods=['GET', 'POST'])
def regist():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']

        # 判断密码是否符合规范
        if vaild_password(password):

            # 对密码加密
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            user = User(username=username, password=hashed_password, email=email, phone=phone)
            try:
                # 新添加的实例对象添加给数据库会话对象
                db.session.add(user)
                # 提交至数据库
                db.session.commit()

                user_folder = os.path.join('data',username)
                if not os.path.exists(user_folder):
                    os.makedirs(user_folder)
                print("已创建该用户的文件夹")

                # 注册成功跳转至index界面
                return render_template('index.html')
            except Exception as e:
                error_message = "注册失败：" + str(e)
                app.logger.error(error_message)
                print(error_message)
                # 回滚数据库事务
                db.session.rollback()

                return "注册失败，请返回注册页面重试！"
        else:
            return "密码不符合规范！必须至少8个字符，包含至少一个大写字母、一个小写字母和一个特殊字符(@#$%&*)"

    return render_template('regist.html')


@index.route('/', methods=['GET', 'POST'])  # 索引欢迎界面
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.session.query(User).filter_by(username=username).first()  # 查询用户

        # 匹配用户与密码
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)  # 登录认证，保持登录状态
            return redirect('/dashboard')

        else:
            return render_template('index.html', message='用户名或密码错误，请重试！')

    return render_template('index.html')

@login_required
@index.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect('/')

