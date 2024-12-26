from flask import Blueprint, render_template, request, session, redirect, current_app, flash, url_for
from db import db
from db.models import users, message
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy import or_
import re  # Импортируем модуль для работы с регулярными выражениями

rgz = Blueprint('rgz', __name__)
ADMIN_PASSWORD_HASH = generate_password_hash("admin123!")  # Хешированный пароль для администратора

def is_valid_login(login):
    # Логин должен состоять только из латинских букв, цифр и знаков . _ -
    return bool(re.match(r'^[a-zA-Z0-9._-]+$', login))

def is_valid_password(password):
    # Пароль должен содержать хотя бы одну латинскую букву, одну цифру и один специальный символ
    return (bool(re.search(r'[a-zA-Z]', password)) and
            bool(re.search(r'\d', password)) and
            bool(re.search(r'[!@#$%^&*()_+{}":;\'<>?,./-]', password)) and
            len(password) > 0 and
            bool(re.match(r'^[a-zA-Z0-9!@#$%^&*()_+{}":;\'<>?,./-]+$', password)))

@rgz.route('/rgz/')
def lab():
    user_login = session.get('login', "anonymous")  
    return render_template('rgz/index.html', login=session.get('login'))

def is_admin():
    user = current_user
    return user.login == "AdminMessage" and check_password_hash(user.password, "admin123!")

