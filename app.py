import csv
import os
from flask import Flask, request, render_template, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "MaSuperCleSecrete"
CSV_FILE = "utilisateurs.csv"
AVATAR_FOLDER = "static/avatars/"

# Créer le dossier des avatars si nécessaire
if not os.path.exists(AVATAR_FOLDER):
    os.makedirs(AVATAR_FOLDER)

# Lecture du fichier CSV
def lire_utilisateurs():
    utilisateurs = {}
    with open(CSV_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Ignorer l'en-tête
        for row in reader:
            if len(row) == 2:  # Si l'email n'est pas encore présent, on a seulement login et password
                login, password = row
                utilisateurs[login] = {"password": password, "email": ""}
            elif len(row) == 3:  # Si l'email est déjà dans le CSV
                login, password, email = row
                utilisateurs[login] = {"password": password, "email": email}
    return utilisateurs

# Sauvegarde des utilisateurs dans le fichier CSV
def sauvegarder_utilisateurs(utilisateurs):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['login', 'password', 'email'])
        for login, data in utilisateurs.items():
            writer.writerow([login, data["password"], data["email"]])

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
            session['avatar'] = avatar_path  # Sauvegarde du chemin de l'avatar
            return redirect(url_for('profil'))

    return render_template('choisir_avatar.html')

# Profil utilisateur, afficher avatar et identifiant
@app.route('/profil')
def profil():
    if 'login' not in session:
        return redirect(url_for('login'))

    avatar_path = session.get('avatar', None)
    if not avatar_path:
        avatar_path = os.path.join(AVATAR_FOLDER, f"{session['login']}.jpg")
        if os.path.exists(avatar_path):
            session['avatar'] = avatar_path  # Sauvegarde dans la session

    return render_template('profil.html', avatar_path=avatar_path, login=session['login'])

@app.route('/', methods=['GET', 'POST'])
def bonjour_post():
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def message():  

    return render_template('message.html')

# Connexion avec identifiant et mot de passe
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form['login']
        password = request.form['password']
        email = request.form['email']  # Récupère l'email saisi
        utilisateurs = lire_utilisateurs()

        # Vérifier si l'identifiant existe et que le mot de passe correspond
        for login, data in utilisateurs.items():
            if login_input == login and data["password"] == password:
                # Si l'email est vide pour cet utilisateur, ajouter l'email saisi
                if not data["email"]:
                    utilisateurs[login]["email"] = email
                    sauvegarder_utilisateurs(utilisateurs)

                # Vérifier si l'email saisi correspond à celui stocké dans le CSV
                if data["email"] == email:
                    session['login'] = login

                    # Vérifier si un avatar existe déjà et le charger
                    avatar_path = os.path.join(AVATAR_FOLDER, f"{login}.jpg")
                    if os.path.exists(avatar_path):
                        session['avatar'] = avatar_path

                    # Rediriger vers le profil si le mot de passe n'est pas encore par défaut
                    if data["password"] == "azerty*123":
                        return redirect(url_for('changer_mot_de_passe'))
                    else:
                        return redirect(url_for('profil'))
                else:
                    return "Email incorrect", 401

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
        utilisateurs[login]["password"] = nouveau_mdp  # Mettre à jour le mot de passe
        
        # Sauvegarder les modifications dans le fichier CSV
        sauvegarder_utilisateurs(utilisateurs)

        return redirect(url_for('choisir_avatar'))

    return render_template('changer_mot_de_passe.html')

@app.route('/logout')
def logout():
    session.pop('login', None)
    session.pop('avatar', None)  # Supprimer l'avatar de la session
    return redirect(url_for('login'))

@app.route('/remplacement')
def index():
    type_user = 'Gestionnaire'  # Exemple, peut être dynamique

    # Lire le fichier CSV
    remplacements = []
    try:
        with open('besoins.csv', 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)  # Ignore l'en-tête du CSV
            for row in reader:
                if len(row) == 6:  # Vérifier qu'il y a bien 6 colonnes
                    date, jour, horaire, matiere, classe, status = row  # Prendre toutes les colonnes
                    remplacements.append({
                        'date': date,  # Ajout de la date (si besoin)
                        'jour': jour,
                        'horaire': horaire,
                        'matiere': matiere,
                        'classe': classe,
                        'status': status
                    })
    except FileNotFoundError:
        pass  # Si le fichier n'existe pas encore, on ne fait rien

    return render_template('remplacement.html', type_user=type_user, remplacements=remplacements)
@app.route('/ajouter_remplacement', methods=['POST'])
def ajouter_remplacement():
    jour = request.form['jour']
    horaire = request.form['horaire']
    matiere = request.form['matiere']
    classe = request.form['classe']
    status = request.form['status']

    # Remplacement du numéro de l'horaire par le jour réel
    jours_mapping = {
        'lundi': "Lundi",
        'mardi': "Mardi",
        'mercredi': "Mercredi",
        'jeudi': "Jeudi",
        'vendredi': "Vendredi",
        'samedi': "Samedi"
    }
    horaire = jours_mapping.get(jour, jour)

    # Ajout des données au fichier CSV
    with open('besoins.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([jour, horaire, matiere, classe, status])

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

@app.route('/remplacement', methods=['GET', 'POST'])
def remplacement():
    if request.method == 'POST': 
       
        créneau = request.form['Créneau']
        classe = request.form['classe']
        matière = request.form['Matière']
        mail_personnel = request.form ['Mail_personnel']
        
        new_message = [{'Créneau': créneau, 'Classe': classe, 'Matière': matière, 'mail_personnel': mail_personnel}]
        
       
        with open('remplacement.csv', mode='a', newline='', encoding='utf-8') as csvfile:
            fieldnames = new_message[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            
            csvfile.seek(0, 2)  
            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerows(new_message)

        
        return redirect(url_for('confirmation', créneau=créneau, classe=classe, matière=matière, mail_personnel=mail_personnel))

   
    return render_template('remplacement.html')  

@app.route('/confirmation')
def confirmation():
    
    créneau = request.args.get('créneau')
    classe = request.args.get('classe')
    matière = request.args.get('matière')
    mail_personnel = request.args.get('mail')

    return render_template('confirmation.html', créneau=créneau, classe=classe, matière=matière, mail=mail_personnel)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
