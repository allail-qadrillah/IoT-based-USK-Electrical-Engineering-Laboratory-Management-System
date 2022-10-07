import firebase_admin
from firebase_admin import credentials, firestore, storage, db
import uuid

credential = {
    "type": "service_account",
    "project_id": "eed-website-34a52",
    "private_key_id": "bba3337bcbd6fc9bb690db4275b61dc82fd859ab",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCwrLLOP3zi8PL1\n8PmVJzrMeEbGTFbuwxgbAB6X1jvFcJDIwUIl/ca1y8Uo2Yhs3/s+Kg+TXUPf8Kct\nwIKTbT4VLCPnSPZTb4TgPRLObo1hiu0pjpoz1NbENsbTc/GvmdwOPOS9FYLn005n\nJJbTWcjckhR3kXUDspm2UaIeGopAF6eUBXkg/PAdPkCziqViLifS6cEHlAhRFcrR\nbZvQQtg6EVyrVkZK4N3ZSl9Mj8X2UngOoBNBAydRqBZgTZ+zP3YSAO4f0URqzi/4\nm3yqOfph/rv1hF1tpEtFMMh7TDm6ECZ3i3lgMo32ClFKZ1NJm5ZHsEYft6zW+qUA\nUUYbAQJnAgMBAAECggEAAI1Iql9+EIukQG5QxpurCqF44yA/JQ0DvjT11UheNKcv\npJjmZSpR1YhTQUl3yMwr4AY58eVm2rXzrtn10gQv9KBrndjXVXpjpdDJPzKdGXK9\nCiQ/uvR/MiPTqixu73P9+gqFNfTjTS+IZ/++URfr/BhnnPZzFLzSCG+Zn6flAzgg\nJVKvojurRN86QGdCZLWYWSF8iKT3krdYJWVk3GdeiJKA4AE6BBUx+j++HMz9rigC\nB3jufMrBMsksW7euFqfcWEjHifP7r6rAWRcQyWRxwYtVsCYWf5Sx/vS4CMgvazrz\nBz/YMB8KI7qaa1sZJyL4+D6BqH33hOZv/Z0Cwrmm0QKBgQDa5yCSNHZVTTw5MB/t\nKxvqZhB+4RxaQMehnllmfv/h/oGOiNmIzB1d9v7pT3wP6a0bl1T2CnOkO3Mbk4vk\n5MKLFrss3at3JNWzV7Q5poOOa5eqS5RtcNxZ1P9Ad/TC0Qd6lI5MB8D5JSa7ntj9\n+p583aiiFEdOTqDGmjpVRl4ZFwKBgQDOnYr9z7vRFmLbKozOWJIQVYE90YDs6f2/\nO9oEhh5t3XO8RTwJdOmiEFtD2IuAppD7lCw/8mKByR2qa3Mfd4EnqBlx+rRAVnGg\nDGnQBf58XzCpIX+ybwbbb3BGkgnA3QqSNjwyLovLA8kR3Z9XuWZsTL4xfTb47JUO\nM1/Dy9qTMQKBgH/tat+GwVEAnh1dvorAEsRdeW5s6EDmcsRE4kJAHhJYxiYiW97S\nSqdLXZXD2eEC0yO4wPI5EXP9Ojv3cl4GQps+YYzKzxYF9M2mh7DZWzC0OCJRoSCE\nQIJPNAzdDbF8rz436yELtv7jc0tafb2P5Wdbst1ltHZTBSqLn2OOiBdpAoGAW7Xu\nVg75TSvkoWfXrFgALaPmhCwUUBTk/xdwBIYLx7R+hNkudvwgIEGmYQ0jju1geWsh\n4RiTxQwiUNz08si22YVyFfe0PsKgGOypox6mAUq3bLtj1S4XGxvx+EEmdycmZBQS\n0Ct8/ZYmj/mRmvy+i9/cpFbyKbfJyc3f+iboVGECgYAWaJXHnvZj15MO5KVFOICn\ngCfly3ijBb5Zs7xVDND9vqU5J/rAhtFVbwR1tUYPnK4TfuVOOdgeUllD/FxTCNfj\nv/SJc+hHtHg5gdVTvlT82VBiDirYZqs0/uHc8l4wGf4ur4aAwceu3o82vp7dcsq1\nYHAdvvrVEe3LwCOLQUqbtg==\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-7hoe4@eed-website-34a52.iam.gserviceaccount.com",
    "client_id": "116792398322061718024",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-7hoe4%40eed-website-34a52.iam.gserviceaccount.com"
}
# import credentials file
cred = credentials.Certificate(credential)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'eed-website-34a52.appspot.com',
    'databaseURL': 'https://eed-website-34a52-default-rtdb.firebaseio.com/'
})

