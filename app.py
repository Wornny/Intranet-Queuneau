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


###Partie Cantine

from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Clé secrète pour la gestion des sessions

plats = []

@app.route('/cantine')
def cantine():
    return render_template('cantine.html', plats=plats)  # Vérifie que cantine.html existe bien dans templates/

@app.route('/ajouter_plat', methods=['POST'])
def ajouter_plat():
    plat = request.form['nouveauPlat']
    jour = request.form['jour']
    plats.append({'nom': plat, 'jour': jour, 'likes': 0, 'dislikes': 0, 'users_voted': []})  # Correction ici
    return redirect(url_for('cantine'))

@app.route('/vote/<int:plat_index>/<vote_type>', methods=['POST'])
def vote(plat_index, vote_type):
    if plat_index < 0 or plat_index >= len(plats):
        return redirect(url_for('cantine'))  # Sécurisation si l'index est invalide

    plat = plats[plat_index]  # Correction ici

    if 'user_id' in session:
        user_id = session['user_id']
        user_vote = next((vote for vote in plat['users_voted'] if vote['user_id'] == user_id), None)

        if user_vote:
            if user_vote['vote'] == 'like' and vote_type == 'like':
                plat['likes'] -= 1
                plat['users_voted'].remove(user_vote)
                return redirect(url_for('cantine'))
            if user_vote['vote'] == 'dislike' and vote_type == 'dislike':
                plat['dislikes'] -= 1
                plat['users_voted'].remove(user_vote)
                return redirect(url_for('cantine'))
            if user_vote['vote'] == 'like' and vote_type == 'dislike':
                plat['likes'] -= 1
                plat['dislikes'] += 1
            elif user_vote['vote'] == 'dislike' and vote_type == 'like':
                plat['dislikes'] -= 1
                plat['likes'] += 1
            plat['users_voted'].remove(user_vote)
            plat['users_voted'].append({'user_id': user_id, 'vote': vote_type})
        else:
            if vote_type == 'like':
                plat['likes'] += 1
            elif vote_type == 'dislike':
                plat['dislikes'] += 1
            plat['users_voted'].append({'user_id': user_id, 'vote': vote_type})
    else:
        session['user_id'] = len(session) + 1  

    return redirect(url_for('cantine'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
