from flask import Flask, render_template, request, redirect, session
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap


app = Flask(__name__)

bootstrap = Bootstrap(app)

app.secret_key = 'session'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root@192.168.136.152:3306/flasklogin"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(32), nullable=False)


class Article(db.Model):
    __tablename__ = 'article'
    article_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    detail = db.Column(db.TEXT())
    user_id = db.Column(db.ForeignKey('user.user_id'))


db.create_all()


# db.drop_all()

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/')
def hello_world():
    return 'hello flask'


@app.route('/regist', methods=['GET', 'POST'])
def regist():
    '''用户注册页'''
    if request.method == 'POST':
        username = request.form.get('name')
        password = request.form.get('pwd')
        print(username,password)
        if username and password:
            print('jinru')
            # user = User(username=username)
            # pswd = User(password=password)
            # db.session.add_all([user,pswd])
            user = User(username=username,password=password)
            db.session.add(user)
            db.session.commit()
    return render_template('regist.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''用户登录页'''
    if request.method == 'GET':

        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('user')
        user = User.query.filter_by(username=username).first()
        if user:
            print(user)
            password = request.form.get('pwd')
            pwd = user.password
            if pwd == password:
                # if username == 'alex' and password == '123':
                return redirect('/index')

        return 'ok'


@app.route('/index')
def index():
    '''渲染首页文章数据'''
    # user = User.query.filter_by(username='tom').first() # 查询成功
    article = Article.query.all()
    article_dic = {}
    for i in article:
        user = User.query.filter_by(user_id=i.user_id).first()
        # print(user.username)
        article_dic[str(i.article_id)] = {}
        article_dic[str(i.article_id)]['username'] = user.username
        article_dic[str(i.article_id)]['title'] = i.title
        article_dic[str(i.article_id)]['detail'] = i.detail

    print(article_dic)
    return render_template('index.html', article_dic=article_dic)


@app.route('/ajaxcheck')
def ajaxcheck():
    return 'ajax'

@app.route('/user/<username>')
def user(username):
    return 'user is %s' % username





if __name__ == '__main__':
    app.run()
