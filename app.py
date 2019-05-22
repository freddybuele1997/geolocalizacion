from flask import Flask, render_template, request, make_response, redirect, url_for
import urllib.request, json

app = Flask(__name__)

jsdata = 'dsd'


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
    global jsdata
    jsdata = request.form['javascript_data']
    print(jsdata)
    return jsdata

@app.route('/getpythondata')
def get_python_data():
    print(jsdata)
    return json.dumps(jsdata)


if __name__ == "__main__":
    app.run(debug=True)
