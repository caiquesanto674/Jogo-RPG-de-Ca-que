# apolo_engine/systems/economia.py


class SistemaEconomia:
    """Gerencia a economia global, taxas de câmbio e produção de recursos."""

    def __init__(self, taxa_base_producao: float = 1.0):
        self.recursos = {"Creditos": 1000000, "MineraisRaros": 5000}
        self.taxa_producao = taxa_base_producao
        self.taxas_cambio = {"Creditos_por_Min": 150}
        print("Sistema de Economia Ativado.")

    def gerar_recursos(self, recurso: str, taxa_multiplicador: float):
        """Gera recursos com base na taxa de produção da área (usada por Base Militar)."""
        if recurso in self.recursos:
            aumento = int(self.taxa_producao * taxa_multiplicador)
            self.recursos[recurso] += aumento
            return aumento
        return 0

    def comprar_recurso(self, recurso: str, quantidade: int) -> bool:
        """Processa a compra de recursos, verificando Créditos."""
        custo = quantidade * self.taxas_cambio.get(f"Creditos_por_{recurso[:3]}", 1)
        if self.recursos["Creditos"] >= custo:
            self.recursos["Creditos"] -= custo
            self.recursos[recurso] = self.recursos.get(recurso, 0) + quantidade
            return True
        return False
