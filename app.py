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

@app.route("/web")
def web():
    return """<!doctype html>
        <html>
            <body>
               <h1>web-сервер на flask</h1>
               <a href="/author">author</a>
            <body>
        </html>"""

@app.route("/author")
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
    </body>
<html>
'''

@app.route("/info")
def info():
    return redirect("/author")

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