from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mail import Mail, Message
import json
from flask_sqlalchemy import SQLAlchemy

from pygeocoder import Geocoder

app = Flask(__name__)
mail = Mail(app)
# DEFINIR CONEXION A LA BASE DE DATOS
dbdir = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="freddybuele1997",
    password='12345678 a',
    hostname="freddybuele1997.mysql.pythonanywhere-services.com",

    databasename="ayudas")

app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
db = SQLAlchemy(app)


class usuario(db.Model):
    DNI_CLI = db.Column(db.String(13), primary_key=True)
    NOM_CLI = db.Column(db.String(30))
    APE_CLI = db.Column(db.String(30))
    DIR_CLI = db.Column(db.String(150))


##registros = usuario.query.all()


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pruebasdedesarrollofreddybuele@gmail.com'
app.config['MAIL_PASSWORD'] = '1234567 a'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

coodenadas = []


@app.route("/correo", methods=['POST', 'GET'])
def correo():
    msg = Message(
        'Hola esta persona te agrego como su correo de confianza y esta solicitando tu ayuda' + request.form[
            "text_name"] + ' ' + request.form[
            "text_ape"], sender='pruebasdedesarrollofreddybuele@gmail.com', recipients=[request.form["text_email"]])
    msg.body = request.form["text_desc"] + ' estoy en la siguiente ubicacion' + ' ' + request.form["text_dir"]
    mail.send(msg)
    help = request.form["text_email"]
    return render_template('confirmacion.html', help=help)


js_latitud = 'lat'
js_longitud = 'lon'
resultado = 'direccion'
global coordenadas


@app.route("/registro")
def registro():
    verificar = request.cookies.get('datos', None)
    if verificar == None:
        return render_template("geolocalizacion.html")
    else:
        return redirect(url_for('localizar'))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generar_dato", methods=['POST', 'GET'])
def generar_dato():
    if request.method == "POST":
        new_usuario = usuario(
            DNI_CLI=request.form["text_dni"],
            NOM_CLI=request.form["text_name"],
            APE_CLI=request.form["text_second_name"],
            DIR_CLI=request.form["text_email"]
        )
        db.session.add(new_usuario)
        db.session.commit()
        return redirect(url_for('login'))


@app.route("/login", methods=['POST', 'GET'])
def login():
    return render_template('dni_verificacion.html')


@app.route("/buscar_dni", methods=['POST', 'GET'])
def buscar_dni():
    global users
    if request.method == "POST":
        print("hello")
        if request.form["txt_busqueda"]:
            user1 = db.engine.execute("select * from usuario where DNI_CLI = 0705296168")

            for row in user1:
                users = {'dni': row.DNI_CLI, 'nombres': row.NOM_CLI, 'apellidos': row.APE_CLI, 'correo': row.DIR_CLI}

            print(users)
    return render_template("localizar.html")


@app.route("/localizar", methods=['POST', 'GET'])
def localizar():
    return render_template("localizar.html")


@app.route('/postmethod', methods=['POST'])
def get_post_javascript_data():
    global js_latitud
    global js_longitud

    js_latitud = request.form['js_latitud']
    js_longitud = request.form['js_longitud']
    results = Geocoder(api_key='AIzaSyCRjRkHf-0D28I2DFoZKRIyWIJJ_VoVrt4').reverse_geocode(float(js_latitud),
                                                                                          float(js_longitud))
    global coordenadas
    coordenadas = {'dni': users['dni'], 'nombres': users['nombres'], 'apellido': users['apellidos'],
                   'direccion': results.formatted_address, 'email': users['correo'],
                   'mensaje_predeterminado': 'NECESITO DE TU AYUDA ESTOY EN UNA SITUACIÓN DESESPERANTE POR FAVOR VEN RAPIDO!!!!'}
    print(coordenadas)
    return jsonify(coordenadas)


@app.route('/ingreso')
def ingreso():
    return render_template('dni_verificacion.html')


@app.route('/getpythondata')
def get_python_data():
    return json.dumps(coordenadas)


if __name__ == "__main__":
    app.run(debug=True)
