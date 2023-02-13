from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from firebase_admin import firestore
from werkzeug.security import generate_password_hash
from backend.auth import admin_required, login_required
from backend.db import get_all_collection, db, get_all_subcollection, storage

usersapp = Blueprint('usersapp', __name__)

@usersapp.route('/users', methods=['POST', 'GET'])
@login_required
@admin_required
def all_users():
    if request.method == 'POST':
        if request.form['password'] != request.form['confirm_password']:
            flash('Password Tidak Sama', 'danger')
            return redirect(url_for('.all_users'))

        data = {
            'username': request.form['username'].lower(),
            'link': f'https://trvltoken.io/{request.form["username"]}',
            'password': generate_password_hash(request.form['password'], 'sha256'),
            'nama_lengkap': request.form['nama_lengkap'],
            'created_at': firestore.SERVER_TIMESTAMP,
            'role': 'user',
            'email': request.form['email']

        }
        
        
        users_ref = db.collection('users').where('username', '==', data['username']).stream()
        users = {}
        for ur in users_ref:
            users = ur.to_dict()
            users['id'] = ur.id
        
        if users:
            flash('Username / URL Sudah Ada', 'danger')
            return redirect(url_for('.all_users'))
        else:
            db.collection('users').document(data['username']).set(data)
            flash('Berhasil Menambahkan Users', 'success')
            return redirect(url_for('.all_users'))

        
    data = get_all_collection('users', orderBy='created_at', direction=firestore.Query.DESCENDING)
    return render_template('users.html', data=data)

@usersapp.route('/users/hapus',methods=['POST'])
@login_required
@admin_required
def delete_user():
    if request.method =='POST':
        uid = request.form.get('uid')
        # delete subdomain link
        links = get_all_subcollection('users', uid, 'link')
        if links:
            for link in links:
                db.collection('users').document(uid).collection('link').document(link['id']).delete()
                
        db.collection('users').document(uid).delete()

        flash('Berhasil Hapus User', 'danger')
        return ('', 204)

@usersapp.route('/users/resetpassword', methods=['POST'])
@login_required
@admin_required
def reset_password():
    if request.method == 'POST':
        uid = request.form.get('uid')
        data = {
            'password': generate_password_hash('trvltoken123', 'sha256')
        }

        db.collection('users').document(uid).update(data)
        flash('Berhasil Reset Password : <b>trvltoken123</b>', 'success')
        return ('', 204)




# ================================== CRUD LINK MANAJEMEN ============================
# ===================================================================================

@usersapp.route('/list-link', methods=['POST','GET'])
@login_required
def all_link():
    if request.method == 'POST':
        data = {
            'created_at': firestore.SERVER_TIMESTAMP,
            'title': request.form['title'],
            'url': request.form['url'],
            'is_active': True

        }

        db.collection('users').document(session['user']['username']).collection('link').document().set(data)
        flash('Berhasil Menambahkan Link', 'success')
        return redirect(url_for('.all_link'))

    data = get_all_subcollection('users', session['user']['username'], 'link', orderBy='created_at', direction=firestore.Query.DESCENDING)
    return render_template('link.html', data=data)

@usersapp.route('/<username>')
def profile(username):
    user = db.collection('users').document(username).get().to_dict()
    data = get_all_subcollection('users', username, 'link', orderBy='created_at', direction=firestore.Query.DESCENDING)
    return render_template('profile.html', data=data, user=user)

@usersapp.route('/list-link/hapus',methods=['POST'])
@login_required
def hapus_link():
    if request.method =='POST':
        uid = request.form.get('uid')
        db.collection('users').document(session['user']['username']).collection('link').document(uid).delete()
        flash('Berhasil Hapus Link', 'danger')
        return ('', 204)


@usersapp.route('/edit-profile', methods=['POST', 'GET'])
@login_required
def edit_profil():
    if request.method == 'POST':
        data = {
            'is_edit': True
        }
        
        needed = ['nama_lengkap', 'jabatan', 'about_me']
        for need in needed:
            if need in request.form and request.form[need]:
                data[need] = request.form[need]

        if 'foto' in request.files and request.files['foto']:
            image = request.files['foto']
            ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
            filename = image.filename
            lokasi = f"profil/{filename}"
            ext = filename.rsplit('.', 1)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                storage.child(lokasi).put(image)
                data['foto'] = storage.child(lokasi).get_url(None)
            else:
                flash("Foto tidak diperbolehkan", "danger")
                return redirect(url_for('.edit_profil'))
        
        db.collection('users').document(session['user']['id']).set(data, merge=True)
        flash('Berhasil Update Profil', 'success')
        session['user']['is_edit'] = True
        return redirect(url_for('.edit_profil'))

    user = db.collection('users').document(session['user']['id']).get().to_dict()

    return render_template('edit_profil.html', user=user)