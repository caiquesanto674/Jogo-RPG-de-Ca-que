# SCRIPT DE AUTOANÁLISE
# ========================
# Este script importa o NexusDiagnosticCore do motor principal
# e o utiliza para escanear e gerar um relatório do projeto.

from nexus_engine import NexusDiagnosticCore
import json

if __name__ == "__main__":
    print("Iniciando autoanálise do projeto...")

    # Inicializa o núcleo de diagnóstico
    diagnostic = NexusDiagnosticCore()

    # Escaneia o projeto (o diretório atual)
    diagnostic.scan_project()

    # Detecta conflitos de nomes (não deve haver, pois tudo está em um arquivo)
    diagnostic.detect_name_conflicts()

    # Gera o relatório final
    report = diagnostic.generate_report()

    # Imprime um resumo do relatório
    print("\n===== RELATÓRIO DA AUTOANÁLISE =====")
    print(f"  - Timestamp: {report['timestamp']}")
    print(f"  - Total de arquivos .py analisados: {report['total_arquivos']}")
    print(f"  - Warnings encontrados: {len(report['warnings'])}")
    print(f"  - Erros encontrados: {len(report['errors'])}")

    # Salva o relatório completo em um arquivo para inspeção
    with open("analise_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\nRelatório completo salvo em 'analise_report.json'.")
    print("Autoanálise concluída com sucesso!")
