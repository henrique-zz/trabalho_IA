from experta import *
from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

PALAVRAS_SAUDACOES = [
    r"\boi\b",  # \b pra delimitar pra não pegar "estrelado" por exemplo, e o .* serve pra dizer que pode ter qualquer coisa no meio
    r"\bol[aá]\b"
]

PALAVRAS_BOOT = [
    r"\btela\b.*\bazul\b",
    r"\berro\b.*\btela\b.*\bazul\b",
    r"\bn[aã]o liga\b",
    r"\bn[aã]o est[aá] ligando\b",
    r"\bn[aã]o inicia\b",
    r"\bn[aã]o est[aá] iniciando\b",
    r"\bsistema operacional n[aã]o inicia\b",
    r"\bn[aã]o entra no windows\b",
    r"\bn[aã]o carrega\b",
    r"\bc[oó]digo na bios\b",
    r"\bn[aã]o salva\b.*\bbios\b",
    r"\bdesliga do nada\b",
    r"\bdesliga ao ligar\b",
    r"\bdesliga\b.*\bsozinho\b",
    r"\bliga\b.*\bdesliga\b",
    r"\breinicia\b.*\bsozinho\b",
    r"\bfica\b.*\bcarregando\b",
    r"\bloop\b.*\binicializa[cç][aã]o\b"
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
    r"\bfalta\b.*\benergia\b",
    r"\bn[aã]o liga\b",
    r"\bn[aã]o est[aá] ligando\b",
    r"\bcabo\b.*\bfor[çc]a\b",
    r"\bfonte\b.*\bqueimada\b",
    r"\bn[aã]o acende\b.*\bled\b",
    r"\bcheiro\b.*\bqueimado\b",
    r"\bbarulho\b",
    r"\bbarulhento\b",
    r"\besquentando\b",
    r"\besquentando demais\b",
    r"\bdesligou\b.*\bn[aã]o liga mais\b",
    r"\bsistema lento\b",
    r"\bhd\b.*\bbarulho\b"
]



PALAVRAS_FIREWALL = [
    r"\bfirewall\b.*\bbloqueando\b",
    r"\bfirewall\b.*\bbarrando\b",
    r"\bbloqueio\b.*\bfirewall\b",
    r"\bfirewall\b.*\bimpedindo\b.*\bacesso\b",
    r"\bfirewall\b.*\bbloqueou\b"
]


PALAVRAS_SEGURANCA = [
    r"\bnavegador\b.*\blento\b",
    r"\bnavegador\b.*\btravando\b",
    r"\bpropaganda\b.*\bdemais\b",
    r"\bpop.?ups?\b.*\bconstantes\b",
    r"\bjanelas\b.*\babrindo\b.*\bsozinhas\b",
    r"\bbrowser\b.*\bpropaganda\b",
    r"\bp[áa]ginas\b.*\babrindo\b.*\bsozinhas\b",
    r"\binternet\b.*\bcheia\b.*\bpopups\b",
    r"\bvírus\b",
    r"\bmalware\b",
    r"\bamea[çc]a\b.*\bdetectada\b",
    r"\bprote[cç][aã]o\b.*\bativa\b",
    r"\bantiv[ií]rus\b.*\bdesligado\b",
    r"\bseguran[çc]a\b.*\bdesativada\b",
    r"\bsoftware\b.*\bestranho\b.*\biniciar\b",
    r"\binicializa[cç][aã]o\b.*\bindesejada\b",
    r"\bprogramas?\b.*\babrindo\b.*\bsozinho\b"
]


PALAVRAS_SOFTWARE = [
    r"\bfalta\b.*\bDLL\b",
    r"\bmissing DLL\b",
    r"\bprograma\b.*\btravando\b",
    r"\bprograma\b.*\bdevagar\b",
    r"\bprograma\b.*\blento\b",
    r"\bprograma\b.*\bfechou\b.*(sozinho|do nada)",
    r"\bsistema\b.*\blento\b",
    r"\bcomputador\b.*\bdevagar\b",
    r"\bm[áa]quina\b.*\btravando\b",
    r"\bdesempenho\b.*\bbaixo\b",
    r"\bcomputador\b.*\barrastado\b",
    r"\blentid[aã]o\b.*\bsistema\b",
    r"\b(app|aplicativo|software|programa)\b.*\b(n[aã]o abre|n[aã]o inicia|n[aã]o executa|travado ao iniciar)",
    r"\bincompat[ií]vel\b.*\bsistema\b",
    r"\berro de vers[aã]o\b.*\bprograma\b",
    r"\bconflito\b.*\bentre\b.*\bprogramas\b"
]


