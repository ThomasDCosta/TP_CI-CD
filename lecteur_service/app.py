from flask import Flask, request, jsonify, Response, redirect, url_for, render_template
from functools import wraps
import json
import sqlite3
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
import pybreaker
import random
import time

app = Flask(__name__)



@app.route('/panier', methods=['POST'])
def articles():
    token = request.form.get('token')
    username = token.split("_")[0]

    # Un seul film (radio)
    film = request.form.get('film')

    articles_nouveaux = []
    if film:
        articles_nouveaux.append(film)

    return render_template(
        'lecteur.html',
        articles=articles_nouveaux,
        username=username,
        token=token
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002)
