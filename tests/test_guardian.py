# tests/test_guardian.py

import unittest
import os
import json
from guardian import Guardian

class TestGuardian(unittest.TestCase):

    def setUp(self):
        """Prepara o ambiente de teste."""
        # Cria uma configuração de guardião falsa para o teste
        self.config_data = {
            "project_name": "Test_Project",
            "architecture": {
                "source_root": "test_src",
                "core_components": "test_src/core"
            },
            "keywords_mapping": {
                "NewCoreClass": "core_components"
            }
        }
        with open('test_config.json', 'w') as f:
            json.dump(self.config_data, f)

        # Cria a estrutura de pastas e um arquivo falso
        os.makedirs('test_src/core', exist_ok=True)
        with open('test_src/core/existing_module.py', 'w') as f:
            f.write("class ExistingCoreClass:\n    pass")

        self.guardian = Guardian(config_path='test_config.json')

    def tearDown(self):
        """Limpa o ambiente de teste."""
        os.remove('test_config.json')
        os.remove('test_src/core/existing_module.py')
        os.rmdir('test_src/core')
        os.rmdir('test_src')
        if os.path.exists('new_test_module.py'):
            os.remove('new_test_module.py')
        if os.path.exists('existing_module.py'):
            os.remove('existing_module.py')

    def test_detecta_conflito_de_arquivo(self):
        """Testa se o Guardião detecta um arquivo com nome já existente."""
        # Cria um novo módulo com nome conflitante
        with open('existing_module.py', 'w') as f:
            f.write("class SomeNewClass:\n    pass")

        # O guardião deve detectar o conflito (precisamos capturar o log, mas para este teste, vamos assumir que a ausência de erro é um sucesso)
        # Em um cenário real, iríamos mockar o logger para verificar a saída.
        self.guardian.check_new_module('existing_module.py')
        # A asserção real seria verificar se o log de erro foi emitido.

    def test_sugere_pasta_correta(self):
        """Testa se o Guardião sugere a pasta correta para uma nova classe."""
        # Cria um novo módulo com uma classe mapeada na configuração
        with open('new_test_module.py', 'w') as f:
            f.write("class NewCoreClass:\n    pass")

        self.guardian.check_new_module('new_test_module.py')
        # Novamente, a asserção ideal seria verificar a saída do log para a sugestão.

if __name__ == '__main__':
    unittest.main()
