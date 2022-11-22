from flask import Blueprint, render_template, redirect, url_for, request
from .models import Admin, upload_img, create_realtime_db
from websites import app
import os
import datetime
from werkzeug.utils import secure_filename

admin_views = Blueprint('admin_views', __name__)


@admin_views.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    return render_template('admin/dashboard.html', data=Admin().get_dashboard_data())

@admin_views.route('/peminjaman', methods=['POST', 'GET'])
def peminjaman():
    # get data from database
    dataPeminjam = Admin().get_peminjaman_alat()
    if request.method == "POST":
        if request.files:
            image = request.files['image']
            path  = app.config['IMAGE_UPLOADS']
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
        waktuPengembalian    = request.form['time'].replace('T', ' ')
        message  = request.form['message']

        Admin().add_peminjaman_alat(nama, npm, wa, namaAlat, jumlah, waktuPeminjaman, waktuPengembalian, message, img_url)
        # delete files from local directory
        os.remove(f"{path}/{filename}")

        return redirect(url_for('admin_views.peminjaman'))

    return render_template('admin/peminjaman_alat.html', active='Peminjaman', dataPeminjam = dataPeminjam)

@admin_views.route('/peminjaman/delete/<id>')
def delete_peminjaman(id):
    Admin().delete_peminjaman_alat(id)
    return redirect(url_for('admin_views.peminjaman'))

#  ALAT LAB
@admin_views.route('/alat-lab', methods=['POST', 'GET'])
def alat_lab():
    if request.method == 'POST':
        jumlah = request.form['jumlah']
        nama_alat = request.form['nama_alat']

        Admin().add_alat_lab(nama_alat, jumlah)
        return redirect(url_for('admin_views.alat_lab'))

    data_alat_lab = Admin().get_alat_lab()
    return render_template('admin/alat_lab.html',  active='Peminjaman', data_alat_lab = data_alat_lab)

@admin_views.route('/alat-lab/delete/<id>')
def delete_alat_lab(id):
    Admin().delete_alat_lab(id)
    return redirect(url_for('admin_views.alat_lab'))

#  ABSENSI PENGUNJUNG
@admin_views.route('/absensi-pengunjung')
def absensi_pengunjung():
    data_absensi = Admin().get_absensi_pengunjung()

    return render_template('admin/absensi_pengunjung.html', data_absensi=data_absensi)

@admin_views.route('/pengunjung-realtime', methods=['POST', 'GET'])
def pengunjung_realtime():
    if request.method == 'POST':
        create_realtime_db({'action_take_foto' : True}, '/')
        
        return redirect(url_for('admin_views.pengunjung_realtime'))
    data = Admin().get_realtime_data()

    from time import sleep
    sleep(5)
    return render_template('admin/pengunjung_realtime.html', data_realtime = data)


@admin_views.route('/pengunjung-realtime/delete/<id>', methods=['POST', 'GET'])
def delete_pengunjung_realtime(id):
    Admin().delete_pengunjung_realtime(id)
    return redirect(url_for('admin_views.pengunjung_realtime'))


@admin_views.route('/api')
def api():
    return "aktif"
