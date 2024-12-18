from flask import Blueprint, render_template, request, make_response, redirect,session
lab4=Blueprint('lab4',__name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div',methods=['POST'])
def div():
    x1=request.form.get('x1')
    x2=request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    if x2 == '0':
        return render_template('lab4/div.html', error='На ноль делить нельзя, выберете другое число!')
    x1=int(x1)
    x2=int(x2)
    result=x1/x2
    return render_template('lab4/div.html',x1=x1,x2=x2, result=result)

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum',methods=['POST'])
def sum():
    x1=request.form.get('x1')
    x2=request.form.get('x2')
    x1 = int(x1) if x1 else 0
    x2 = int(x2) if x2 else 0   
    result=x1+x2
    return render_template('lab4/sum.html',x1=x1,x2=x2, result=result)

@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul',methods=['POST'])
def mul():
    x1=request.form.get('x1')
    x2=request.form.get('x2')
    x1 = int(x1) if x1 else 1
    x2 = int(x2) if x2 else 1
    result=x1*x2
    return render_template('lab4/mul.html',x1=x1,x2=x2, result=result)

@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub',methods=['POST'])
def sub():
    x1=request.form.get('x1')
    x2=request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    x1=int(x1)
    x2=int(x2)
    result=x1-x2
    return render_template('lab4/sub.html',x1=x1,x2=x2, result=result)

@lab4.route('/lab4/deg-form')
def deg_form():
    return render_template('lab4/deg-form.html')

@lab4.route('/lab4/deg',methods=['POST'])
def deg():
    x1=request.form.get('x1')
    x2=request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/deg.html', error='Оба поля должны быть заполнены!')
    if x2 == '0':
        return render_template('lab4/deg.html', error='На ноль делить нельзя, выберете другое число!')
    x1=int(x1)
    x2=int(x2)
    result=x1**x2
    return render_template('lab4/deg.html',x1=x1,x2=x2, result=result)

tree_count=0
max_trees=33

@lab4.route('/lab4/tree',methods=['GET','POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count,max_trees=max_trees)
    
    operation=request.form.get('operation')

    if operation == 'cut':
        if tree_count >0:
            tree_count -=1
    elif operation == 'plant':
        if tree_count < max_trees: 
            tree_count += 1

    return redirect('/lab4/tree')

users = [
    {'login':'alex', 'password':'917', 'name':'Алекс', 'gender':'M'},
    {'login':'bob', 'password':'777', 'name':'Боб', 'gender':'M'},
    {'login':'elly', 'password':'838', 'name':'Элли', 'gender':'F'},
    {'login':'olga', 'password':'995', 'name':'Ольга', 'gender':'F'},
    {'login':'windy', 'password':'123', 'name':'Винди', 'gender':'F'}
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            name = next((user['name'] for user in users if user['login'] == login), '')
        else:
            authorized = False
            login = ''
            name = ''
        return render_template('lab4/login.html', authorized=authorized, login=login, name=name)

    login = request.form.get('login')
    password = request.form.get('password')

    if not login:
        error = 'Не введён логин'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)
    if not password:
        error = 'Не введён пароль'
        return render_template('lab4/login.html', error=error, authorized=False, login=login)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            name = user['name']
            return render_template('lab4/login.html', authorized=True, name=name) 

    error = 'Неверные логин или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login=login)

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    message = ""
    snowflakes = ""
    temperature = None

    if request.method == 'POST':
        try:
            temperature = float(request.form.get('temperature'))
        except ValueError:
            message = "Ошибка: неверно введено значение температуры"

        if temperature is None:
            message = "Ошибка: не задана температура"
        elif temperature < -12:
            message = "Не удалось установить температуру — слишком низкое значение"
        elif temperature > -1:
            message = "Не удалось установить температуру — слишком высокое значение"
        elif -12 <= temperature <= -9:
            message = f"Установлена температура: {temperature}°С"
            snowflakes = "❄️❄️❄️"
        elif -8 <= temperature <= -5:
            message = f"Установлена температура: {temperature}°С"
            snowflakes = "❄️❄️"
        elif -4 <= temperature <= -1:
            message = f"Установлена температура: {temperature}°С"
            snowflakes = "❄️"

    return render_template('/lab4/fridge.html', message=message, snowflakes=snowflakes, temperature=temperature)

prices = {
    "ячмень": 12345,
    "овёс": 8522,
    "пшеница": 8722,
    "рожь": 14111
}

@lab4.route('/lab4/zakaz', methods=['GET', 'POST'])
def zakaz():
    message = ""
    if request.method == 'POST':
        grain = request.form.get('grain')
        try:
            weight = float(request.form.get('weight'))
        except (ValueError, TypeError):
            message = "Ошибка: вес не был указан или указан неверно."
            return render_template('/lab4/zakaz.html', message=message)

        if weight <= 0:
            message = "Ошибка: вес должен быть больше 0."
            return render_template('/lab4/zakaz.html', message=message)
        elif weight > 500:
            message = "Ошибка: такого объёма сейчас нет в наличии."
            return render_template('/lab4/zakaz.html', message=message)

        total_cost = prices[grain] * weight
        discount = 0

        if weight > 50:
            discount = total_cost * 0.10
            total_cost -= discount
            message = f"Заказ успешно сформирован. Вы заказали {grain}. Вес: {weight} т. Сумма к оплате: {total_cost:.2f} руб. Применена скидка за большой объём: {discount:.2f} руб."
        else:
            message = f"Заказ успешно сформирован. Вы заказали {grain}. Вес: {weight} т. Сумма к оплате: {total_cost:.2f} руб."

    return render_template('/lab4/zakaz.html', message=message)
