from flask import Blueprint, render_template, request, make_response, redirect,session,current_app,url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3 
import os
from os import path

lab8=Blueprint('lab8',__name__)

@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html',login=session.get('login')) 