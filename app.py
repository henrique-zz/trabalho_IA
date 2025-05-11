from experta import *
from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

PALAVRAS_SAUDACOES = [
    r"\boi\b",
    r"\bol[aá]\b"
]

PALAVRAS_BOOT = [
    r"\btela\b.*\bazul\b", # \b pra delimitar pra não pegar "estrelado" por exemplo, e o .* serve pra dizer que pode ter qualquer coisa no meio
    r"\bn[aã]o liga\b",
    r"\bn[aã]o est[aá] ligando\b"   
]

PALAVRAS_VIDEO = [
    r"\btela\b.*\bpreta\b",
    r"\btela\b.*\bdistorcida\b",
    r"\bimagem\b.*\bdistorcida\b",
    r"\bresolu[cç][aã]o\b.*\berrada\b",
    r"\bn[aã]o d[aá] v[ií]deo\b",
    r"\bn[aã]o aparece\b.*\btela\b",
    r"\bn[aã]o est[aá] aparecendo\b.*\btela\b",
    r"\bn[aã]o mostra\b.*\btela\b",
    r"\btela\b.*\bn[aã]o aparece\b",
    r"\bnada\b.*\btela\b"
]

PALAVRAS_FONTE = [
    
]

PALAVRAS_FIREWALL = [
    
]

PALAVRAS_SEGURANCA = [
    
]

PALAVRAS_SOFTWARE = [
    
]

PALAVRAS_REDE = [
    
]

PALAVRAS_ARMAZENAMENTO = [
    
]

PALAVRAS_DISPOSITIVOS = [
    
]

PALAVRAS_AUDIO = [
    r"\bsem som\b",
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

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x) for p in PALAVRAS_BOOT))))
    def problemas_memoria(self):
        self.resposta = "💾 Problema de memória RAM ou energia."
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x) for p in PALAVRAS_VIDEO))))
    def problemas_video(self):
        self.resposta = "🖥️ Possível problema de vídeo: verifique o cabo de vídeo, a placa gráfica ou a tela."
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x) for p in PALAVRAS_FONTE))))
    def problemas_fonte(self):
        self.resposta = "🔌 Verifique se o cabo de força está conectado corretamente e se há energia na tomada. Teste com outro cabo ou fonte, se possível."
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x) for p in PALAVRAS_FIREWALL))))
    def problemas_firewall(self):
        self.resposta = "🛡️ Pode ser o firewall bloqueando o acesso. Verifique as configurações ou desative temporariamente para testar a conexão."
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x) for p in PALAVRAS_SEGURANCA))))
    def problemas_seguranca(self):
        self.resposta = "🦠 Verifique se o antivírus está bloqueando o programa. Atualize a base de vírus e faça uma varredura completa no sistema."
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x) for p in PALAVRAS_SOFTWARE))))
    def problemas_software(self):
        self.resposta = "🧩 Pode ser um problema de software. Tente reinstalar o programa ou verificar por atualizações disponíveis."
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x) for p in PALAVRAS_REDE))))
    def problemas_rede(self):
        self.resposta = "💡 Verifique o roteador ou tente reiniciar a conexão de rede."
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x) for p in PALAVRAS_ARMAZENAMENTO))))
    def problemas_armazenamento(self):
        self.resposta = "💽 Verifique o espaço disponível no disco. Se estiver cheio, libere espaço excluindo arquivos desnecessários ou transferindo para um HD externo."
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x) for p in PALAVRAS_DISPOSITIVOS))))
    def problemas_dispositivos(self):
        self.resposta = "🔌 Verifique se o dispositivo está corretamente conectado e reconhecido. Tente trocar de porta USB ou reinstalar os drivers."
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x) for p in PALAVRAS_AUDIO))))
    def problemas_audio(self):
        self.resposta = "🔊 Verifique se o áudio está no mudo, se o cabo está conectado corretamente ou se o driver de som está instalado e atualizado."
        self.halt()

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
