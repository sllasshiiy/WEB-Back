from flask import Blueprint, render_template, request, make_response, redirect,session,current_app,url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3 
import os
from os import path

rgz=Blueprint('rgz',__name__)

@rgz.route('/rgz/')
def lab():
    return render_template('rgz/index.html',login=session.get('login')) 
def db_connect():
    if current_app.config['DB_TYPE']=='postgres':
        conn=psycopg2.connect(
            host='127.0.0.1',
            port='5432',
            database='rgz_web',
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

@rgz.route('/rgz/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('rgz/login.html')
    
    login=request.form.get('login')
    password=request.form.get('password')

    if not (login or password):
        return render_template('rgz/login.html',error="Заполните поля!")
    
    conn,cur=db_connect()

    cur.execute("SELECT * FROM users WHERE login=%s;",(login, ))
    user=cur.fetchone()

    if not user:
        db_close(conn,cur)
        return render_template('rgz/login.html',error='Логин и/или пароль неверны')
    
    if not check_password_hash( user['password'],password):
        db_close(conn,cur)
        return render_template('rgz/login.html',error='Логин и/или пароль неверны')
    
    session['login']=login
    db_close(conn,cur)
    return render_template('rgz/succes_login.html',login=login)

@rgz.route('/rgz/register',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('rgz/register.html')
    
    login=request.form.get('login')
    password=request.form.get('password')

    if not (login or password):
        return render_template('/rgz/register.html',error='Заполните все поля')
    conn,cur=db_connect()

    if current_app.config['DB_TYPE']=='postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;",(login, ))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;",(login, ))
    if cur.fetchone():
        db_close(conn,cur)
        return render_template('/rgz/register.html',error="Такой пользователь уже существует")
    
    password_hash=generate_password_hash(password)
    if current_app.config['DB_TYPE']=='postgres':
        cur.execute("INSERT INTO users (login,password) VALUES (%s,%s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login,password) VALUES (?,?);", (login, password_hash))
    db_close(conn,cur)
    return render_template('rgz/success.html',login=login)





