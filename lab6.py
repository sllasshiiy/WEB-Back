from flask import Blueprint, render_template, request, make_response, redirect,session,current_app,url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3 
import os
from os import path

lab6=Blueprint('lab6',__name__)

offices=[]
for i in range(1,11):
    offices.append({"number": i, "tenant": "", "price":900+i%10})

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')
def db_connect():
    if current_app.config['DB_TYPE']=='postgres':
        conn=psycopg2.connect(
            host='127.0.0.1',
            port='5432',
            database='vika_zag_knowledge_base',
            user='vika_zagorodnyaya_knowledge_base',
            password='200890',
            options="-c client_encoding=UTF8"
        )
        cur=conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path=path.dirname(path.realpath(__file__))
        db_path=path.jsoin(dir_path,"database.db")
        conn=sqlite3.connect(db_path)
        conn.row_factory=sqlite3.Row
        cur=conn.cursor()

    return conn,cur

def db_close(conn,cur):
    conn.commit()
    cur.close()
    conn.close()

@lab6.route('/lab6/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('lab6/login.html')
    
    login=request.form.get('login')
    password=request.form.get('password')

    if not (login or password):
        return render_template('lab6/login.html',error="Заполните поля!")
    
    conn,cur=db_connect()

    cur.execute("SELECT * FROM users WHERE login=%s;",(login, ))
    user=cur.fetchone()

    if not user:
        db_close(conn,cur)
        return render_template('lab6/login.html',error='Логин и/или пароль неверны')
    
    if not check_password_hash( user['password'],password):
        db_close(conn,cur)
        return render_template('lab6/login.html',error='Логин и/или пароль неверны')
    
    session['login']=login
    db_close(conn,cur)
    return render_template('lab6/succes_login.html',login=login)

@lab6.route('/lab6/register',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('lab6/register.html')
    
    login=request.form.get('login')
    password=request.form.get('password')

    if not (login or password):
        return render_template('lab6/register.html',error='Заполните все поля')
    conn,cur=db_connect()

    if current_app.config['DB_TYPE']=='postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;",(login, ))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;",(login, ))
    if cur.fetchone():
        db_close(conn,cur)
        return render_template('lab6/register.html',error="Такой пользователь уже существует")
    
    password_hash=generate_password_hash(password)
    if current_app.config['DB_TYPE']=='postgres':
        cur.execute("INSERT INTO users (login,password) VALUES (%s,%s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login,password) VALUES (?,?);", (login, password_hash))
    db_close(conn,cur)
    return render_template('lab6/success.html',login=login)

@lab6.route('/lab6/logout')
def logout():
    session.pop('login',None)
    return redirect('/lab6/login')

@lab6.route('/lab6/json-rpc-api/',methods=['POST'])
def api():
    data=request.json
    id=data['id']
    if data['method']=='info':
        return{
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }
    login=session.get('login')
    if not login:
        return{
            'jsonrpc': '2.0',
            'error':{
                'code': 1,
                'message': 'Unauthorized'
            },
            'id':id
        }
    if data['method']=='booking':
        office_number=data['params']
        for office in offices:
            if office['number']==office_number:
                if office['tenant']!='':
                    return{
                        'jsonrpc':'2.0',
                        'error':{
                            'code': 2,
                            'message': 'Офис уже занят!'
                        },
                        'id':id
                    }
                
                office['tenant']=login
                return{
                    'jsonrpc': '2.0',
                    'result':'success',
                    'id': id
                }
    if data['method']=='cancellation':
        office_number=data['params']
        for office in offices:
            if office['number']==office_number:
                if office['tenant']=='':
                    return{
                        'jsonrpc':'2.0',
                        'error':{
                            'code':3,
                            'message':'Office is not booked'
                        },
                        'id':id
                    }
                if office['tenant']!=login:
                    return{
                        'jsonrpc':'2.0',
                        'error':{
                            'code': 4,
                            'message':'You do not have permission to cancel this booking'
                        },
                        'id':id
                    }
                office['tenant']=""
                return{
                    'jsonrpc':'2.0',
                    'result': 'success',
                    'id':id
                }
    return{
            'jsonrpc': '2.0',
            'error':{
                'code': -32601,
                'message': 'Method not found'
            },
            'id': id
    }
