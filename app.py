import csv
import os
from flask import Flask, request, render_template, redirect, session, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "MaSuperCleSecrete"
CSV_FILE = "utilisateurs.csv"
AVATAR_FOLDER = "static/avatars/"

# Créer le dossier si nécessaire
if not os.path.exists(AVATAR_FOLDER):
    os.makedirs(AVATAR_FOLDER)

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

# Gérer le téléchargement de l'avatar
@app.route('/choisir_avatar', methods=['GET', 'POST'])
def choisir_avatar():
    if 'login' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        avatar = request.files['avatar']
        if avatar:
            avatar_path = os.path.join(AVATAR_FOLDER, f"{session['login']}.jpg")
            avatar.save(avatar_path)

            # Ajouter le chemin de l'avatar à la session
            session['avatar'] = avatar_path
            return redirect(url_for('profil'))  # Rediriger vers le profil après téléchargement de l'avatar

    return render_template('choisir_avatar.html')

# Profil utilisateur, afficher avatar et identifiant
@app.route('/profil')
def profil():
    if 'login' not in session:
        return redirect(url_for('login'))

    avatar_path = session.get('avatar', None)
    return render_template('profil.html', avatar_path=avatar_path, login=session['login'])

@app.route('/', methods=['GET', 'POST'])
def bonjour_post():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        utilisateurs = lire_utilisateurs()

        if login in utilisateurs and utilisateurs[login] == password:
            session['login'] = login

            # Si l'utilisateur a encore le mot de passe par défaut, on lui demande de le changer
            if utilisateurs[login] == "azerty*123":
                return redirect(url_for('changer_mot_de_passe'))
            else:
                return redirect(url_for('profil'))  # Rediriger vers le profil après connexion

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

        return redirect(url_for('choisir_avatar'))  # Rediriger vers la page de choix d'avatar après le changement de mot de passe

    return render_template('changer_mot_de_passe.html')

@app.route('/logout')
def logout():
    # Supprimer les données de la session pour déconnecter l'utilisateur
    session.pop('login', None)
    session.pop('avatar', None)  # Supprimer l'avatar si nécessaire
    return redirect(url_for('login'))  # Rediriger vers la page de connexion

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
