from flask import Flask, url_for, redirect, render_template_string, render_template
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9
from rgz import rgz
import os
from os import path
from flask_sqlalchemy import SQLAlchemy
from db import db
from db.models import users,message
from flask_login import LoginManager


app=Flask(__name__)


login_manager=LoginManager()
login_manager.login_view='lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_users(login_id):
    return users.query.get(int(login_id))

app.config['SECRET_KEY']=os.environ.get('SECRET_KEY','Шла Саша по шоссе и сосала сушку')
app.config['DB_TYPE']=os.getenv('DB_TYPE','postgres')

if app.config['DB_TYPE']=='postgres':
    db_name='vika_zag_orm'
    db_user='vika_zagorodnyaya_knowledge_base'
    db_password='200890'
    host_ip='127.0.0.1'
    host_port=5432

    app.config['SQLALCHEMY_DATABASE_URI']=f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path=path.dirname(path.realpath(__file__))
    db_path=path.join(dir_path,"vika_zag_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{db_path}'

db.init_app(app)
app.secret_key='Шла Саша по шоссе и сосала сушку'


app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)
app.register_blueprint(rgz)


@app.errorhandler(404)
def not_found(err):
    tt=url_for("static",filename="cat.jpg")
    return '''
<!doctype html>
<html>
    <body>
        <h1 style="font-size:4em; color:red;">404</h1>
        <div style="font-size:3em; color:green;margin-bottom: 20px;">К сожалению, такой страницы не существует</div>
        <img src="''' + tt +'''">
    </body>
</html>
''', 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template_string('''
        <!doctype html>
        <html lang="ru">
        <head>
            <meta charset="utf-8">
            <title>Ошибка 500</title>
        </head>
        <body>
            <h1>Внутренняя ошибка сервера (500)</h1>
            <p>Произошла ошибка на сервере. Пожалуйста, попробуйте позже.</p>
        </body>
        </html> '''),500
if __name__=='__main__':
    app.run(debug=False)


@app.route("/")
@app.route("/index")
def start():
    g=url_for("static",filename="main.css")
    return f'''
<!DOCTYPE html>
<html lang="ru">
    <head>
        <link rel="stylesheet" type="text/css" href="{g}">
        <meta charset="UTF-8">
        <title> НГТУ,ФБ,Лабораторные работы </title>
    </head>

    <body>
        <header>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
            <hr>
        </header>

        <main>
        <div class=st>
        <ul>
        <li><a href="/lab1" style="color:black;text-shadow: 1px 1px 2px rgba(246, 246, 246, 0.875);">Первая лабораторная</a></li>
        <li><a href="/lab2/" style="color:black;text-shadow: 1px 1px 2px rgba(246, 246, 246, 0.875);">Вторая лабораторная</a></li>
        <li><a href="/lab3/" style="color:black;text-shadow: 1px 1px 2px rgba(246, 246, 246, 0.875);">Третья лабораторная</a></li>
        <li><a href="/lab4/" style="color:black;text-shadow: 1px 1px 2px rgba(246, 246, 246, 0.875);">Четвертая лабораторная</a></li>
        <li><a href="/lab5/" style="color:black;text-shadow: 1px 1px 2px rgba(246, 246, 246, 0.875);">Пятая лабораторная</a></li>
        <li><a href="/lab6/" style="color:black;text-shadow: 1px 1px 2px rgba(246, 246, 246, 0.875);">Шестая лабораторная</a></li>
        <li><a href="/lab7/" style="color:black;text-shadow: 1px 1px 2px rgba(246, 246, 246, 0.875);">Седьмая лабораторная</a></li>
        <li><a href="/lab8/" style="color:black;text-shadow: 1px 1px 2px rgba(246, 246, 246, 0.875);">Восьмая лабораторная</a></li>
        <li><a href="/lab9/" style="color:black;text-shadow: 1px 1px 2px rgba(246, 246, 246, 0.875);">Девятая лабораторная</a></li>
        <li><a href="/rgz/" style="color:black;text-shadow: 1px 1px 2px rgba(246, 246, 246, 0.875);">РГЗ</a></li>
        </ul>
        <div>
        </main>

        <footer>
            <hr>
            &copy;Загородняя Виктория, ФБИ-21, 3 курс,2024</footer>
    </body>
</html>
'''