from experta import *
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

class Cliente(Fact):
    pass

class SuporteTecnico(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.resposta = "❌ Problema não identificado."

    @Rule(Cliente(problema=P(lambda x: "tela azul" in x.lower())))
    def problema_memoria(self):
        self.resposta = "💾 Provavelmente um problema de memória RAM."

    @Rule(Cliente(problema=P(lambda x: "internet" in x.lower())))
    def problema_rede(self):
        self.resposta = "💡 Verifique o roteador ou tente reiniciar a conexão de rede."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    problema = request.json["mensagem"]
    
    engine = SuporteTecnico()
    engine.reset()
    engine.declare(Cliente(problema=problema))
    engine.run()

    return jsonify({"resposta": engine.resposta})

if __name__ == "__main__":
    app.run(debug=True)
