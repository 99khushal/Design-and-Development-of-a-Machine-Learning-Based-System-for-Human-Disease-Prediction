import streamlit as st
import numpy as np
import pickle
import matplotlib.pyplot as plt
import sqlite3
import hashlib

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Disease Prediction", page_icon="🩺")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS history (user TEXT, disease TEXT, result TEXT)")
conn.commit()

# ---------------- PASSWORD HASH ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- AUTH ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def register():
    st.title("📝 Register")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Register"):
        c.execute("INSERT INTO users VALUES (?,?)", (user, hash_password(pwd)))
        conn.commit()
        st.success("Account Created ✅")

def login():
    st.title("🔐 Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        c.execute("SELECT * FROM users WHERE username=? AND password=?",
                  (user, hash_password(pwd)))
        if c.fetchone():
            st.session_state.logged_in = True
            st.session_state.user = user
            st.success("Login Successful ✅")
            st.rerun()
        else:
            st.error("Invalid Credentials ❌")

# ---------------- LOGIN MENU ----------------
menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

if not st.session_state.logged_in:
    if choice == "Login":
        login()
    else:
        register()
    st.stop()

# ---------------- DARK UI ----------------
st.markdown("""
<style>
.main {background-color:#0f172a;}
h1 {color:#38bdf8; text-align:center;}
h3 {color:#e2e8f0; text-align:center;}
label {color:white !important;}
.stButton>button {
background: linear-gradient(90deg,#38bdf8,#6366f1);
color:white; border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1>🩺 Multi Disease Prediction System</h1>", unsafe_allow_html=True)
st.markdown("<h3>AI-Based Smart Health Analyzer</h3>", unsafe_allow_html=True)
st.write("---")

# ---------------- LOAD MODELS ----------------
diabetes_model = pickle.load(open("model/diabetes_model.pkl","rb"))
heart_model = pickle.load(open("model/heart_model.pkl","rb"))
parkinsons_model = pickle.load(open("model/parkinsons_model.pkl","rb"))

# ---------------- SIDEBAR ----------------
st.sidebar.success(f"👤 {st.session_state.user}")
disease = st.sidebar.radio("Select Disease",
                           ["Diabetes","Heart Disease","Parkinson’s"])

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# ---------------- ADMIN PANEL ----------------
if st.session_state.user == "admin":
    st.sidebar.subheader("👑 Admin Panel")

    if st.sidebar.button("View Users"):
        st.write(c.execute("SELECT username FROM users").fetchall())

    if st.sidebar.button("View History"):
        st.write(c.execute("SELECT * FROM history").fetchall())

# ---------------- DIABETES ----------------
if disease == "Diabetes":
    st.subheader("Enter Details")

    preg = st.number_input("Pregnancies")
    glucose = st.number_input("Glucose")
    bp = st.number_input("BP")
    skin = st.number_input("Skin")
    insulin = st.number_input("Insulin")
    bmi = st.number_input("BMI")
    dpf = st.number_input("DPF")
    age = st.number_input("Age")

    if st.button("Predict"):
        data = np.array([[preg,glucose,bp,skin,insulin,bmi,dpf,age]])
        result = diabetes_model.predict(data)
        prob = diabetes_model.predict_proba(data)

        res = "High Risk" if result[0]==1 else "Low Risk"
        st.write(res)

        c.execute("INSERT INTO history VALUES (?,?,?)",
                  (st.session_state.user,"Diabetes",res))
        conn.commit()

        fig, ax = plt.subplots()
        ax.bar(["No","Yes"], prob[0])
        st.pyplot(fig)

# ---------------- HEART ----------------
elif disease == "Heart Disease":
    st.subheader("Enter Details")

    age = st.number_input("Age")
    sex = st.selectbox("Sex",["Male","Female"])
    cp = st.number_input("CP")
    trestbps = st.number_input("BP")
    chol = st.number_input("Chol")
    fbs = st.selectbox("FBS",[0,1])
    restecg = st.number_input("ECG")
    thalach = st.number_input("HR")
    exang = st.selectbox("Angina",[0,1])
    oldpeak = st.number_input("Oldpeak")
    slope = st.number_input("Slope")
    ca = st.number_input("CA")
    thal = st.number_input("Thal")

    if st.button("Predict"):
        data = np.array([[age,1 if sex=="Male" else 0,cp,trestbps,chol,
                          fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]])

        result = heart_model.predict(data)
        prob = heart_model.predict_proba(data)

        res = "High Risk" if result[0]==1 else "Low Risk"
        st.write(res)

        c.execute("INSERT INTO history VALUES (?,?,?)",
                  (st.session_state.user,"Heart",res))
        conn.commit()

        fig, ax = plt.subplots()
        ax.bar(["No","Yes"], prob[0])
        st.pyplot(fig)

# ---------------- PARKINSON ----------------
else:
    st.subheader("Enter Details")

    fo = st.number_input("Fo")
    fhi = st.number_input("Fhi")
    flo = st.number_input("Flo")
    jitter = st.number_input("Jitter")
    jitter_abs = st.number_input("Jitter Abs")
    rap = st.number_input("RAP")
    ppq = st.number_input("PPQ")
    ddp = st.number_input("DDP")
    shimmer = st.number_input("Shimmer")
    shimmer_db = st.number_input("Shimmer dB")
    apq3 = st.number_input("APQ3")
    apq5 = st.number_input("APQ5")
    apq = st.number_input("APQ")
    dda = st.number_input("DDA")
    nhr = st.number_input("NHR")
    hnr = st.number_input("HNR")
    rpde = st.number_input("RPDE")
    dfa = st.number_input("DFA")
    spread1 = st.number_input("Spread1")
    spread2 = st.number_input("Spread2")
    d2 = st.number_input("D2")
    ppe = st.number_input("PPE")

    if st.button("Predict"):
        data = np.array([[fo,fhi,flo,jitter,jitter_abs,rap,ppq,ddp,
                          shimmer,shimmer_db,apq3,apq5,apq,dda,
                          nhr,hnr,rpde,dfa,spread1,spread2,d2,ppe]])

        result = parkinsons_model.predict(data)
        prob = parkinsons_model.predict_proba(data)

        res = "High Risk" if result[0]==1 else "Low Risk"
        st.write(res)

        c.execute("INSERT INTO history VALUES (?,?,?)",
                  (st.session_state.user,"Parkinson",res))
        conn.commit()

        fig, ax = plt.subplots()
        ax.bar(["No","Yes"], prob[0])
        st.pyplot(fig)