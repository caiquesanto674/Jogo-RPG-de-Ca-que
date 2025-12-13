"""
Módulo do Motor de Autocura do Nexus Guardian.
"""

import re

class AutoHealEngine:
    """
    Motor de autocura para corrigir problemas comuns de sintaxe e estrutura.
    As correções são heurísticas e devem ser usadas com cautela.
    """

    def heal_syntax(self, code: str) -> str:
        """
        Tenta corrigir problemas de sintaxe comuns de forma conservadora.
        """
        fixed = code

        # Remove caracteres de controle inválidos, mantendo os essenciais
        fixed = ''.join(char for char in fixed if ord(char) >= 32 or char in '\n\t\r')

        # Substitui tabs por 4 espaços, uma prática padrão em Python
        fixed = fixed.replace('\t', '    ')

        # Heurística para fechar parênteses/colchetes/chaves abertos no final de linhas
        # Isso é arriscado, então aplicamos de forma limitada.
        lines = fixed.split('\n')
        fixed_lines = []
        for line in lines:
            stripped_line = line.strip()
            # Só adiciona se a linha não for vazia e parecer precisar de fechamento
            if stripped_line and not stripped_line.endswith((':', ',', '(', '[', '{')):
                open_paren = line.count('(') - line.count(')')
                open_bracket = line.count('[') - line.count(']')
                open_brace = line.count('{') - line.count('}')

                if open_paren > 0:
                    line += ')' * open_paren
                if open_bracket > 0:
                    line += ']' * open_bracket
                if open_brace > 0:
                    line += '}' * open_brace
            fixed_lines.append(line)

        return '\n'.join(fixed_lines)

    def heal_structure(self, code: str) -> str:
        """
        Tenta corrigir problemas estruturais, como duplicações simples.
        """
        lines = code.split('\n')
        cleaned = []
        seen_signatures = set()
        in_function = False

        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # Detectar e corrigir "def def função"
            line = re.sub(r'^\s*def\s+def\s+', 'def ', line)

            # Evitar duplicação de assinaturas de função/classe
            if stripped.startswith('def ') or stripped.startswith('class '):
                signature = stripped.split('(')[0] # Pega a assinatura básica
                if signature in seen_signatures:
                    # Pula o bloco duplicado (heurística)
                    i += 1
                    while i < len(lines) and (not lines[i].strip().startswith(('def ', 'class ')) and lines[i].startswith((' ', '\t', '#'))):
                        i += 1
                    continue # Volta para o loop principal sem adicionar a linha
                seen_signatures.add(signature)

            cleaned.append(line)
            i += 1

        # Remover linhas em branco duplicadas
        final_code = "\n".join(cleaned)
        return re.sub(r'\n\n\n+', '\n\n', final_code)