firestore = firestore.client()

class Admin():


    def get_dashboard_data(self):
        return {
            'inventory': len(firestore.collection(u'alat lab').get()),
            'peminjam alat': len(firestore.collection(u'peminjaman alat').get()),
            'absensi': len(firestore.collection(u'absensi').get())
        }

    def delete_alat_lab(self, id):
        # find key who has the id
        data = firestore.collection('alat lab').where('id', '==', id).get()
        # delete document
        firestore.collection('alat lab').document(data[0].id).delete()
        
    def add_alat_lab(self, nama, jumlah):
        firestore.collection('alat lab').add({
            'id': str(uuid.uuid4()),
            'nama': nama,
            'jumlah': int(jumlah)
        })

    def get_alat_lab(self):
        data = firestore.collection('alat lab').get()
        return [each.to_dict() for each in data]

    def add_absensi_pengunjung(self, nama, npm, bidang, kegiatan, tanggal):
        firestore.collection("absensi").add({
            "nama": nama,
            "npm": npm,
            "bidang": bidang,
            "kegiatan": kegiatan,
            "tanggal": tanggal,
        })

    def get_absensi_pengunjung(self):
        data = firestore.collection("absensi").get()

        return [each.to_dict() for each in data]

    def add_peminjaman_alat(self, nama, npm, wa, namaAlat, jumlah, waktuPeminjaman, waktuPengembalian, message, imgUrl):
        firestore.collection('peminjaman alat').add({
            'id': str(uuid.uuid4()),
            'nama': nama,
            'npm': npm,
            'wa': wa,
            'nama alat': namaAlat,
            'jumlah': int(jumlah),
            'waktu peminjaman': waktuPeminjaman,
            'waktu pengembalian' : waktuPengembalian,
            'message': message,
            'img' : imgUrl
        })
        
    def get_peminjaman_alat(self):
        data = firestore.collection('peminjaman alat').get()
        return [each.to_dict() for each in data]

    def delete_peminjaman_alat(self, id):
        # find key who has the id
        data = firestore.collection('peminjaman alat').where('id', '==', id).get()
        # delete document
        firestore.collection('peminjaman alat').document(data[0].id).delete()
    
    def get_realtime_data(self):
        data = firestore.collection('data pengunjung realtime').get()
        return [each.to_dict() for each in data]

    def delete_pengunjung_realtime(self, id):
        data = firestore.collection('data pengunjung realtime').where('id', '==', id).get()
        firestore.collection('data pengunjung realtime').document(data[0].id).delete()


def upload_img(imgSave, imgUpload):
    bucket = storage.bucket()
    blob = bucket.blob(imgUpload)
    blob.upload_from_filename(imgSave)
    blob.make_public()

    return blob.public_url

def create_realtime_db(data, path):
    ref = db.reference(path)
    ref.update(data)

def get_realtime_db(key, path):
    ref = db.reference(path)
    return ref.get()[key]


# print(get_temp_url())
# create_temp_url()
# print(upload_img('app/websites/static/img/uploads/logo.png', 'logo.png'))
# user = Admin()
# user.delete_peminjaman_alat('d27713bd-05ec-4166-9510-3a0d44605953')
# print(user.get_dashboard_data()['inventory'])
# print(user.delete_alat_lab('7b1eaa25-d45b-4508-b030-c44d03698cfirestore'))
# user.add_alat_lab('opencs', 12)
# user.add_absensi_pengunjung('qadrillah', '2047', 'Teknik Informatika', 'ngoding', '20-05-2020')
# data = user.get_absensi_pengunjung()
