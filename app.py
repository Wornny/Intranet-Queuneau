from flask import Flask, request, render_template, redirect, session, url_for

import csv 

# Nom du fichier CSV
CSV_REMPLACEMENT = "./assets/csv/fichierRemplacements.csv"

app = Flask(__name__)
app.secret_key = "MaSuperCleSecrete"  


@app.route('/', methods=['GET', 'POST'])
def bonjour_post():

    return render_template('index.html',)


#Route pour l'affichage du formulaire (GET) ou le traitement du formulaire (POST)
#Avec la méthode POST les données du formulaire sont extraites et ensuite sauvegardées
#dans un fichier CSV. le formulaire est ensuite affiché
@app.route("/addremplacement", methods=["POST","GET"])
def home():
    message = ""    #permet de transmettre un message à la page
    if request.methods == "POST" :
        message = "Erreur de message"   #message pour le cas où une erreur se produise
        matiere = request.form["matiere"]  #Récupération des valeurs du formulaire
        date = request.form["date"]
        jour = request.form["jour"]
        classe = request.form["classe"]
        horaire = request.form["horaire"]
        status = "D"    #D pour dispo et R pour remplacé

        with open(CSV_REMPLACEMENT, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([ date, jour, horaire,matiere, classe,status])
            message = "Enregistrement réussi"
    

    return render_template("addRemplacement.html",message=message)

if __name__ == '__main__':
    app.run(host ="0.0.0.0" , port=8000 , debug=True)
