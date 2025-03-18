from flask import Flask, render_template, request
import csv 

# Nom du fichier CSV
CSV_REMPLACEMENT = "./assets/csv/fichierRemplacements.csv"

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)