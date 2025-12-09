# Jogo do Monarca Caíque Ω

Este repositório contém a versão final e unificada do jogo do Monarca Caíque. O projeto é um script único, `jogo_unificado_final.py`, que combina elementos de simulação econômica, estratégia militar, avanço tecnológico e sistemas de IA.

## Como Executar o Jogo

Para jogar, basta executar o script principal a partir do seu terminal:

```bash
python jogo_unificado_final.py
```

O jogo rodará em um loop contínuo. Para encerrar, pressione `Ctrl+C`.

---

## Sistema de Integração Jules

Para ajudar a adicionar novos códigos ao jogo principal sem criar conflitos, foi desenvolvido o **Sistema de Integração Jules** (`integrador_jules.py`). Esta ferramenta funde um novo arquivo de código ao script principal de forma segura.

### Como Usar o Integrador

1.  **Crie seu Novo Módulo**: Escreva seu novo código (contendo novas classes ou funções) e salve-o em um arquivo separado (por exemplo, `meu_novo_modulo.py`).

2.  **Prepare o Integrador**:
    *   Abra o arquivo `integrador_jules.py`.
    *   No final do arquivo, dentro do bloco `if __name__ == '__main__':`, altere o valor da variável `novo_modulo` para o nome do arquivo que você acabou de criar.

    ```python
    if __name__ == '__main__':
        logging.info("Sistema de Integração Jules - Pronto para uso.")

        arquivo_principal = 'jogo_unificado_final.py'
        # MODIFIQUE A LINHA ABAIXO
        novo_modulo = 'meu_novo_modulo.py'
        arquivo_final = 'jogo_unificado_final.py'

        integrar_novo_modulo(arquivo_principal, novo_modulo, arquivo_final)
    ```

3.  **Execute o Integrador**:
    *   Salve suas alterações no `integrador_jules.py`.
    *   Execute-o a partir do terminal:

    ```bash
    python integrador_jules.py
    ```

4.  **Verifique o Resultado**:
    *   O integrador irá analisar os dois arquivos. Se não encontrar nenhuma classe ou função global com o mesmo nome, ele anexará seu novo código ao final do `jogo_unificado_final.py`.
    *   Se um conflito for detectado, a operação será cancelada, e o integrador informará qual nome está causando o conflito. Você precisará renomear o elemento no seu novo módulo antes de tentar novamente.

Este sistema garante que o jogo principal nunca seja corrompido por uma integração mal-sucedida.
