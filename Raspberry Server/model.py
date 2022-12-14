import firebase_admin
from firebase_admin import credentials, db, firestore, storage

credential = {
    "type": "",
    "project_id": "",
    "private_key_id": "",
    "private_key": "",
    "client_email": "",
    "client_id": "",
    "auth_uri": "",
    "token_uri": "",
    "auth_provider_x509_cert_url": "",
    "client_x509_cert_url": ""
}
# import credentials file
cred = credentials.Certificate(credential)
firebase_admin.initialize_app(cred, {
    'storageBucket': '',
    'databaseURL': ''
})

firestore = firestore.client()

def create_realtime_db(data, path):
    ref = db.reference(path)
    ref.update(data)

def upload_img(imgSave, imgUpload):
    bucket = storage.bucket()
    blob = bucket.blob(imgUpload)
    blob.upload_from_filename(imgSave)
    blob.make_public()

    return blob.public_url

def ignore_first_call(fn):
    called = False

    def wrapper(*args, **kwargs):
        nonlocal called
        if called:
            return fn(*args, **kwargs)
        else:
            called = True
            return None
    return wrapper

def on_stop():
    print("Raspberry  stopped")
    create_realtime_db({'raspberry_server': False}, '/')



