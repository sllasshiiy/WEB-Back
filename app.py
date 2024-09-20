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

@app.errorhandler(400)
def not_found(err):
    return '''
<!doctype html>
<html>
    <body>
        <h1>400</h1>
        <div>Некорректный запрос</div>
    </body>
</html>
''', 400

@app.errorhandler(401)
def not_found(err):
    return '''
<!doctype html>
<html>
    <body>
        <h1>401</h1>
        <div>Для доступа к запрашиваему ресурсу требуется аутентификация</div>
    </body>
</html>
''',401

@app.errorhandler(403)
def not_found(err):
    return '''
<!doctype html>
<html>
    <body>
        <h1>403</h1>
        <div>Доступ к запрошенному ресурсу запрещен</div>
    </body>
</html>
''', 403

@app.errorhandler(405)
def not_found(err):
    return '''
<!doctype html>
<html>
    <body>
        <h1>405</h1>
        <div>Указанный клиентом метод нельзя применить к текущему ресурсу</div>
    </body>
</html>
''', 405

@app.errorhandler(418)
def not_found(err):
    return '''
<!doctype html>
<html>
    <body>
        <h1>418</h1>
        <div>Я-чайник</div>
    </body>
</html>
''', 418

@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
            <body>
               <h1>web-сервер на flask</h1>
               <a href="/lab1/author">author</a>
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
<html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title> НГТУ,ФБ,Лабораторные работы </title>
    </head>

    <body>
        <header>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных
            <hr>
        </header>

        <main>
        <a href="/">Первая лабораторная</a>
        </main>

        <footer>
            <hr>
            &copy;Загородняя Виктория, ФБИ-21, 3 курс,2024</footer>
    </body>
</html>
'''
@app.route("/lab1")
def lab1():
    return '''
<!DOCTYPE html>
<html>
<head>
        <meta charset="UTF-8">
        <title>Лабораторная 1</title>
    </head>
    <body>
        <main>
        <p>Flask — фреймворк для создания веб-приложений на языке
        программирования Python, использующий набор инструментов
        Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
        называемых микрофреймворков — минималистичных каркасов
        веб-приложений, сознательно предоставляющих лишь самые ба-
        зовые возможности.</p>
        <a href="/lab1/web">Корень сайта</a>
        </main>
    </body>
</html>
'''