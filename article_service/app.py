from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/article_page', methods=['GET', 'POST'])
def article_page():
    token = request.args.get('token')

    # Sécurisation : si pas de token → accès refusé
    if not token or "_" not in token:
        return "Token invalide", 400

    # Extraction du username depuis le token
    username = token.split("_")[0]

    return render_template('article.html', username=username, token=token)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "service": "article_service",
        "status": "OK"
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
