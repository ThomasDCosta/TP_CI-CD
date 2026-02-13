from flask import Flask, request, jsonify, Response, redirect, url_for, render_template
from functools import wraps
import json
import sqlite3
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
import pybreaker
import random
import time
import requests
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

MICROSERVICES = {
    "article_service": "http://article-service:5001/health",
    "auth_service": "http://auth-service:5000/health",
    "banque_service": "http://banque-service:5003/health"
}

@app.route('/health', methods=['GET'])
def health():
    results = {}
    overall_status = "healthy"

    for name, url in MICROSERVICES.items():
        try:
            resp = requests.get(url, timeout=2)
            if resp.status_code == 200:
                results[name] = {"status": "healthy"}
            else:
                results[name] = {"status": "unhealthy", "code": resp.status_code}
                overall_status = "unhealthy"
        except Exception as e:
            results[name] = {"status": "unhealthy", "error": str(e)}
            overall_status = "unhealthy"

    # Retourne le statut global
    status_code = 200 if overall_status == "healthy" else 503
    return jsonify({"status": overall_status, "services": results}), status_code


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True,threaded=True)
