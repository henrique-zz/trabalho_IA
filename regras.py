from experta import *

class Cliente(Fact):
    """Fato que representa um cliente solicitando suporte"""
    pass

class SuporteTecnico(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.resposta = ""

    @Rule(Cliente(problema=P(lambda x: "tela azul" in x.lower())))
    def problema_memoria(self):
        self.resposta = "💾 Provavelmente um problema de memória RAM."
        self.halt()

    @Rule(Cliente(problema=P(lambda x: "internet" in x.lower())))
    def problema_rede(self):
        self.resposta = "💡 Verifique o roteador ou tente reiniciar a conexão de rede."
        self.halt()

    @Rule(Cliente(problema=P(lambda x: True)))
    def resposta_padrao(self):
        self.resposta = "🤖 Desculpe, não entendi o problema. Pode ser mais específico?"
        self.halt()
    
    

    def obter_resposta(self, problema):
        self.reset()
        self.resposta = ""
        self.declare(Cliente(problema=problema))
        self.run()
        return self.resposta
