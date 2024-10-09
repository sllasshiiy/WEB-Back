from flask import Blueprint, url_for, redirect
lab1=Blueprint('lab1',__name__)


@lab1.route('/error')
def trigger():
    return 1/0


@lab1.route("/400")
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


@lab1.route("/402")
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


@lab1.route("/401")
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


@lab1.route("/403")
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


@lab1.route("/405")
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


@lab1.route("/418")
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


@lab1.route("/lab1/web")
def web():
    cs=url_for('static',filename='main.css')
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


@lab1.route("/lab1/author")
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


@lab1.route('/lab1/oak')
def oak():
    path=url_for("static", filename="oak1.jpg")
    t=url_for("static",filename="main.css")
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

@lab1.route('/lab1/counter')
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


@lab1.route('/lab1/reset')
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


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@lab1.route("/lab1/created")
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


@lab1.route("/lab1")
def lab():
    g=url_for("static",filename="main.css")
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


@lab1.route("/lab1/zadanee9")
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