@rgz.route('/rgz/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('rgz/register.html')
    
    # Получаем логин и пароль из формы
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    # Проверка на пустые поля
    if not login_form or not password_form:
        return render_template('rgz/register.html', error='Логин и пароль не могут быть пустыми.')

    # Проверка валидности логина и пароля
    if not is_valid_login(login_form):
        return render_template('rgz/register.html', error='Логин содержит недопустимые символы.')

    if not is_valid_password(password_form):
        return render_template('rgz/register.html', error='Пароль должен содержать хотя бы одну букву, одну цифру и один специальный символ.')

    # Проверяем, существует ли пользователь с таким логином
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('rgz/register.html', error='Такой пользователь уже существует')
    
    # Хэшируем пароль и создаём нового пользователя
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    # Логиним нового пользователя и сохраняем логин в сессии
    login_user(new_user)
    session['login'] = login_form
    return redirect('/rgz/')

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html')
    
    # Получаем данные из формы
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    # Проверка на пустые поля
    if not login_form or not password_form:
        return render_template('/rgz/login.html', error='Логин и пароль не могут быть пустыми.')

    # Проверка валидности логина и пароля
    if not is_valid_login(login_form):
        return render_template('/rgz/login.html', error='Логин содержит недопустимые символы.')

    if not is_valid_password(password_form):
        return render_template('/rgz/login.html', error='Пароль должен содержать хотя бы одну букву, одну цифру и один специальный символ.')

    # Проверяем наличие пользователя в базе данных
    user = users.query.filter_by(login=login_form).first()
    if user:
        if check_password_hash(user.password, password_form):
            login_user(user)  # Авторизуем пользователя
            session['login'] = user.login  # Сохраняем логин в сессии            
            # Проверка на администратора
            if user.login == "AdminMessage":
                return redirect(url_for('rgz.admin_users_list'))  # Перенаправление на страницу администраторов
            
            return redirect(url_for('rgz.users_list'))  # Перенаправление на страницу пользователей
            
    # В случае ошибки отображаем сообщение
    return render_template('/rgz/login.html', error='Ошибка входа: логин и/или пароль неверны')

# Выход пользователя
@rgz.route('/rgz/logout')
@login_required
def logout():
    logout_user()  # Завершаем сессию пользователя
    session.pop('login', None)  # Удаляем логин из сессии
    return redirect('/rgz/')

# Список всех пользователей
@rgz.route('/rgz/users', methods=['GET'])
@login_required
def users_list():
    # Получаем всех пользователей, кроме текущего
    all_users = users.query.filter(users.id != current_user.id).all()
    return render_template('rgz/users.html', users=all_users)

# Отправка сообщения
@rgz.route('/rgz/send_message/<int:receiver_id>', methods=['POST'])
@login_required
def send_message(receiver_id):
    content = request.form.get('content')

    if not content:
        flash("Сообщение не может быть пустым.")
        return redirect(url_for('rgz.users_list'))

    # Создаем новое сообщение
    new_message = message(sender_id=current_user.id, receiver_id=receiver_id, content=content)
    db.session.add(new_message)
    db.session.commit()
    flash("Сообщение отправлено.")
    return redirect(url_for('rgz.users_list'))

# Просмотр сообщений текущего пользователя
@rgz.route('/rgz/messages', methods=['GET'])
@login_required
def messages_list():
    # Получаем все сообщения, адресованные текущему пользователю
    received_messages = message.query.filter_by(receiver_id=current_user.id).all()
    sent_messages = message.query.filter_by(sender_id=current_user.id).all()
    return render_template('rgz/chat.html', received=received_messages, sent=sent_messages)

@rgz.route('/rgz/reply_message/<int:message_id>', methods=['POST'])
@login_required
def reply_message(message_id):
    original_message = message.query.get_or_404(message_id)

    # Получаем текст ответа из формы
    reply_content = request.form.get('reply_content')

    # Создаем новое сообщение
    reply_message = message(
        content=reply_content,
        sender_id=current_user.id,
        receiver_id=original_message.sender_id  # Отправляем ответ отправителю оригинального сообщения
    )

    # Сохраняем новое сообщение в базе данных
    db.session.add(reply_message)
    db.session.commit()

    flash("Ваш ответ отправлен.")
    return redirect(url_for('rgz.messages_list'))

@rgz.route('/rgz/delete_message/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    msg = message.query.get_or_404(message_id)  # Измените 'message' на 'msg'

    # Проверяем, принадлежит ли сообщение текущему пользователю
    if msg.sender_id == current_user.id or msg.receiver_id == current_user.id:
        db.session.delete(msg)
        db.session.commit()
        flash("Сообщение удалено.")
    else:
        flash("Вы не можете удалить это сообщение.")
    
    return redirect(url_for('rgz.messages_list'))

@rgz.route('/rgz/admin/users', methods=['GET'])
@login_required
def admin_users_list():
    if not is_admin():
        flash("У вас нет прав для доступа к этой странице.")
        return redirect(url_for('rgz.lab'))
    users_list = users.query.all()  # Получаем всех пользователей
    return render_template('rgz/admin.html', users=users_list)

@rgz.route('/rgz/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not is_admin():
        flash("У вас нет прав для доступа к этой странице.")
        return redirect(url_for('rgz.lab'))

    user = users.query.get_or_404(user_id)

    if request.method == 'POST':
        user.login = request.form.get('login')
        password_form = request.form.get('password')
        if password_form:
            user.password = generate_password_hash(password_form)
        
        db.session.commit()
        flash("Учетная запись пользователя обновлена.")
        return redirect(url_for('rgz.admin_users_list'))

    return render_template('rgz/edit_user.html', user=user)

@rgz.route('/rgz/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not is_admin():
        flash("У вас нет прав для доступа к этой операции.")
        return redirect(url_for('rgz.admin_users_list'))

    user = users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("Учетная запись пользователя удалена.")
    return redirect(url_for('rgz.admin_users_list'))

@rgz.route('/rgz/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = current_user
    
    # Удаляем все сообщения, отправленные пользователем
    messages_sent = message.query.filter_by(sender_id=user.id).all()
    for msg in messages_sent:
        db.session.delete(msg)

    # Удаляем все сообщения, полученные пользователем
    messages_received = message.query.filter_by(receiver_id=user.id).all()
    for msg in messages_received:
        db.session.delete(msg)

    # Теперь удаляем аккаунт пользователя
    db.session.delete(user)
    db.session.commit()  # Сохраняем изменения в базе данных
    
    logout_user()  # Выход пользователя после удаления аккаунта
    session.pop('login', None)  # Удаляем логин из сессии
    flash("Ваш аккаунт был успешно удален.")
    
    return redirect('/rgz/')


