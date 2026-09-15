import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyAevG3CK4q6NCbEgiIpiKvoV9iRUnjqzHs",
  authDomain: "challengesiliconshoring.firebaseapp.com",
  projectId: "challengesiliconshoring",
  storageBucket: "challengesiliconshoring.firebasestorage.app",
  messagingSenderId: "490003124801",
  appId: "1:490003124801:web:790ebdaa28896df9226cc0"
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);