from flask import Flask, request, render_template, redirect, session, url_for

app = Flask(__name__)
app.secret_key = "MaSuperCleSecrete"  


@app.route('/', methods=['GET', 'POST'])
def bonjour_post():

    return render_template('index.html',)

@app.route('/save', methods=['POST'])
def save_message():

    return render_template('message.html',)


if __name__ == '__main__':
    app.run(host ="0.0.0.0" , port=8000 , debug=True)

