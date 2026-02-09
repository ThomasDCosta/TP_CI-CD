.PHONY: all down build up
# dit en gros que ce qui suit sont des commandes et non des fichiers
 
 
 
#//////////////////////////////////////////////////////////
DC=docker compose
URL=http://127.0.0.1:5000
#//////////////////////////////////////////////////////////
 
 
lancement: down build scan up open
rapport-erreur: trivy rapport-json conversion affichage-rapport
down:
    $(DC) down -v
 
build:
    $(DC) build
 
# -d sur up pour qu'il ne reste pas par défault en premier plan
up:
    $(DC) up -d
 
open:
    @open $(URL) || open $(URL)
 
 
# génère un rapport html de chaque vulnérabilitées sur les 4 images docker
trivy:
    @trivy image --format json -o report-auth.json devops-auth:latest
    @trivy image --format json -o report-article.json devops-article:latest
    @trivy image --format json -o report-banque.json devops-banque:latest
    @trivy image --format json -o report-panier.json devops-panier:latest
 
rapport-json:
    @for img in devops-banque:latest devops-auth:latest devops-panier:latest devops-article:latest; do \
        file_name=$$(echo $$img | tr ':/' '--').json; \
        echo "Scanning $$img → $$file_name"; \
        trivy image --format json -o "$$file_name" "$$img"; \
    done
 
conversion:
    python3 conversion\ json-py.py  
 
affichage-rapport:
    open report.html   