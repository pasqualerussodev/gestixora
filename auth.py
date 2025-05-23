import sqlite3
import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
from forms import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password_hash = generate_password_hash(form.password.data)
        created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = db.get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
                (username, password_hash, created_at)
            )
            conn.commit()
            flash("Registrazione completata. Ora puoi effettuare il login.", "success")
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            flash("Username già in uso.", "danger")
        finally:
            conn.close()
    return render_template("register.html", form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        conn = db.get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password_hash'], form.password.data):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash("Accesso effettuato con successo.", "success")
            return redirect(url_for('index'))
        else:
            flash("Credenziali non valide.", "danger")
    return render_template("login.html", form=form)

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Sei stato disconnesso.", "info")
    return redirect(url_for('auth.login'))
