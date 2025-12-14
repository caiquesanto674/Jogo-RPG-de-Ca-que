# -*- coding: utf-8 -*-

import unittest
from apolo_engine.entidades.unidades import Personagem, Inimigo
from apolo_engine.sistemas.motor_decisao import SistemaDecisaoFonte

class TestCombatSystem(unittest.TestCase):
    """Testes para o sistema de combate principal."""

    def test_attack_damage(self):
        """Verifica se o cálculo de dano está correto."""
        # Configuração
        sdf = SistemaDecisaoFonte()
        atacante = Personagem("Herói de Teste", 10, 100)
        defensor = Inimigo("Ogro de Teste", 5, 80)
        vida_inicial_defensor = defensor.vida

        # Ação
        atacante.atacar(defensor, sdf)

        # Verificação
        dano_esperado = sdf.regras["dano_base"] + (atacante.forca * sdf.regras["modificador_forca"])
        vida_esperada_final = vida_inicial_defensor - dano_esperado

        self.assertEqual(defensor.vida, vida_esperada_final)

if __name__ == '__main__':
    unittest.main()
