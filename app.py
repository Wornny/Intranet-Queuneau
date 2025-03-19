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
            return "Connexion réussie"
        else:
            return "Identifiants incorrects", 401
    return render_template('login.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
