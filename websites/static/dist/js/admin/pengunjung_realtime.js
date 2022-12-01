import { initializeApp } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-app.js";
const firebaseApp = initializeApp({
  apiKey: "AIzaSyCBDhVoR-6MrrXpVA1es7JZnBc-o1CXSAo",
  authDomain: "eed-website-34a52.firebaseapp.com",
  databaseURL: "https://eed-website-34a52-default-rtdb.firebaseio.com",
  projectId: "eed-website-34a52",
  storageBucket: "eed-website-34a52.appspot.com",
  messagingSenderId: "698112175231",
  appId: "1:698112175231:web:13701c78b3ba091f37a34a",
  measurementId: "G-BVYHW2XCL6"
});

import { getDatabase, ref, onValue, get, update } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-database.js";
const db = getDatabase()
// update data
onValue(ref(db, '/'), (snapshot) => {
  const data = snapshot.val();

  const status = data['raspberry_server'];
  var lampuOtomatis = data['lampu_otomatis'] ? document.getElementById('lampu-otomatis').innerHTML = 'Matikan Lampu Otomatis' : document.getElementById('lampu-otomatis').innerHTML = 'Hidupkan Lampu Otomatis'
  var lampuOtomatis = data['lampu_otomatis'] ? document.getElementById('lampu-otomatis').className = 'btn btn-danger mb-4' : document.getElementById('lampu-otomatis').className = 'btn btn-success mb-4'
  var lampu = data['lampu'] ? document.getElementById('lampu').innerHTML = 'Hidup' : document.getElementById('lampu').innerHTML = 'Mati'
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