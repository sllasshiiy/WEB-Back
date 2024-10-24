from flask import Blueprint, render_template, request, make_response, redirect
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
    if x1=='' or x2=='':
        x1=0
        x2=0
    else:
        x1=int(x1)
        x2=int(x2)   
    result=x1+x2
    return render_template('lab4/sum.html',x1=x1,x2=x2, result=result)

@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul',methods=['POST'])
def mul():
    x1=request.form.get('x1')
    x2=request.form.get('x2')
    if x1=='' or x2=='':
        x1=1
        x2=1
    else:
        x1=int(x1)
        x2=int(x2)
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

@lab4.route('/lab4/tree',methods=['GET','POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation=request.form.get('operation')

    if operation == 'cut':
        tree_count -=1
    elif operation == 'plant':
        tree_count +=1

    return redirect('lab4/tree')