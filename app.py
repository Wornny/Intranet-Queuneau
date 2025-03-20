import csv
import os
from flask import Flask, request, render_template, redirect, session, url_for

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
            return redirect(url_for('profil'))

    return render_template('choisir_avatar.html')

# Profil utilisateur, afficher avatar et identifiant
@app.route('/profil')
def profil():
    if 'login' not in session:
        return redirect(url_for('login'))

    # Charger l'avatar depuis le fichier
    avatar_path = session.get('avatar', None)
    if not avatar_path:
        avatar_path = os.path.join(AVATAR_FOLDER, f"{session['login']}.jpg")
        if os.path.exists(avatar_path):
            session['avatar'] = avatar_path  # Sauvegarder le chemin de l'avatar dans la session

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

            # Vérifier si un avatar existe déjà et le charger
            avatar_path = os.path.join(AVATAR_FOLDER, f"{login}.jpg")
            if os.path.exists(avatar_path):
                session['avatar'] = avatar_path

            # Si l'utilisateur a encore le mot de passe par défaut, on lui demande de le changer
            if utilisateurs[login] == "azerty*123":
                return redirect(url_for('changer_mot_de_passe'))
            else:
                return redirect(url_for('profil'))

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

        return redirect(url_for('choisir_avatar'))

    return render_template('changer_mot_de_passe.html')

@app.route('/logout')
def logout():
    # Supprimer les données de la session pour déconnecter l'utilisateur
    session.pop('login', None)
    session.pop('avatar', None)  # Supprimer l'avatar si nécessaire
    return redirect(url_for('login'))

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
    app.run(host="0.0.0.0", port=8000, debug=True)
