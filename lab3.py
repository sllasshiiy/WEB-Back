from flask import Blueprint, render_template, request, make_response
lab3=Blueprint('lab3',__name__)


@lab3.route('/lab3/')
def lab():
    name=request.cookies.get('name')
    return render_template('lab3/lab3.html', name=name)

@lab3.route('/lab3/cookie')
def cookie():
    resp=make_response('установка cookie', 200)
    resp.set_cookie('name', 'Alex')
    resp.set_cookie('age', '20')
    resp.set_cookie('color', 'magenta')

@lab3.route('/lab3/form1')
def form1():
    errors={}
    user=request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age=request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    sex=request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)