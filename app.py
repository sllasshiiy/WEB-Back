from flask import Flask, url_for, redirect
app=Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return '''
<!doctype html>
<html>
    <body>
        <h1>404</h1>
        <div>Нет такой страницы</div>
    </body>
</html>
''', 404

@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
            <body>
               <h1>web-сервер на flask</h1>
               <a href="/author">author</a>
            <body>
        </html>""",200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
            }

@app.route("/lab1/author")
def author():
    name="Загородняя Виктория Артемовна"
    group="ФБИ-21"
    faculty="ФБ"

    return """<!doctype html>
        <html>
            <body>
               <p>Студент: """ + name + """</p>
               <p>Группа: """ + group + """</p>
               <p>Факультет: """ + faculty + """</p>
               <a href="/web">web</a>
            <body>
        </html>"""

@app.route('/lab1/oak')
def oak():
    path=url_for("static", filename="oak.jpg")
    path=url_for("static",filename="lab1.css")
    return '''
    <!doctype html>
        <html>
            <body>
                <h1>Дуб</h1>
                <img src="''' + path + ''' ">
            <body>
        </html>
'''

count=0

@app.route('/lab1/counter')
def counter():
    global count
    count+=1
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <a href="/lab1/reset">Обнуление счетчика</a>
    </body>
<html>
'''

@app.route('/lab1/reset')
def reset():
    global count
    count=0
    return '''
<!doctype html>
<html>
    <body>
        Ваш счетчик обновлен: ''' + str(count) + '''
    </body>
<html>
'''

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>Что-то создано...</i></div>
    </body>
</html>
''',201

@app.route("/")
@app.route("/index")
def start():
    return '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title> НГТУ,ФБ,Лабораторные работы </title>
    </head>

    <body>
        <header>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
            <hr>
        </header>

        <main>
        <a href="/lab1">Первая лабораторная</a>
        </main>

        <footer>
            <hr>
            &copy;Загородняя Виктория, ФБИ-21, 3 курс,2024</footer>
    </body>
</html>
'''

