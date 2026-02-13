.PHONY: all down build up
# dit en gros que ce qui suit sont des commandes et non des fichiers



#//////////////////////////////////////////////////////////
DC=docker compose
URL=http://127.0.0.1:5000
#//////////////////////////////////////////////////////////

lancement: down build up open
rapport-erreur: rapport-json conversion affichage-rapport

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

rapport-json:
	@mkdir -p rapports_json
	@for img in devops-banque:latest devops-auth:latest devops-panier:latest devops-article:latest; do \
		file_name=$$(echo $$img | tr ':/' '--').json; \
		output_path="rapports_json/$$file_name"; \
		echo "Scanning $$img → $$output_path"; \
		[ -f "$$output_path" ] && rm "$$output_path"; \
		trivy image --format json -o "$$output_path" "$$img"; \
	done

vulnérabilitées_dossier:
	trivy fs . 

conversion:
	python3 conversion\ json-py.py  

affichage-rapport:
	open report.html   

generateur-traffic:
	bash ./monitoring/traffic.sh
