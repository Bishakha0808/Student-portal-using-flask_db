from flask import Flask, render_template, request, redirect, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

# Static files live in templates/static/ to match the existing project layout
app = Flask(__name__, static_folder='templates/static', static_url_path='/static')
app.secret_key = "change_this_in_production"   # Use os.urandom(24) in production

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Bb#2004@'        # ← put your MySQL root password here
app.config['MYSQL_DB'] = 'flask_db'

mysql = MySQL(app)


# ── Home / Login page ────────────────────────────────────────────────────────
@app.route('/')
def login():
    if 'username' in session:
        return redirect('/dashboard')
    return render_template('login.html')


# ── Signup ────────────────────────────────────────────────────────────────────
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email    = request.form['email'].strip()
        password = generate_password_hash(request.form['password'])

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM users WHERE username = %s", [username])
        if cur.fetchone():
            cur.close()
            flash('Username already taken. Please choose another.', 'danger')
            return render_template('signup.html')

        cur.execute(
            "INSERT INTO users(username, email, password) VALUES(%s, %s, %s)",
            (username, email, password)
        )
        mysql.connection.commit()
        cur.close()
        flash('Account created! You can now log in.', 'success')
        return redirect('/')

    return render_template('signup.html')


# ── Login authentication ──────────────────────────────────────────────────────
@app.route('/login', methods=['POST'])
def login_user():
    username = request.form['username'].strip()
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT password FROM users WHERE username = %s", [username])
    row = cur.fetchone()
    cur.close()

    if row and check_password_hash(row[0], password):
        session['username'] = username
        return redirect('/dashboard')

    flash('Invalid username or password.', 'danger')
    return redirect('/')


# ── Dashboard ─────────────────────────────────────────────────────────────────
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')

    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT email, grade FROM users WHERE username = %s",
        [session['username']]
    )
    row = cur.fetchone()
    cur.close()

    email = row[0] if row else ''
    grade = row[1] if row else 'N/A'
    return render_template('dashboard.html', grade=grade, email=email)


# ── Update email ──────────────────────────────────────────────────────────────
@app.route('/update', methods=['GET', 'POST'])
def update():
    if 'username' not in session:
        return redirect('/')

    if request.method == 'POST':
        email = request.form['email'].strip()
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE users SET email = %s WHERE username = %s",
            (email, session['username'])
        )
        mysql.connection.commit()
        cur.close()
        flash('Email updated successfully!', 'success')
        return redirect('/dashboard')

    cur = mysql.connection.cursor()
    cur.execute("SELECT email FROM users WHERE username = %s", [session['username']])
    row = cur.fetchone()
    cur.close()
    current_email = row[0] if row else ''
    return render_template('update.html', current_email=current_email)


# ── Reset password ────────────────────────────────────────────────────────────
@app.route('/reset', methods=['POST'])
def reset():
    if 'username' not in session:
        return redirect('/')

    hashed = generate_password_hash(request.form['password'])
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE users SET password = %s WHERE username = %s",
        (hashed, session['username'])
    )
    mysql.connection.commit()
    cur.close()
    flash('Password reset successfully!', 'success')
    return redirect('/dashboard')


# ── Logout ────────────────────────────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)