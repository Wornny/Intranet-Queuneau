from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

@app.route('/remplacement')
def index():
    return render_template('remplacement.html')

@app.route('/ajouter_remplacement', methods=['POST'])
def ajouter_remplacement():
    jour = request.form['jour']  # Récupère le jour sélectionné
    horaire = request.form['horaire']  # Récupère l'horaire sélectionné
    matiere = request.form['matiere']  # Récupère la matière
    classe = request.form['classe']  # Récupère la classe
    status = request.form['status']  # Récupère le statut

    # Remplacer le numéro de l'horaire par le jour réel
    if jour == 'lundi':
        horaire = "Lundi"
    elif jour == 'mardi':
        horaire = "Mardi"
    elif jour == 'mercredi':
        horaire = "Mercredi"
    elif jour == 'jeudi':
        horaire = "Jeudi"
    elif jour == 'vendredi':
        horaire = "Vendredi"
    elif jour == 'samedi':
        horaire = "Samedi"

    # Ajout des données au fichier CSV
    with open('besoins.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([jour, horaire, matiere, classe, status])  # Enregistrement dans le CSV

    return redirect('/remplacement')

if __name__ == '__main__':
    app.run(debug=True)
