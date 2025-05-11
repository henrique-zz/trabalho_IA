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
        self.resposta = "❌ Problema não identificado. Por favor, descreva seu problema com mais detalhes."

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x, re.IGNORECASE) for p in PALAVRAS_SAUDACOES))))
    def saudacoes(self):
        self.resposta = "😀 Olá! Sou seu assistente de suporte técnico. Por favor, descreva seu problema para que eu possa ajudar."
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x, re.IGNORECASE) for p in PALAVRAS_BOOT))))
    def problemas_inicializacao(self):
        self.resposta = """💻 Problema de inicialização detectado:
        
1. Verifique a conexão de energia:
   - Cabo de força bem conectado
   - Tomada funcionando
   - Luzes do gabinete acesas

2. Problemas com memória RAM:
   - Tente remover e recolocar os pentes de memória
   - Teste com um pente de cada vez

3. Verifique o disco rígido:
   - Acesse a BIOS (geralmente apertando DEL ou F2 durante a inicialização)
   - Confira se o HD/SSD está sendo detectado"""
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x, re.IGNORECASE) for p in PALAVRAS_VIDEO))))
    def problemas_video(self):
        self.resposta = """🖥️ Problema de vídeo detectado:

1. Verifique as conexões físicas:
   - Cabo de vídeo bem conectado (tanto na placa quanto no monitor)
   - Teste com outro cabo se possível

2. Problemas com placa de vídeo:
   - Se for placa dedicada, verifique os conectores de energia
   - Tente remover e recolocar a placa

3. Soluções de software:
   - Atualize os drivers da placa de vídeo
   - Reinstale o driver atual"""
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x, re.IGNORECASE) for p in PALAVRAS_FONTE))))
    def problemas_energia(self):
        self.resposta = """🔌 Problema de energia detectado:

1. Verificação básica:
   - Teste outra tomada
   - Verifique se o cabo de força está intacto
   - Cheque se a fonte está ligada (botão na parte traseira)

2. Teste da fonte de alimentação:
   - Desconecte todos os componentes desnecessários
   - Tente ligar com apenas o essencial conectado

3. Possíveis problemas:
   - Fonte queimada (cheque por cheiro de queimado)
   - Superaquecimento (ventoinha da fonte girando?)"""
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x, re.IGNORECASE) for p in PALAVRAS_FIREWALL))))
    def problemas_firewall(self):
        self.resposta = """🛡️ Problema com firewall detectado:

1. Verificação básica:
   - Temporariamente desative o firewall para testes
   - Verifique se o programa está na lista de permitidos

2. Configurações avançadas:
   - Verifique as regras de entrada/saída
   - Confira se o antivírus não está bloqueando

3. Soluções alternativas:
   - Adicione exceções para o programa
   - Atualize o software de segurança"""
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x, re.IGNORECASE) for p in PALAVRAS_SEGURANCA))))
    def problemas_seguranca(self):
        self.resposta = """🦠 Problema de segurança detectado:

1. Verificação de vírus:
   - Execute uma verificação completa do sistema
   - Atualize as definições de vírus

2. Problemas com malware:
   - Use o Windows Defender ou seu antivírus
   - Execute ferramentas como Malwarebytes

3. Prevenção:
   - Não clique em links suspeitos
   - Mantenha seu sistema atualizado"""
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x, re.IGNORECASE) for p in PALAVRAS_SOFTWARE))))
    def problemas_software(self):
        self.resposta = """🧩 Problema de software detectado:

1. Soluções básicas:
   - Reinicie o programa
   - Reinicie o computador

2. Atualizações:
   - Verifique atualizações para o software
   - Atualize seu sistema operacional

3. Reinstalação:
   - Desinstale completamente o programa
   - Baixe a versão mais recente do site oficial"""
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x, re.IGNORECASE) for p in PALAVRAS_REDE))))
    def problemas_rede(self):
        self.resposta = """📶 Problema de rede detectado:

1. Verificação básica:
   - Reinicie o roteador/modem
   - Verifique se outros dispositivos estão conectados

2. Soluções para Wi-Fi:
   - Mova-se mais perto do roteador
   - Tente conectar via cabo de rede

3. Configurações:
   - Verifique se o modo avião está desligado
   - Esqueça a rede e conecte novamente
   - Atualize os drivers de rede"""
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x, re.IGNORECASE) for p in PALAVRAS_ARMAZENAMENTO))))
    def problemas_armazenamento(self):
        self.resposta = """💾 Problema de armazenamento detectado:

1. Verificação de disco:
   - Execute CHKDSK (Prompt: chkdsk /f C:)
   - Verifique erros com ferramentas como CrystalDiskInfo

2. Espaço insuficiente:
   - Libere espaço deletando arquivos temporários
   - Desinstale programas não utilizados

3. Problemas físicos:
   - Verifique os cabos SATA/energia
   - Teste o disco em outro computador"""
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x, re.IGNORECASE) for p in PALAVRAS_DISPOSITIVOS))))
    def problemas_dispositivos(self):
        self.resposta = """🖱️ Problema com dispositivos detectado:

1. Verificação básica:
   - Reconecte o dispositivo
   - Teste em outra porta USB
   - Tente em outro computador

2. Problemas com drivers:
   - Atualize os drivers no Gerenciador de Dispositivos
   - Desinstale e deixe o Windows reinstalar

3. Configurações:
   - Verifique as configurações de energia (USB selective suspend)
   - Teste sem hubs USB (conecte diretamente no PC)"""
        self.halt()

    @Rule(Cliente(problema=P(lambda x: any(re.search(p, x, re.IGNORECASE) for p in PALAVRAS_AUDIO))))
    def problemas_audio(self):
        self.resposta = """🔊 Problema de áudio detectado:

1. Verificação básica:
   - Verifique se o som não está mudo
   - Confira o dispositivo de saída selecionado

2. Problemas com drivers:
   - Atualize drivers no Gerenciador de Dispositivos
   - Reinstale o driver de áudio

3. Configurações:
   - Verifique o Mixer de Volume (botão direito no ícone de som)
   - Teste em diferentes programas (YouTube, Windows Sounds)"""
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
