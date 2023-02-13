from firebase_admin import firestore, credentials
import firebase_admin

# ======================================

# CONFIGURASI FIREBASE
# SILAHKAN MASUKKAN SECRET KEY FIREBASE PADA FILE firebase.json

# ======================================

cred = credentials.Certificate('firebase.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

import pyrebase
firebaseConfig = {
    "apiKey": "AIzaSyByGKket6GHbYpvAcbT97eacxOZgIQpjsk",
    "authDomain": "trvltoken-576ca.firebaseapp.com",
    "databaseURL": "https://trvltoken-576ca-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "trvltoken-576ca",
    "storageBucket": "trvltoken-576ca.appspot.com",
    "messagingSenderId": "1004592571885",
    "appId": "1:1004592571885:web:45212be98ccbed41e6f3e4"
}
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

def get_all_collection(collection, orderBy=None, direction=None):
    if orderBy:
        collects_ref = db.collection(collection).order_by(
            orderBy, direction=direction)
    else:
        collects_ref = db.collection(collection)
    collects = collects_ref.stream()
    RETURN = []
    for collect in collects:
        ret = collect.to_dict()
        ret['id'] = collect.id
        RETURN.append(ret)
    return RETURN

def get_all_subcollection(col, uid, subcollection, orderBy=None, direction=None):
    if orderBy:
        collects_ref = db.collection(col).document(uid).collection(
            subcollection).order_by(orderBy, direction=direction)
    else:
        collects_ref = db.collection(col).document(
            uid).collection(subcollection)
    collects = collects_ref.stream()
    RETURN = []
    for collect in collects:
        ret = collect.to_dict()
        ret['id'] = collect.id
        RETURN.append(ret)
    return RETURN