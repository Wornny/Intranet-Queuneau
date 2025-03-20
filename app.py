import csv
import os
from flask import Flask, request, render_template, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "MaSuperCleSecrete"

@app.route('/', methods=['GET', 'POST'])
def bonjour_post():

    return render_template('index.html',)

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

@app.route('/deplacement', methods=['GET', 'POST'])
def deplacement_post():

    return render_template('deplacement.html',)

#Route pour l'affichage du formulaire (GET) ou le traitement du formulaire (POST)
#Avec la méthode POST les données du formulaire sont extraites et ensuite sauvegardées
#dans un fichier CSV. le formulaire est ensuite affiché
@app.route('/save', methods=['POST'])
def save_message():
    address = request.form.get('address')
    address_2 = request.form.get('address_2')  # Champ honeypot
    postal_code = request.form.get('postal_code')
    start_city = request.form.get('start_city')
    car = request.form.get('car')
    objet = request.form.get('objet')
    end_city = request.form.get('end_city')
    bussiness = request.form.get('bussiness')
    date = request.form.get('date')
    start_hours_go = request.form.get('start_hours_go')
    end_hours_go = request.form.get('end_hours_go')
    start_hours_back = request.form.get('start_hours_back')
    end_hours_back = request.form.get('end_hours_back')

    new_message = [{'address': address, 
                    "address_2": address_2, 
                    "postal_code": postal_code, 
                    "start_city": start_city, 
                    "car": car, 
                    "objet" : objet, 
                    "end_city" : end_city, 
                    "bussiness" : bussiness,
                    "date" : date,
                    "start_hours_go" : start_hours_go,
                    "end_hours_go" : end_hours_go,
                    "start_hours_back" : start_hours_back,
                    "end_hours_back" : end_hours_back
                    }]

    # Sauvegarde dans le fichier CSV
    with open('message.csv', mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=new_message[0].keys())
        writer.writerows(new_message)

    return redirect('/')

if __name__ == '__main__':
    app.run(host ="0.0.0.0" , port=8000 , debug=True)
