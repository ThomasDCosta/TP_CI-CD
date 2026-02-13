import json
import glob

# Tous les fichiers JSON à traiter
json_files = glob.glob("rapports_json/devops-*.json")

# Définir l'ordre de gravité
severity_order = {"CRITICAL": 1, "HIGH": 2, "MEDIUM": 3, "LOW": 4, "UNKNOWN": 5}

# Extraire toutes les vulnérabilités
vulns = []
for file_name in json_files:
    with open(file_name, encoding="utf-8") as f:
        data = json.load(f)
    for result in data.get("Results", []):
        image_name = result.get("Target", file_name)  
        for vuln in result.get("Vulnerabilities", []):
            vulns.append({
                "VulnerabilityID": vuln['VulnerabilityID'],
                "PkgName": vuln.get('PkgName', ''),
                "Severity": vuln['Severity'],
                "Image": image_name,
                "SourceFile": file_name
            })

# Trier par gravité
vulns_sorted = sorted(vulns, key=lambda x: severity_order.get(x['Severity'], 6))

# Générer HTML
html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Rapport Trivy</title>
<style>
    table { border-collapse: collapse; width: 90%; margin: 20px auto; }
    th, td { border: 1px solid black; padding: 8px; text-align: left; }
    th { background-color: #f2f2f2; }
    .CRITICAL { background-color: #ff4d4d; }
    .HIGH { background-color: #ff5f4d; }
    .MEDIUM { background-color: #ffff99; }
    .LOW { background-color: #b3ffb3; }
    .UNKNOWN { background-color: #d9d9d9; }
</style>
</head>
<body>
<h1 style="text-align:center;">Rapport Trivy</h1>
"""

# Grouper les vulnérabilités par image
images = sorted(set(v['Image'] for v in vulns_sorted))
for image in images:
    html_content += f"<h2 style='text-align:center;'>Image : {image}</h2>\n"
    html_content += """
    <table>
        <tr>
            <th>Vulnérabilité</th>
            <th>Package</th>
            <th>Gravité</th>
            <th>Fichier source</th>
        </tr>
    """
    for vuln in [v for v in vulns_sorted if v['Image'] == image]:
        html_content += f"""
        <tr class="{vuln['Severity']}">
            <td>{vuln['VulnerabilityID']}</td>
            <td>{vuln['PkgName']}</td>
            <td>{vuln['Severity']}</td>
            <td>{vuln['SourceFile']}</td>
        </tr>
        """
    html_content += "</table>\n"

html_content += "</body></html>"

# Écrire dans le fichier HTML
with open("report.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"report.html généré avec tableau trié par gravité et groupé par image !")
