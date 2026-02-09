import subprocess
import sys, os, time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

services = [
    ("auth_service", "app.py", 5000),
    ("article_service", "app.py", 5001),
    ("banque_service", "app.py", 5003),
    ("lecteur_service", "app.py", 5002),
]

processes = []

def run_service(folder, script, port):
    folder_path = os.path.join(BASE_DIR, folder)
    script_path = os.path.join(folder_path, script)
    print(f"Lancement de {folder} sur le port {port}…")
    return subprocess.Popen([sys.executable, script_path], cwd=folder_path, shell=False)

try:
    for folder, script, port in services:
        p = run_service(folder, script, port)
        processes.append(p)
        time.sleep(1)

    print("\nTous les services sont lancés ! Accès : http://localhost:5000\n")
    for p in processes:
        p.wait()
except KeyboardInterrupt:
    print("\nArrêt des services…")
    for p in processes:
        p.terminate()
