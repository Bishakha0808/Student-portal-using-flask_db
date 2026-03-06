# Student-portal-using-flask_db
To develop an application for user authentication and document sharing for student using mysql workbench 8.0.45
A student portal built with **Flask + MySQL** featuring user authentication, profile management, and grade viewing.


---

## Features

- User **Sign Up** with duplicate-username check
- Secure **Login** using hashed passwords (Werkzeug)
- **Dashboard** showing email, grade (read-only), and password reset
- **Update Email** profile page
- Flash messages for all user actions
- Bootstrap 5 responsive UI

---

## Project Structure

```
├── app.py                  # Flask application
├── SQL.sql                 # Database schema
├── requirements.txt        # Python dependencies
└── templates/
    ├── login.html
    ├── signup.html
    ├── dashboard.html
    ├── update.html
    └── static/
        └── style.css
```

---

## Setup

### 1. Install dependencies
```bash
pip install flask flask-mysqldb
```

### 2. Create the database
Open **MySQL Workbench** and run `SQL.sql`:
```sql
CREATE DATABASE IF NOT EXISTS flask_db;
USE flask_db;

CREATE TABLE IF NOT EXISTS users (
    id       INT          AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50)  NOT NULL UNIQUE,
    email    VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    grade    VARCHAR(10)  DEFAULT NULL
);
```

### 3. Configure MySQL credentials
Edit `app.py` and set your MySQL root password:
```python
app.config['MYSQL_PASSWORD'] = 'your_password_here'
```

### 4. Run the app
```bash
python app.py
```
Open `http://127.0.0.1:5000` in your browser.

---

## Assigning Grades (Admin only)

Students cannot edit their own grades. Run this in MySQL:
```sql
UPDATE users SET grade = 'A' WHERE username = 'student_name';
```

---

## Tech Stack

| Layer    | Technology          |
|----------|---------------------|
| Backend  | Python 3, Flask     |
| Database | MySQL, flask-mysqldb|
| Security | Werkzeug (bcrypt)   |
| Frontend | Bootstrap 5, CSS3   |
