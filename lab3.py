from flask import Blueprint, render_template, request, make_response, redirect
lab3=Blueprint('lab3',__name__)


@lab3.route('/lab3/')
def lab():
    name=request.cookies.get('name') or 'Аноним'
    name_color=request.cookies.get('name_color')
    age=request.cookies.get('age')
    return render_template('lab3/lab3.html', name=name, name_color=name_color,age=age)


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp=make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/cookie')
def cookie():
    resp=make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Vika',max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors={}
    user=request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле "Имя" !'
    age=request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле "Имя" !'
    sex=request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

price=0

@lab3.route('/lab3/pay')
def pay():
    global price
    drink=request.args.get('drink')
    if drink == 'cofee':
        price=120
    elif drink == 'black-tea':
        price=80
    else:
        price=70

    if request.args.get('milk') == 'on':
        price+=30
    if request.args.get('sugar') == 'on':
        price+=10
    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/settings')
def settings():
    color = request.form.get('color')
    background_color = request.form.get('background_color')
    font_size = request.form.get('font_size')
    font_weight=request.form.get('font_weight')
    if color:
        resp = make_response(redirect('/lab3/settings'))
        resp.set_cookie('color', color)
        return resp
    if background_color:
        resp = make_response(redirect('/lab3/settings'))
        resp.set_cookie('background_color', background_color)
        return resp
    if font_size:
        resp = make_response(redirect('/lab3/settings'))
        resp.set_cookie('font_size', font_size)
        return resp
    if font_weight:
        resp = make_response(redirect('/lab3/settings'))
        resp.set_cookie('font_weight', font_weight)
        return resp
    
    color = request.cookies.get('color')
    background_color = request.cookies.get('background_color')
    font_size = request.cookies.get('font_size')
    font_weight = request.cookies.get('font_weight')
    
    return render_template('lab3/settings.html', color=color, background_color=background_color, font_size=font_size,font_weight=font_weight)

@lab3.route('/lab3/del_cookie_settings')
def del_cookie_settings():
    resp=make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('background_color')
    resp.delete_cookie('font-size')
    resp.delete_cookie('font-weight')
    return resp

@lab3.route('/lab3/ticket_form', methods=['GET', 'POST'])
def ticket_form():
    if request.method == 'POST':
        # Получение данных из формы
        passenger_name = request.form['name']
        shelf_type = request.form['shelf']
        is_bedding = 'bedding' in request.form
        is_baggage = 'baggage' in request.form
        age = request.form['age']
        departure = request.form['departure']
        destination = request.form['destination']
        travel_date = request.form['date']
        is_insurance = 'insurance' in request.form

        # Проверка на заполнение всех полей и возраст
        if not all([passenger_name, shelf_type, age, departure, destination, travel_date]):
            flash("Пожалуйста, заполните все поля.")
            return redirect(url_for('ticket_form'))

        try:
            age = int(age)
            if age < 1 or age > 120:
                flash("Возраст должен быть от 1 до 120 лет.")
                return redirect(url_for('ticket_form'))
        except ValueError:
            flash("Возраст должен быть числом.")
            return redirect(url_for('ticket_form'))

        # Расчет стоимости
        price = 1000 if age >= 18 else 700

        if shelf_type in ['lower', 'lower_side']:
            price += 100
        if is_bedding:
            price += 75
        if is_baggage:
            price += 250
        if is_insurance:
            price += 150

        ticket_type = "Детский билет" if age < 18 else "Взрослый билет"

        return render_template('/lab3/ticket_form.html', 
                               name=passenger_name, 
                               shelf=shelf_type, 
                               age=age, 
                               departure=departure, 
                               destination=destination, 
                               travel_date=travel_date, 
                               price=price, 
                               ticket_type=ticket_type)

    return render_template('lab3/forma.html')
