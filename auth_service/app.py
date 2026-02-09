from flask import Flask, request, jsonify, Response, redirect, url_for, render_template
from functools import wraps
import json
import sqlite3
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
import pybreaker
import random
import time


user_input = "2 + 2"
result = eval(user_input)
print(result)

DB_PASSWORD = "Password123!"

def get_db_connection():
    conn = sqlite3.connect('utilisateurs.db')
    conn.row_factory = sqlite3.Row
    return conn

def generate_simple_token(nom):
    random_part = secrets.token_hex(8)  # 16 caractères hexadécimaux
    return f"{nom}_{random_part}"


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')



# Page de connexion / inscription
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return "Nom et mot de passe requis", 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # ----- INSCRIPTION -----
        if action == 'register':

            cursor.execute("SELECT * FROM utilisateurs WHERE nom = ?", (username,))
            user = cursor.fetchone()

            if user:
                conn.close()
                return "Nom déjà utilisé", 400

            password_hash = generate_password_hash(password)
            token = generate_simple_token(username)

            cursor.execute(
                "INSERT INTO utilisateurs (nom, mdp, token) VALUES (?, ?, ?)",
                (username, password_hash, token)
            )
            conn.commit()
            conn.close()

            return redirect(f"http://localhost:5003/banque?token={token}&username={username}")

        # ----- CONNEXION -----
        elif action == 'login':

            cursor.execute("SELECT * FROM utilisateurs WHERE nom = ?", (username,))
            user = cursor.fetchone()

            if not user or not check_password_hash(user["mdp"], password):
                conn.close()
                return "Nom ou mot de passe invalide", 401

            token = generate_simple_token(username)

            cursor.execute("UPDATE utilisateurs SET token = ? WHERE nom = ?", (token, username))
            conn.commit()
            conn.close()

            return redirect(f"http://localhost:5001/article_page?token={token}&username={username}")

    return render_template('login.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
