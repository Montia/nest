import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db

def num_name_valid(num, name):
    #TODO: only allow students to register
    return True

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if g.user is not None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        num = request.form['num']
        name = request.form['name']
        password = request.form['password']
        db = get_db()
        error = None

        if not num:
            error = 'Num is required.'
        elif not name:
            error = 'Name is required.'
        elif not password:
            error = 'Password is required.'
        elif not num_name_valid(num, name):
            error = 'Num and name is not valid.' 
        elif db.execute(
            'select num from user where name = ?', (name,)
        ).fetchone() is not None:
            error = 'Num {} is already registered.'.format(num)

        if error is None:
            db.execute(
                'insert into user (num, name, passwd) values (?,?,?)',
                (num, name, generate_password_hash(password))
            )
            for lab in range(1, 8):
                db.execute(
                    'insert into score (num, lab, score) values (?,?,?)',
                    (num, lab, 0)
                )
            db.commit()
            return redirect(url_for('auth.login'))
        
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if g.user is not None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        num = request.form['num']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'select * from user where num = ?', (num, )
        ).fetchone()

        if user is None:
            error = 'Incorrect num.'
        elif not check_password_hash(user['passwd'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['num'] = user['num']
            return redirect(url_for('index'))
        
        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    num = session.get('num')

    if num is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'select * from user where num = ?', (num,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

