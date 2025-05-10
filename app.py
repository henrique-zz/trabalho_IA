from experta import *
from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

PALAVRAS_SAUDACOES = [
    r"\boi\b",
    r"\bol[aá]\b"
]

PALAVRAS_RAM = [
    r"\btela\b.*\bazul\b", # \b pra delimitar pra não pegar "estrelado" por exemplo, e o .* serve pra dizer que pode ter qualquer coisa no meio
    r"\bn[aã]o liga\b",
    r"\bn[aã]o est[aá] ligando\b"   
]

class Cliente(Fact):
    pass

class SuporteTecnico(KnowledgeEngine):
    
    def __init__(self):
        super().__init__()
        self.resposta = "❌ Problema não identificado."

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x) for p in PALAVRAS_SAUDACOES))))
    def saudacoes(self):
        self.resposta = "😀 Olá! Como posso ajudar?"
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x) for p in PALAVRAS_RAM))))
    def problema_memoria(self):
        self.resposta = "💾 Problema de memória RAM ou energia."
        self.halt()

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
