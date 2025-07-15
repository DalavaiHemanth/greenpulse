from flask import Flask, render_template, redirect, request, session, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd
import pickle
import random
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- User model ---
class User(UserMixin):
    def __init__(self, id_, username, password_hash):
        self.id = id_
        self.username = username
        self.password_hash = password_hash

    def get_id(self):
        return str(self.id)

def get_user_by_username(username):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT id, username, password FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()
    if row:
        return User(*row)
    return None

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute("SELECT id, username, password FROM users WHERE id=?", (user_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return User(*row)
    return None

# --- Routes ---

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_hash))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return 'Username already exists'
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/energy')
@login_required
def energy_api():
    data = get_live_data()
    prediction = model.predict([[data['usage']]])[0]
    overuse = bool(prediction)
    tip = get_tip(overuse)
    return jsonify({
        'data': data,
        'overuse': overuse,
        'tip': tip
    })

@app.route('/api/history')
@login_required
def history_data():
    try:
        df = pd.read_csv('data/usage_data.csv').tail(20)
        return jsonify({
            'labels': list(range(len(df))),
            'values': df['usage'].tolist()
        })
    except Exception as e:
        return jsonify({'error': str(e)})

# --- Energy Usage Simulation ---
def get_live_data():
    usage = round(random.uniform(0.5, 3.0), 2)
    device = 'Air Conditioner'
    record = {'device': device, 'usage': usage}
    os.makedirs('data', exist_ok=True)
    csv_file = 'data/usage_data.csv'
    df = pd.DataFrame([record])
    if os.path.exists(csv_file):
        df.to_csv(csv_file, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_file, index=False)
    return record

def get_tip(overuse):
    return "Try setting your AC to 24°C for efficiency." if overuse else "Your power usage is optimal!"

# --- Load ML Model ---
with open('model/predictor.pkl', 'rb') as f:
    model = pickle.load(f)

# --- DB Init ---
def init_db():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

