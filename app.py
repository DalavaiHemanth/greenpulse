from flask import Flask, render_template, request, redirect, session
import sqlite3
import hashlib
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace this

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ? AND password = ?",
                  (email, hash_password(password)))
        user = c.fetchone()
        conn.close()

        if user:
            session['user'] = email
            return redirect('/dashboard')
        else:
            error = 'Invalid email or password.'
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Gmail-only validation
        if not re.match(r'^[\w\.-]+@gmail\.com$', email):
            error = 'Only Gmail addresses are allowed.'
        else:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE email = ?", (email,))
            if c.fetchone():
                error = 'Email already registered.'
            else:
                c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                          (username, email, hash_password(password)))
                conn.commit()
                conn.close()
                return redirect('/login')
    return render_template('register.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return f"<h2>Welcome to GreenPulse Dashboard, {session['user']}</h2>"
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
