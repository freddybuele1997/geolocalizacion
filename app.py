from flask import Flask, render_template, request, make_response, redirect, url_for, jsonify
import urllib.request, json
from pygeocoder import Geocoder

app = Flask(__name__)

js_latitud = 'lat'
js_longitud = 'lon'
resultado = 'direccion'


def public_ip():
    lista = "0123456789."
    ip = ""
    dato = urllib.request.urlopen("http://checkip.dyndns.org").read()
    for x in str(dato):
        if x in lista:
            ip += x
    return ip


@app.route("/")
def index():
    verificar = request.cookies.get("datos", None)
    if verificar == None:
        return render_template("geolocalizacion.html")
    else:
        return redirect(url_for('localizar'))


@app.route("/generar_dato", methods=['POST', 'GET'])
def generar_dato():
    verificar = request.cookies.get("datos", None)
    if verificar == None:
        response = make_response(render_template("localizar.html"))
        response.set_cookie("datos",
                            "usuario nombre: " + request.form["text_name"] + "_usuario apellido:  " + request.form[
                                "text_second_name"] + "_usuario email: " + request.form["text_email"])
        return response
    else:
        return redirect(url_for('localizar'))


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
    coordenadas = {'direccion':results.formatted_address}

    return jsonify(coordenadas)


@app.route('/getpythondata')
def get_python_data():
    return json.dumps(coordenadas)


if __name__ == "__main__":
    app.run(debug=True)
