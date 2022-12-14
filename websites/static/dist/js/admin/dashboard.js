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

import { getDatabase, ref, onValue } from "https://www.gstatic.com/firebasejs/9.10.0/firebase-database.js";
const db = getDatabase()
// update data
onValue(ref(db, '/'), (snapshot) => {
  const data = snapshot.val();

  const status = data['raspberry_server'];


  if (status == true) {
    document.getElementById('raspberry-status').innerHTML = "Aktif";
    document.getElementById('pengunjung-lab').innerHTML = data['pengunjung_lab'];
    document.getElementById('class-raspberry-server').className = 'small-box bg-success';
  } else {
    document.getElementById('raspberry-status').innerHTML = "Non Aktif";
    document.getElementById('pengunjung-lab').innerHTML = '0';
    document.getElementById('class-raspberry-server').className = 'small-box bg-danger';
  }
});

