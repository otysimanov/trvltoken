from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from backend.db import db
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from firebase_admin import firestore

authapp = Blueprint('authapp', __name__)

# ================================================

# INI HALAMAN CONFIGURASI LOGIN
# 1. login_required
# 2. admin_required

# ================================================


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            flash('Anda harus login', 'danger')
            return redirect(url_for('.login'))
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session['user']['role'] == 'admin':
            return f(*args, **kwargs)
        else:
            flash('Anda bukan admin', 'danger')
            return redirect(url_for('authapp.login'))
    return wrapper


@authapp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = {
            'username': request.form['username'],
            'password': request.form['password']
        }

        users = db.collection('users').where(
            'username', '==', data['username']).stream()
        user = {}

        for us in users:
            user = us.to_dict()
            user['id'] = us.id

        if user:
            if check_password_hash(user['password'], data['password']):
                session['user'] = user
                flash('Anda berhasil login', 'success')
                return redirect(url_for('.dashboard'))
            else:
                flash('maaf password anda salah', 'danger')
                return redirect(url_for('.login'))
        else:   
            flash('username tidak terdaftar', 'danger')
            return redirect(url_for('.login'))

    if 'user' in session:
        return redirect(url_for('.dashboard'))
    return render_template('login.html')


@authapp.route('/logout', methods=["GET"])
def logout():
    session.clear()
    flash('Anda Keluar', 'danger')
    return redirect(url_for('.login'))


# @authapp.route('/register')
# def register():
#     data = {
#         'created_at': firestore.SERVER_TIMESTAMP,
#         'username': 'admin',
#         'nama_lengkap': 'administrator',
#         'password': generate_password_hash('administrator123', 'sha256'),
#         'role': 'admin'

#     }

#     db.collection('users').document('admin').set(data)
#     return "oke"

@authapp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
