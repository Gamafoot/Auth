from flask import render_template, session, flash, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from Modules.DataBase import DataBase
from Blueprints.auth import bp_auth
import re

#============================================================================
#========================== Flask decotartors ===============================
#============================================================================
@bp_auth.before_request
def before_request():
    global db
    db = DataBase()

#============================================================================
#=========================== Custom functions ===============================
#============================================================================
def validateEmail(email:str):
    error = ''
    if not re.search('([a-zA-Z]|\d)*@[a-z]+\.[a-z]', email): error = 'Почта введена неккоректно!'
    if re.search("""WHERE|SELECT|DELETE|FROM|INSERT|INTO|UPDATE|SET|ALTER|!|"|'|\(|\)|\*|,|:|;|<|=|>|\?|`""", email): error = 'Почта введена неккоректно!'
    return error if len(error) > 0 else True


def validatePassword(password:str):
    error = ''
    if len(password) < 8 or len(password) > 100: error = 'Пароль должен состоять от 8 до 100 символов!'
    elif not re.search('[a-z]+', password): error = 'Пароль должен содержать латинские буквы!'
    elif not re.search('[A-Z]+', password): error = 'Пароль должен содержать заглавный латинские буквы!'
    elif not re.search('\d+', password): error = 'Пароль должен содержать цифры!'
    elif not re.search("""!|"|#|\$|%|&|'|\(|\)|\*|\+|,|-|\.|/|:|;|<|=|>|\?|@|\[|\\|\]|\^|_|`|\{|\||\}|~""", password): error = 'Пароль должен содержать спец символы! (!,#,$,%,?)'
    return error if len(error) > 0 else True

#============================================================================
#========================== Route functions =================================
#============================================================================
@bp_auth.route('/register', methods=['POST','GET'])
def register():
    
    if request.method == 'POST':
        
        email = request.form.get('email')
        password = request.form.get('password')
        password_repeat = request.form.get('repeat_password')
        
        for i in range(1):
            if password == password_repeat:
                
                validate_email = validateEmail(email)
                if validate_email != True:
                    flash('Неккоректный email адресс!')
                    break
                
                valide_password = validatePassword(password)
                if valide_password != True:
                    flash(valide_password, category='error')
                    break
                
                if not db.HasUser(email, table='users', field='login'):
                    user_id = db.AddUser(email, generate_password_hash(password))
                    session['logged'] = user_id
                    return redirect('/')
                else:
                    flash('Пользователь с такой почтой уже зарегистрирован!', category='error')
            else:
                flash('Пароли не совпадают!', category='error')
    
    return render_template('register.html')


@bp_auth.route('/login', methods=['POST','GET'])
def login():
    
    if request.method == 'POST':
        
        email = request.form.get('email')
        password = request.form.get('password')
        
        for i in range(1):
            validate_email = validateEmail(email)
            if validate_email != True:
                flash('Неккоректный email адресс!')
                break
            
            if db.HasUser(email, table='users', field='login') and check_password_hash(db.GetHash(email, table='users', field='login'), password):
                user_id = db.GetUser(email, 'users', 'login')['id']
                session['logged'] = user_id
                return redirect('/')
            else:
                flash('Неверный логин или пароль',category='error')
    
    return render_template('login.html')


@bp_auth.route('/logout')
def logout():
    if 'logged' in session:
        session.clear()
        return redirect('/login')
    else:
        return redirect('/')