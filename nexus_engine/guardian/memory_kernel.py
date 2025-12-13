"""
Módulo do Kernel de Memória do Nexus Guardian.
"""

from datetime import datetime
from typing import Dict, Optional, List

class MemoryKernel:
    """
    Kernel de memória para armazenar e recuperar os resultados das análises
    de código realizadas pelo Guardian.
    """

    def __init__(self):
        self.records: Dict[str, Dict] = {}

    def store(self, file_name: str, analysis_data: Dict) -> None:
        """
        Armazena os dados de análise de um arquivo.

        Args:
            file_name (str): O nome/caminho do arquivo, usado como chave.
            analysis_data (Dict): O dicionário contendo os resultados da análise.
        """
        self.records[file_name] = {
            "data": analysis_data,
            "timestamp": datetime.now().isoformat(),
            "size_bytes": len(str(analysis_data))
        }

    def retrieve(self, file_name: str) -> Optional[Dict]:
        """
        Recupera os dados de análise de um arquivo da memória.

        Args:
            file_name (str): O nome/caminho do arquivo a ser recuperado.

        Returns:
            Optional[Dict]: Os dados da análise ou None se não encontrado.
        """
        record = self.records.get(file_name)
        return record.get("data") if record else None

    def list_records(self) -> List[str]:
        """
        Lista os nomes de todos os arquivos cujas análises estão na memória.
        """
        return list(self.records.keys())

    def clear(self) -> int:
        """
        Limpa todos os registros da memória.

        Returns:
            int: O número de registros removidos.
        """
        num_records = len(self.records)
        self.records.clear()
        return num_records

    def get_summary(self) -> Dict:
        """
        Retorna um resumo do estado atual da memória.
        """
        total_size = sum(record.get("size_bytes", 0) for record in self.records.values())

        return {
            "total_records": len(self.records),
            "total_size_bytes": total_size,
            "latest_record_timestamp": max(
                (record["timestamp"] for record in self.records.values()),
                default=None
            )
        }
