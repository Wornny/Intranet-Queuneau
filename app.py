import csv
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

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
    app.run(debug=True, host='0.0.0.0', port=5000)
