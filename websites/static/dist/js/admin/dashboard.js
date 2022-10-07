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

