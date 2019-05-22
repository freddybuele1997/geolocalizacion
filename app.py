from flask import Flask, render_template, request, make_response,redirect,url_for

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(debug=False)
