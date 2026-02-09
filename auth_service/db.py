import sqlite3

# Chemin vers la base de données utilisée par ton Flask app
db_path = 'utilisateurs.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Créer la table utilisateurs si elle n'existe pas
cursor.execute("""
CREATE TABLE IF NOT EXISTS utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL UNIQUE,
    mdp TEXT NOT NULL,
    token TEXT
);
""")

conn.commit()
conn.close()

print("Table 'utilisateurs' créée ou déjà existante avec succès.")
