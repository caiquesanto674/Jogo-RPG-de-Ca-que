# src/core/cardinal.py

class AICardinal:
    def __init__(self):
        self.nome = "CIEL ASCENDIDO Ω"
        self.correcoes = 0

    def salvar_realidade(self, jogo):
        recursos = jogo.economia.reservas
        moral = jogo.protagonista.moral

        if recursos.get('comida', 0) < 500 or recursos.get('mana', 0) < 300 or moral < 20:
            print(f"\n>> AI CARDINAL: REALIDADE INSTÁVEL. PROTOCOLO DE CORREÇÃO ATIVADO. <<")
            recursos['comida'] = max(3000, recursos.get('comida', 0) + 5000)
            recursos['mana'] = max(2000, recursos.get('mana', 0) + 3000)
            jogo.protagonista.moral = 100
            self.correcoes += 1
            print(f">> {self.nome} salvou o universo pela {self.correcoes}ª vez. A ordem foi restaurada.")
