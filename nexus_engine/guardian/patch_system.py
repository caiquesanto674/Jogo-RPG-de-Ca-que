"""
Módulo do Sistema de Patches do Nexus Guardian.
"""

import difflib
import hashlib
from datetime import datetime
from typing import Dict, Optional

class PatchSystem:
    """
    Sistema para gerar e aplicar patches entre versões de código.
    """

    def generate_patch(self, original: str, modified: str) -> Dict:
        """
        Gera um patch no formato unified_diff.
        """
        diff = list(difflib.unified_diff(
            original.splitlines(keepends=True),
            modified.splitlines(keepends=True),
            fromfile='original',
            tofile='modified',
            lineterm=''
        ))

        patch_text = ''.join(diff)
        patch_id = hashlib.sha256(patch_text.encode()).hexdigest()

        return {
            "id": patch_id,
            "timestamp": datetime.now().isoformat(),
            "patch": patch_text,
            "tamanho": len(patch_text),
            "linhas_adicionadas": sum(1 for line in diff if line.startswith('+') and not line.startswith('+++')),
            "linhas_removidas": sum(1 for line in diff if line.startswith('-') and not line.startswith('---')),
        }

    def apply_patch(self, base_code: str, patch_text: str) -> Optional[str]:
        """
        Aplica um patch a um código base.
        Esta é uma implementação simplificada. Para casos complexos,
        bibliotecas como 'patch' são mais robustas.
        """
        if not patch_text.strip():
            return base_code

        try:
            # difflib não tem uma função direta para aplicar patches.
            # A lógica para aplicar um diff pode ser complexa.
            # A abordagem aqui é uma heurística simples para adições e remoções.

            base_lines = base_code.splitlines()
            patch_lines = patch_text.splitlines()

            result_lines = list(base_lines)

            # Pular o cabeçalho do diff
            patch_lines = [line for line in patch_lines if not line.startswith('---') and not line.startswith('+++')]

            for line in patch_lines:
                if line.startswith('@@'):
                    continue # Ignorar marcadores de linha por simplicidade
                elif line.startswith('+'):
                    # Tenta encontrar um lugar para inserir a linha
                    # Esta é a parte mais complexa e frágil
                    result_lines.append(line[1:]) # Adiciona no final
                elif line.startswith('-'):
                    line_to_remove = line[1:]
                    if line_to_remove in result_lines:
                        result_lines.remove(line_to_remove)

            return '\n'.join(result_lines)
        except Exception as e:
            print(f"Erro ao aplicar patch: {e}")
            return None
