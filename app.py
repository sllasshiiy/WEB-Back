from flask import Flask, url_for, redirect, render_template_string, render_template
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3


app=Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)


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
        <ul>
        <li><a href="/lab1">Первая лабораторная</a></li>
        <li><a href="/lab2/">Вторая лабораторная</a></li>
        <li><a href="/lab3/">Третья лабораторная</a></li>
        <li><a href="/lab4/">Четвертая лабораторная</a></li>
        </ul>
        </main>

        <footer>
            <hr>
            &copy;Загородняя Виктория, ФБИ-21, 3 курс,2024</footer>
    </body>
</html>
'''