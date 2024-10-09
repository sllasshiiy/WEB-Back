from flask import Blueprint, url_for, redirect, render_template
lab2=Blueprint('lab2',__name__)


@lab2.route('/lab2/a')
def a():
    return 'без слэша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'


flower_list=[]
@lab2.route('/lab2/add_flower/<name>')
def add_flower(name):
    g=url_for("static",filename="main.css")
    if not name:
        return 'Вы не задали имя цветка', 400
    flower_list.lab2end(name)
    return f'''
<!doctype html>
<html>
<header>
    <link rel="stylesheet" type="text/css" href="{g}">
    </header>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name} </p>
    <a href="/lab2/flowers">Показать все цветы</a>
    </body>
</html>
'''


@lab2.route('/lab2/flowers')
def show_flowers():
    g=url_for("static",filename="main.css")
    count=len(flower_list)
    flowers_html=''.join(f'<li>{flower}</li>' for flower in flower_list)
    return f'''
    <!doctype html>
    <html>
    <header>
    <link rel="stylesheet" type="text/css" href="{g}">
    </header>
        <body>
            <h1>Список цветков ({count})</h1>
            <ul>
                {flowers_html}
            </ul>
            <a href="/lab2/clear_flower_list">Очистить список цветков</a>
        </body>
    </html>
    '''


@lab2.route('/lab2/flowers/<int:flower_id>')
def get_flower(flower_id):
    g=url_for("static",filename="main.css")
    if flower_id <0 or flower_id >= len(flower_list):
        return 'Цветок не найден', 404
    flower_name=flower_list[flower_id]
    return f'''
    <!doctype html>
    <html>
    <header>
    <link rel="stylesheet" type="text/css" href="{g}">
    </header>
        <body>
            <h1>Цветок: {flower_name}</h1>
            <p>ID цветка: {flower_id}</p>
            <a href="/lab2/flowers">Вернуться к списку всех цветков</a>
        </body>
    </html>
'''


@lab2.route('/lab2/clear_flower_list')
def clear_flower_list():
    g=url_for("static",filename="main.css")
    flower_list.clear()
    return f'''
    <!doctype html>
    <html>
    <header>
    <link rel="stylesheet" type="text/css" href="{g}">
    </header>
        <body>
            <h1>Список цветков очищен</h1>
            <a href="/lab2/flowers">Показать список цветков</a>
        </body>
    </html>
'''


if __name__=='__main__':
    lab2.run(debug=True)



@lab2.route('/lab2/example')
def example():
    name='Загородняя Виктория'
    l1='Лабораторная работа 2'
    group='ФБИ-21'
    k='3 курс'
    fruits=[
        {'name':'яблоки','price':100},
        {'name':'груши','price':120},
        {'name':'апельсины','price':80},
        {'name':'мандарины','price':95},
        {'name':'манго','price':321},
    ]
    return render_template('example.html', name=name,l1=l1,group=group,k=k,fruits=fruits)


@lab2.route('/lab2/')
def lab():
    g=url_for("static",filename="main.css")
    return render_template('lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase="0 <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calculate(a, b):
    g=url_for("static",filename="main.css")
    summation = a + b
    subtraction = a - b
    multiplication = a * b
    division = a / b if b != 0 else 'Деление на ноль!'
    exponentiation = a ** b
    return f'''
    <!doctype html>
    <html>
    <header>
    <link rel="stylesheet" type="text/css" href="{g}">
    </header>
        <body>
            <h1>Результаты операций с {a} и {b}</h1>
            <ul>
                <li>Сумма: {summation}</li>
                <li>Вычитание: {subtraction}</li>
                <li>Умножение: {multiplication}</li>
                <li>Деление: {division}</li>
                <li>Возведение в степень: {exponentiation}</li>
            </ul>
            <a href="/lab2/calc/{a}/1">Использовать 1 в качестве второго числа</a>
        </body>
    </html>
    '''


@lab2.route('/lab2/calc/')
def default_calc():
    g=url_for("static",filename="main.css")
    return redirect(url_for('calculate', a=1, b=1))


@lab2.route('/lab2/calc/<int:a>')
def redirect_to_default(a):
    g=url_for("static",filename="main.css")
    return redirect(url_for('calculate', a=a, b=1))


if __name__ == '__main__':
    lab2.run(debug=True)



books = [
    {"title": "Тайная история", "author": "Донна Тартт", "genre": "Роман", "pages": "592"},
    {"title": "Гордость и предубеждение", "author": "Джейн Остен", "genre": "Зарубежная классика", "pages": "416"},
    {"title": "ОНО", "author": "Стивен Кинг", "genre": "Ужасы", "pages": "1248"},
    {"title": "Рога", "author": "Джо Хилл", "genre": "Ужасы", "pages": "448"},
    {"title": "Мастер и Маргарита", "author": "Михаил Булгаков", "genre": "Роман", "pages": "512"},
    {"title": "Шестерка Воронов", "author": "Ли Бардуго", "genre": "Фэнтези", "pages": "528"},
    {"title": "Молчание ягнят", "author": "Томас Харисс", "genre": "Триллер", "pages": "416"},
    {"title": "Ведьмак. Последнее желание", "author": "Анджей Сапковский", "genre": "Фэнтези", "pages": "320"},
    {"title": "Ангелы и Демоны", "author": "Дэн Браун", "genre": "Детектив", "pages": "640"},
    {"title": "Наследники богов. Огненный трон", "author": "Рик Риордан", "genre": "Фэнтези", "pages": "640"}
]


@lab2.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)


mems=[
    {
        "name": "Невдупленыш",
        "image": "nevdyplensh.jpg",
        "description": "Поднять-подняли, а вот разбудить забыли"
    },
    {
        "name": "Студенты НГТУ",
        "image": "students.jpg",
        "description": "Студенты НГТУ когда? Всегда!"
    },
    {
        "name": "Слепыш",
        "image": "slepsh.jpg",
        "description": "Ничего не видит, нужно очки ему прописать"
    },
    {
        "name": "Перваши на мат.анализе",
        "image": "abababbaababa.jpg",
        "description": "Ладно, мы были такими же первашами"
    },
    {
        "name": "Крутяк!",
        "image": "nice.jpg",
        "description": "Хомяк одобряет!"
    }
]


@lab2.route('/lab2/mems')
def show_mems():
    return render_template('mems.html', mems=mems)