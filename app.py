from flask import Flask, request, jsonify, render_template
from sistema_especialista import SuporteTecnico, Cliente

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    problema = request.json["mensagem"].lower().strip()
    
    engine = SuporteTecnico()
    engine.reset()
    engine.declare(Cliente(problema=problema))
    engine.run()

    return jsonify({"resposta": engine.resposta})

if __name__ == "__main__":
    app.run(debug=True)