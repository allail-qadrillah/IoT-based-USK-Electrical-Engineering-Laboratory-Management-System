import firebase_admin
from firebase_admin import credentials, firestore, storage, db
import uuid

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
cred = credentials.Certificate(credential)
firebase_admin.initialize_app(cred, {
    'storageBucket': '',
    'databaseURL': ''
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