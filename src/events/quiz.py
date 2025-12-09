# src/events/quiz.py

import random
from src.core.monarca import MonarcaAbsoluto
from src.utils.log_protocol import LogSistema

class PerguntaQuiz:
    def __init__(self, tema, questao, opcoes, resposta):
        self.tema, self.questao, self.opcoes, self.resposta = tema, questao, opcoes, resposta

class EventoQuiz:
    def __init__(self, protagonista: MonarcaAbsoluto, log: LogSistema):
        self.protagonista = protagonista
        self.log = log
        self.perguntas = [
            PerguntaQuiz("Economia", "Qual é o papel da inflação?", ["Reduz preços", "Aumenta poder de compra", "Corrói o valor do dinheiro"], 3),
            PerguntaQuiz("Tecnologia", "O que significa IA?", ["Inteligência Artificial", "Infraestrutura Avançada", "Informação Autorizada"], 1),
        ]

    def iniciar(self):
        self.log.registrar("EVENTO", "Quiz do Monarca", "Um desafio de conhecimento foi iniciado!")
        p = random.choice(self.perguntas)
        # Simplificado para não exigir input do usuário em um loop de jogo
        acertou = random.choice([True, False])
        if acertou:
            self.log.registrar("QUIZ", self.protagonista.nome, f"respondeu corretamente à pergunta sobre {p.tema}!")
            self.protagonista.pontos_quiz += 1
            self.protagonista.promover()
        else:
            self.log.registrar("QUIZ", self.protagonista.nome, f"errou a pergunta sobre {p.tema}.")
