from model import *
from time import sleep
import datetime
import uuid
import cv2
import os
import atexit
import threading
from pyfirmata import Arduino

## Algoritma Ambil Gambar dengan Trigger Perintah dari Website
board = Arduino("COM11")
pinLampu = board.get_pin('d:13:o')

hidup = 1
mati = 0

pinLampu.write(hidup)

# Create our body classifier-
face_classifier = cv2.CascadeClassifier(
    'clasifier/haarcascade_frontalface.xml')
# face_classifier = cv2.CascadeClassifier(
#     'clasifier/haarcascade_fullbody.xml')

cap = cv2.VideoCapture(0)

## 2. Function Trigger Listen action_take_foto dari Realtime Database
@ignore_first_call
def listener_take_foto(event):
    global TAKE_IMAGE
    value = event.data
    ## 2. Jika action_take_foto = True => ubah variabel TAKE_IMAGE menjadi True
    if value == True:
        TAKE_IMAGE = True


@ignore_first_call
def listener_lampu(event):
    global LAMPU, LAMPU_OTOMATIS
    value = event.data
    ## 2. Jika action_take_foto = True => ubah variabel TAKE_IMAGE menjadi True
    if value == True:
        # if LAMPU_OTOMATIS == False:
            LAMPU = True
            print('Lampu Hidup')
            pinLampu.write(hidup)

    else:
        LAMPU = False
        print('Lampu mati')
        pinLampu.write(mati)



@ignore_first_call
def listener_lampu_otomatis(event):
    global LAMPU_OTOMATIS
    value = event.data
    print('Lampu otomatis = ', value)
    LAMPU_OTOMATIS = value

def lampuOtomatis(args):
    print(f'otomatis hidup {args}')

def open_camera(cap):
    # Variabel Control Ambil Gambar
    global TAKE_IMAGE, LAMPU, LAMPU_OTOMATIS
    TAKE_IMAGE = False
    LAMPU_OTOMATIS = False
 

    while True:
        
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5,
                            interpolation=cv2.INTER_LINEAR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        bodies = face_classifier.detectMultiScale(gray, 1.2, 3)
    
        # Buat bonding box dan masukkan jumlah body yang terdeteksi ke database
        for (x, y, w, h) in bodies:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        # cv2.imshow('Frame', frame)
        t1 = threading.Thread(target=create_realtime_db,
                                args=({'pengunjung_lab': len(bodies)}, '/', ))
        t1.start()
        
        ## 3. Listen Variabel dari TAKE_IMAGE => Jika True maka ambil gambar
        if TAKE_IMAGE:
            print('ambil gambar')
            ## 4. ubah Variabel pengambilan gambar ke False
            TAKE_IMAGE = False
            create_realtime_db({'action_take_foto': False}, '/')

            ## 5. Ambil gambar dari kamera dan simpan Temporary ke folder lalu upload ke Cloud Storage
            id = str(uuid.uuid5(uuid.NAMESPACE_DNS,
                                str(datetime.datetime.now())))
            path = f'img/{id}.jpg'

            cv2.imwrite(path, frame)

            # create firestore database and upload to Cloud Storage
            firestore.collection('data pengunjung realtime').add({
                'id': id,
                'jam': datetime.datetime.now().strftime("%H:%M"),
                'tanggal': datetime.datetime.now().strftime("%Y-%m-%d"),
                'img': upload_img(path, f'realtime img/{id}')
            })

            ## 6. Hapus Gambar 
            os.remove(path)
        
        if LAMPU_OTOMATIS:

            if len(bodies) > 0:
                print('lampuu hidup')
                pinLampu.write(hidup)
            else:
                print('lampu mati')
                pinLampu.write(mati)

        elif cv2.waitKey(1) == 27:
            break
        
    t1.join()
    cap.release()
    cv2.destroyAllWindows()
    atexit.register(on_stop)



if __name__ == '__main__':
    create_realtime_db({'raspberry_server': True}, '/')

    ## 1. Listen database action_take_foto
    print('action_take_foto listened')
    db.reference('/action_take_foto').listen(listener_take_foto)
    db.reference('/lampu').listen(listener_lampu)
    db.reference('/lampu_otomatis').listen(listener_lampu_otomatis)

    print('Camera Opened')
    open_camera(cap) 

    atexit.register(on_stop)
