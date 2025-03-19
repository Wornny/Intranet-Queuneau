import csv
import os
from flask import Flask, request, render_template, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "MaSuperCleSecrete"
CSV_FILE = "utilisateurs.csv"

# Lecture du fichier CSV
def lire_utilisateurs():
    utilisateurs = {}
    with open(CSV_FILE, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Ignorer l'en-tête
        for row in reader:
            if len(row) == 2:
                utilisateurs[row[0]] = row[1]
    return utilisateurs

# Sauvegarder les utilisateurs après modification
def sauvegarder_utilisateurs(utilisateurs):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['login', 'password'])
        for login, password in utilisateurs.items():
            writer.writerow([login, password])

@app.route('/', methods=['GET', 'POST'])
def bonjour_post():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])  # Ajout de 'POST'
def login():
    if request.method == 'POST':  # Vérifie si le formulaire a été soumis
        login = request.form['login']
        password = request.form['password']
        utilisateurs = lire_utilisateurs()

        if login in utilisateurs and utilisateurs[login] == password:
            session['login'] = login

            # Si l'utilisateur a encore le mot de passe par défaut, on lui demande de le changer
            if utilisateurs[login] == "azerty*123":
                return redirect(url_for('changer_mot_de_passe'))
            else:
                return render_template('index.html')

        else:
            return "Identifiants incorrects", 401

    return render_template('login.html')

@app.route('/changer_mot_de_passe', methods=['GET', 'POST'])
def changer_mot_de_passe():
    if 'login' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nouveau_mdp = request.form['nouveau_mdp']
        login = session['login']
        
        utilisateurs = lire_utilisateurs()
        utilisateurs[login] = nouveau_mdp  # Mettre à jour le mot de passe de l'utilisateur
        
        # Sauvegarder les modifications dans le fichier CSV
        sauvegarder_utilisateurs(utilisateurs)

        return render_template("login.html")

    return render_template('changer_mot_de_passe.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