PALAVRAS_REDE = [
    r"\bsem internet\b",
    r"\bdesconectado da rede\b",
    r"\bsem conex[aã]o\b",
    r"\bn[aã]o conecta\b",
    r"\binternet caiu\b",
    r"\brede nao identificada\b",
    r"\brede desconhecida\b",
    r"\brede n[aã]o aparece\b",
    r"\berro de rede\b",
    r"\binternet\b.*\blenta\b",
    r"\bconex[aã]o fraca\b",
    r"\binternet devagar\b",
    r"\bnavega[cç][aã]o lenta\b",
    r"\bconflito de IP\b",
    r"\bIP duplicado\b",
    r"\bproblema de IP\b",
    r"\bconflito de endere[cç]o\b",
    r"\bDNS nao responde\b",
    r"\berro de DNS\b",
    r"\bDNS indispon[ií]vel\b",
    r"\bfalha ao resolver nomes\b",
    r"\bproblemas no roteador ou modem\b",
    r"\broteador n[aã]o funciona\b",
    r"\bmodem\b.*\bcom defeito\b",
    r"\bluz vermelha no roteador\b"
]

PALAVRAS_ARMAZENAMENTO = [
    r"\bHD ou SSD nao reconhece\b",
    r"\bdisco n[aã]o detectado\b",
    r"\bhd desapareceu\b",
    r"\barmazenamento n[aã]o reconhecido\b",
    r"\bssd sumiu\b",
    r"\bespa[cç]o insuficiente no disco\b",
    r"\bsem espa[cç]o no hd\b",
    r"\bdisco cheio\b",
    r"\barmazenamento lotado\b",
    r"\bsistema travando ao acessar arquivos\b",
    r"\btrava ao abrir pasta\b",
    r"\bn[aã]o abre arquivos\b",
    r"\bcongelamento ao acessar dados\b",
    r"\barquivos\b.*\bcorrompidos\b",
    r"\barquivos\b.*\bdanificados\b",
    r"\berro ao abrir arquivos\b",
    r"\barquivos com problema\b",
    r"\bdemora para copiar\/mover arquivos\b",
    r"\bcopiar arquivo demora\b",
    r"\bmover arquivos muito lento\b",
    r"\bdemora ao transferir dados\b"
]

PALAVRAS_DISPOSITIVOS = [
    r"\bteclado ou mouse n[aã]o respondem\b",
    r"\bmouse nao funciona\b",
    r"\bteclado nao funciona\b",
    r"\bnao consigo clicar\b",
    r"\busb nao funciona\b",
    r"\bconecto e nao funciona\b",
    r"\bdriver ausente ou desatualizados\b",
    r"\bdriver n[aã]o instalado\b",
    r"\bdriver\b.*\bfaltando\b",
    r"\bdriver antigo\b",
    r"\bdrivers desatualizados\b",
    r"\bimpressora nao imprime\b",
    r"\bn[aã]o sai impress[aã]o\b",
    r"\berro na impressora\b",
    r"\bimpressora sem resposta\b",
    r"\bscanner nao e reconhecido\b",
    r"\bscanner n[aã]o aparece\b",
    r"\bscanner n[aã]o detectado\b",
    r"\berro no scanner\b",
    r"\bwebcam nao funciona\b",
    r"\bc[aâ]mera sem imagem\b",
    r"\bwebcam desligada\b",
    r"\bjoystick ou controle nao funciona\b",
    r"\bcontrole\b.*\bsem resposta\b",
    r"\bjoystick n[aã]o detectado\b",
    r"\bcontrole n[aã]o reconhecido\b"
]

PALAVRAS_AUDIO = [
    r"\bsem som\b",
    r"\bplaca de som nao reconhecida\b",
    r"\bcomputador\b.*\bmudo\b",
    r"\bsem [aá]udio\b",
    r"\b[aá]udio n[aã]o funciona\b",
    r"\bsom n[aã]o sai\b",
    r"\bfone de ouvido\/caixa de som nao reconhecidos\b",
    r"\bfone n[aã]o detectado\b",
    r"\bcaixa de som n[aã]o funciona\b",
    r"\b[aá]udio externo n[aã]o reconhecido\b",
    r"\bsem\b.*\bsom\b",
    r"\bn[aã]o sai\b.*\bsom\b",
    r"\bproblema\b.*\b[aá]udio\b",
    r"\bdriver\b.*\bsom\b.*\berro\b",
    r"\bfone\b.*\bn[aã]o funciona\b"
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
