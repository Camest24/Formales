from flask import Flask, request, jsonify #conectamos flask, request que es basiamente la peticion que llega, y tambien jsonify para devolver json
from gateway import convert, simulate

app = Flask(__name__)

@app.route('/')
def hello():
    return "Funciona el programa :D"

@app.route("/convert", methods=["POST"]) # esto es una ruta q recibe el NFA y devuelve el DFA equivalente
def convert_route(): # le decimos a flask q esta ruta solo acepta peticiones POST, no get.porq le vamos a enviar datos,no solo peddir una pagiina
 data = request.get_json() #con el request la peticion http acaba de llegar,con el get.json le pedimos a flask q lo interpete como json y me lo de en un diccionario de python
 resultado = convert(data["states"],data["alphabet"],data["initial"],data["accepting"],data["transitions"] ) # con data(x) sacamos el valor del diccionario data y ese valor completo se pasa como el primer argumento a convert xd
 return jsonify(resultado) #devolver resultad como respuesta json

@app.route("/simulate", methods=["POST"])
def simulate_route():
 data= request.get_json()
 resultado_simulate = simulate(data["dfa"]["dfaStates"],data["dfa"]["transitions"],data["dfa"]["acceptingStates"],data["input"] ) #siimulamos el dfa con el string q recibimos yh ya usando el dfa armado por el convert
 return jsonify(resultado_simulate) #devolver resultad como respuesta json


if __name__ == '__main__':
    app.run(debug=True)