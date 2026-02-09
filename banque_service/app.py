from flask import Flask, request, render_template
import random, time

app = Flask(__name__)

def appeler_banque(nom):
    # Simulation d’un temps de réponse
    duree = random.uniform(1.5, 3)
    time.sleep(duree)
    return f"Transaction simulée réussie pour {nom} en {duree:.2f}s"

@app.route('/banque', methods=['GET', 'POST'])
def banque():
    # Support GET pour la redirection depuis l'inscription
    if request.method == 'POST':
        nom = request.form.get('nom') or request.form.get('username')
        token = request.form.get('token')
    else:
        nom = request.args.get('nom') or request.args.get('username')
        token = request.args.get('token')

    if not nom:
        return "Nom utilisateur manquant", 400

    # Simulation paiement
    resultat = appeler_banque(nom)

    return render_template('banque.html', nom=nom, resultat=resultat, token=token)
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003)
