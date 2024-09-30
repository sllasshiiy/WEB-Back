from flask import Flask, url_for, redirect, render_template_string, render_template
app=Flask(__name__)

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

@app.route('/error')
def trigger():
    return 1/0

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

@app.route("/400")
def err_400():
    return '''
<!doctype html>
<html>
    <body>
        <h1>400</h1>
        <p>Некорректный запрос</p>
    </body>
<html>
''', 400

@app.route("/402")
def err_402():
    return '''
<!doctype html>
<html>
    <body>
        <h1>402</h1>
        <p>Зарезервировано в будущем</p>
    </body>
<html>
''', 402

@app.route("/401")
def err_401():
    return '''
<!doctype html>
<html>
    <body>
        <h1>401</h1>
        <p>Для доступа к запрашиваему ресурсу требуется аутентификация</p>
    </body>
<html>
''', 401

@app.route("/403")
def err_403():
    return '''
<!doctype html>
<html>
    <body>
        <h1>403</h1>
        <p>Доступ к запрошенному ресурсу запрещен</p>
    </body>
<html>
''', 403

@app.route("/405")
def err_405():
    return '''
<!doctype html>
<html>
    <body>
        <h1>405</h1>
        <p>Указанный клиентом метод нельзя применить к текущему ресурсу</p>
    </body>
<html>
''', 405

@app.route("/418")
def err_418():
    return '''
<!doctype html>
<html>
    <body>
        <h1>418</h1>
        <p>Я-чайник</p>
    </body>
<html>
''', 418

@app.route("/lab1/web")
def web():
    cs=url_for('static',filename='lab1.css')
    return f'''<!doctype html>
        <html>
        <head>
        <link rel="stylesheet" type="text/css" href="{cs}">
        </head>
            <body>
               <h1>web-сервер на flask</h1>
               <a href="/lab1/author">author</a>
            </body>
        </html>''',200, {
            'X-Server': 'sample',
            'Content-Type': 'text/html; charset=utf-8'
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
    path=url_for("static", filename="oak1.jpg")
    t=url_for("static",filename="lab1.css")
    return f'''
    <!doctype html>
        <html>
        <head>
        <link rel="stylesheet" type="text/css" href="{t}">
        </head>
            <body>
                <h1>Дуб</h1>
                <img src="''' + path +''' ">
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
        <a href="/lab1/counter">Счетчик</a>
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
    g=url_for("static",filename="lab1.css")
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
        <a href="/lab1">Первая лабораторная</a>
        </main>

        <footer>
            <hr>
            &copy;Загородняя Виктория, ФБИ-21, 3 курс,2024</footer>
    </body>
</html>
'''
@app.route("/lab1")
def lab1():
    g=url_for("static",filename="lab1.css")
    return f'''
<!DOCTYPE html>
<html>
<head>
        <meta charset="UTF-8">
        <title>Лабораторная 1</title>
        <link rel="stylesheet" type="text/css" href="{g}">
    </head>
    <body>
        <main>
        <h1>Flask</h1>
        <p>Flask — фреймворк для создания веб-приложений на языке
        программирования Python, использующий набор инструментов
        Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
        называемых микрофреймворков — минималистичных каркасов
        веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
        <a href="/index">Корень сайта</a>
        <h2>Список роутов</h2>
        <ul>
            <li><a href="/lab1/author">Страница автора</a></li>
            <li><a href="/lab1/web">WEB сервер на Flask</a></li>
            <li><a href="/lab1/oak">Дуб</a></li>
            <li><a href="/lab1/counter">Счетчик посещений</a></li>
            <li><a href="/lab1/created">Страница успешного создания</a></li>
            <li><a href="/lab1/info">Информация</a></li>
            <li><a href="/lab1/error">Генерация ошибки</a></li>
            <li><a href="/lab1/zadanee9">Задание 9</a></li>
        </ul>
        </main>
    </body>
</html>
'''
@app.route("/lab1/zadanee9")
def zadanee9():
    y=url_for("static",filename="lp1.jpg")
    x=url_for("static",filename="lp2.jpg")
    return '''<!doctype html>
        <html>
            <body>
                <div>Когда мне было шесть лет, в книге под названием "Правдивые истории", 
                где рассказывалось про девственные леса, я увидел однажды удивительную картинку. 
                На картинке огромная змея - удав - глотала хищного зверя. Вот как это было нарисовано:
                </div>
                <img src="''' + y +'''">
                <div>В книге говорилось: "Удав заглатывает свою жертву целиком, не жуя. После этого он 
                уже не может шевельнуться и спит полгода подряд, пока не переварит пищу".
                Я много раздумывал о полной приключений жизни джунглей и тоже нарисовал цветным карандашом 
                свою первую картинку. Это был мой рисунок № 1. Вот что я нарисовал:</div>
                <img src="''' + x +'''">
                <div>Я показал мое творение взрослым и спросил, не страшно ли им.</div>
''', 200, {
    'Content-Language': 'ru',
    'Age': 20,
    'Date': 'Wed, 20 Oct 2024 14:28:00 GMT'
}

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list=['роза','тюльпан','незабудка','ромашка']
@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return "такого цветка нет", 404
    else:
        return "цветок: "+ flower_list[flower_id]

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name} </p>
    </body>
</html>
'''

@app.route('/lab2/example')
def example():
    name='Загородняя Виктория'
    return render_template('example.html', name=name)