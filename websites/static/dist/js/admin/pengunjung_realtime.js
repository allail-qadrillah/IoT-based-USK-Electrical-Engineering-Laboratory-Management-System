import { initializeApp } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-app.js";
const firebaseApp = initializeApp({
  apiKey: "",
  authDomain: "",
  databaseURL: "",
  projectId: "",
  storageBucket: "",
  messagingSenderId: "",
  appId: "",
  measurementId: ""
});

import { getDatabase, ref, onValue, get, update } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-database.js";
const db = getDatabase()
// update data
onValue(ref(db, '/'), (snapshot) => {
  const data = snapshot.val();

  const status = data['raspberry_server'];
  var lampuOtomatis = data['lampu_otomatis'] ? document.getElementById('lampu-otomatis').innerHTML = 'Matikan Lampu Otomatis ⚙️' : document.getElementById('lampu-otomatis').innerHTML = 'Hidupkan Lampu Otomatis ⚙️'
  var lampuOtomatis = data['lampu_otomatis'] ? document.getElementById('lampu-otomatis').className = 'btn btn-danger mb-4' : document.getElementById('lampu-otomatis').className = 'btn btn-success mb-4'
  var lampu = data['lampu'] ? document.getElementById('lampu').innerHTML = 'Hidup 💡' : document.getElementById('lampu').innerHTML = 'Mati 💡'
  var lampu = data['lampu'] ? document.getElementById('lampu').className = 'btn btn-success' : document.getElementById('lampu').className = 'btn btn-danger'
  

  if (status == true) {
    document.getElementById('pengunjung-lab').innerHTML = data['pengunjung_lab'];
  } else {
    document.getElementById('pengunjung-lab').innerHTML = '0';
  }
});

function updateBtnStatus(namaBtn) {
  get(ref(db, '/')).then((snapshot) => {
    const status = snapshot.val()[namaBtn]

    if (status) {
      update(ref(db, '/'), {
        [namaBtn]: false
      })
    } else {
      update(ref(db, '/'), {
        [namaBtn]: true
      })
    }

  })
}

window.changeStatus = (lampu) => {
  if (lampu == 'lampuOtomatis') {
    updateBtnStatus('lampu_otomatis')
    console.log("otomatis")
  } else {
    updateBtnStatus('lampu')
    console.log("manual")
  }
}