from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/article_page', methods=['GET', 'POST'])
def article_page():
    # Récupération du token (GET ou POST)
    token = request.args.get('token') or request.form.get('token')

    # Sécurisation minimale
    if not token or "_" not in token:
        return "Token invalide ou manquant", 400

    # Extraction du username depuis le token
    username = token.split("_")[0]

    return render_template(
        'article.html',
        username=username,
        token=token
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
