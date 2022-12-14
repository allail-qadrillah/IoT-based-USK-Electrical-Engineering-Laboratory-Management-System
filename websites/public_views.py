from flask import Blueprint, render_template, request, request
from .models import Admin, create_realtime_db, get_realtime_db, upload_img
import os
from websites import app
import datetime
from flask_uuid import uuid
from werkzeug.utils import secure_filename
from threading import Timer

public_views = Blueprint('public_views', __name__)
url_access = []
ip_access = {}

@public_views.route('/')
def index():
    return render_template('public/index.html', data_alat_lab=Admin().get_alat_lab())

# QRCODE JALAN DI SERVER BERBEDA
@public_views.route(f'/QRCode', methods=['GET', 'POST'])
def QRCode():
    # create url uuid
    create_realtime_db(
        {'temp_url': f"{get_realtime_db('baseUrlAbsensi', '/')}{str(uuid.uuid4())}"}, '/')

    return render_template('public/QRCode.html',)

@public_views.route('/absensi/<uuid(strict=True):id>', methods=['GET', 'POST'])
def form_absensi(id):
    ipAddress = request.headers['X-Forwarded-For']
    time = datetime.datetime.now()
    # Check url acces
    if id in url_access:
        return render_template('public/message.html', text = 'Url Expired 💀')
    if ipAddress in ip_access:
        return render_template('public/message.html', text = f"Device anda dengan IP {ipAddress} sudah melakukan Absensi.")
  
    else:
        ip_access[ipAddress] = time
    
        Timer(120, ip_access.pop, args=[ipAddress]).start()
        url_access.append(id)
      
        # create url uuid
        create_realtime_db({'temp_url': f"{get_realtime_db('baseUrlAbsensi', '/')}{str(uuid.uuid4())}"}, '/')

        return render_template('public/absensi.html')
    
@public_views.route('/absensi', methods=['GET', 'POST'])
def absensi():
    if request.method == 'POST':
        nama       = request.form['nama']
        npm        = request.form['npm']
        bidang     = request.form['bidang']
        kegiatan   = request.form['kegiatan']
        time       = request.form['time'].replace('T', ' ')

        Admin().add_absensi_pengunjung(nama, npm, bidang, kegiatan, time)

        return render_template('public/add_data_complete.html', success=True)

@public_views.route('/pinjam-alat', methods=['GET', 'POST'])
def pinjam_alat():
    if request.method == "POST":
        if request.files:
            image = request.files['image']
            path = app.config['IMAGE_UPLOADS']
            filename = secure_filename(image.filename)
            
            if filename != '':
                # save and upload file
                image.save(os.path.join(path, filename))
                img_url = upload_img(f"{path}/{filename}", f'image alat/{filename}')
            else: return "file tidak dapat di upload :("
        # get data form
        nama = request.form['nama']
        npm  = request.form['npm']
        wa   = request.form['wa']
        namaAlat = request.form['nama-alat']
        jumlah   = request.form['jumlah']
        waktuPeminjaman = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        waktuPengembalian = request.form['time'].replace('T', ' ')
        message  = request.form['message']

        Admin().add_peminjaman_alat(nama, npm, wa, namaAlat, jumlah, waktuPeminjaman, waktuPengembalian, message, img_url)
        # delete files from local directory
        os.remove(f"{path}/{filename}")
        return render_template('public/add_data_complete.html', success=True)
        

    return render_template('public/pinjam_alat.html')