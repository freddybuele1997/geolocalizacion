from flask import Flask, render_template, request, redirect, url_for, jsonify, session, escape
from flask_mail import Mail, Message
import json
from pygeocoder import Geocoder

app = Flask(__name__)
mail = Mail(app)
app.secret_key = "123456789"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pruebasdedesarrollofreddybuele@gmail.com'
app.config['MAIL_PASSWORD'] = '1234567 a'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route("/correo", methods=['POST', 'GET'])
def correo():
    msg = Message(
        'Hola esta persona te agrego como su correo de confianza' + request.form["text_name"] + ' ' + request.form[
            "text_ape"], sender='pruebasdedesarrollofreddybuele@gmail.com', recipients=[request.form["text_email"]])
    msg.body = request.form["text_desc"]
    mail.send(msg)
    help = request.form["text_email"]
    return render_template('confirmacion.html',help = help)


js_latitud = 'lat'
js_longitud = 'lon'
resultado = 'direccion'


@app.route("/")
def index():
    if 'datos' in session:
        return redirect(url_for('localizar'))
    else:
        return render_template("geolocalizacion.html")


@app.route("/generar_dato", methods=['POST', 'GET'])
def generar_dato():
    if 'datos' in session:

        return redirect(url_for('localizar'))

    else:
        session.permanent = True
        session['datos'] = {'nombre': request.form["text_name"], 'apellidos': request.form[
            "text_second_name"], 'email': request.form["text_email"]}
        return redirect(url_for('localizar'))


@app.route("/localizar", methods=['POST', 'GET'])
def localizar():
    if 'datos' in session:
        print(session['datos'].get('email'))
        return render_template("localizar.html")
    else:
        return redirect(url_for('index'))


@app.route('/postmethod', methods=['POST'])
def get_post_javascript_data():
    global js_latitud
    global js_longitud
    js_latitud = request.form['js_latitud']
    js_longitud = request.form['js_longitud']
    results = Geocoder(api_key='AIzaSyCRjRkHf-0D28I2DFoZKRIyWIJJ_VoVrt4').reverse_geocode(float(js_latitud),
                                                                                          float(js_longitud))
    global coordenadas
    coordenadas = {'nombres': session['datos'].get('nombre'), 'apellido': session['datos'].get('apellidos'),
                   'direccion': results.formatted_address, 'email': session['datos'].get('email'),'mensaje_predeterminado':'NECESITO DE TU AYUDA ESTOY EN UNA SITUACIÓN DESESPERANTE POR FAVOR VEN RAPIDO!!!!'}

    return jsonify(coordenadas)


@app.route('/getpythondata')
def get_python_data():
    return json.dumps(coordenadas)


if __name__ == "__main__":
    app.run(debug=True)
