"""
NEXUS ENGINE 7K - VERSÃO UNIFICADA E CORRIGIDA
=============================================
Sistema consolidado sem duplicações e com bugs corrigidos
"""

import uuid
import random
import math
import re
import ast
import hashlib
import difflib
import os
import json
import shutil
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set, Tuple

# ============================================================
# 1. SISTEMA DE LOG OTIMIZADO
# ============================================================

class UniversalLog:
    def __init__(self, max_log: int = 5000):
        self.eventos: List[Dict[str, Any]] = []
        self._max_log = max_log
        self._indice_por_tipo: Dict[str, List[int]] = {}

    def registrar(self, origem: str, tipo: str, dados: Dict[str, Any]) -> str:
        """Registra evento com índice para busca rápida"""
        evento_id = str(uuid.uuid4())
        evento = {
            "id": evento_id,
            "origem": origem,
            "tipo": tipo,
            "dados": dados,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.eventos.append(evento)

        # Atualizar índice
        if tipo not in self._indice_por_tipo:
            self._indice_por_tipo[tipo] = []
        self._indice_por_tipo[tipo].append(len(self.eventos) - 1)

        # Limitar tamanho mantendo índices consistentes
        if len(self.eventos) > self._max_log:
            eventos_removidos = len(self.eventos) - self._max_log
            self.eventos = self.eventos[-self._max_log:]

            # Reconstruir índices (mais simples que manter)
            self._reconstruir_indices()

        return evento_id

    def _reconstruir_indices(self):
        """Reconstrói índices após remoção de eventos antigos"""
        self._indice_por_tipo = {}
        for idx, evento in enumerate(self.eventos):
            tipo = evento["tipo"]
            if tipo not in self._indice_por_tipo:
                self._indice_por_tipo[tipo] = []
            self._indice_por_tipo[tipo].append(idx)

    def consultar(self, tipo: Optional[str] = None, limite: int = 100) -> List[Dict]:
        """Consulta rápida com índice"""
        if tipo is None:
            return self.eventos[-limite:] if limite else self.eventos

        if tipo not in self._indice_por_tipo:
            return []

        indices = self._indice_por_tipo[tipo][-limite:] if limite else self._indice_por_tipo[tipo]
        return [self.eventos[idx] for idx in indices if idx < len(self.eventos)]

    def buscar(self, filtro: callable) -> List[Dict]:
        """Busca personalizada"""
        return [e for e in self.eventos if filtro(e)]


# ============================================================
# 2. SISTEMA DE EVENTOS MELHORADO
# ============================================================

class Evento:
    def __init__(self, nome: str, origem: str, gravidade: int = 1,
                 dados: Optional[Dict[str, Any]] = None,
                 prioridade: int = 0):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.origem = origem
        self.gravidade = min(max(gravidade, 1), 10)  # 1-10
        self.dados = dados or {}
        self.tempo = datetime.utcnow()
        self.prioridade = prioridade  # 0=normal, 1=alta, 2=urgente

    def __repr__(self):
        return f"<Evento {self.nome} G{self.gravidade} P{self.prioridade}>"

    def __lt__(self, other):
        # Para ordenar por prioridade (maior primeiro) e tempo
        if self.prioridade != other.prioridade:
            return self.prioridade > other.prioridade
        return self.tempo < other.tempo


class GerenciadorEventos:
    def __init__(self, log: UniversalLog):
        self.log = log
        self.fila: List[Evento] = []
        self.handlers: Dict[str, List[callable]] = {}
        self._running = True

    def registrar_handler(self, tipo_evento: str, handler: callable):
        """Registra função para tratar tipo específico de evento"""
        if tipo_evento not in self.handlers:
            self.handlers[tipo_evento] = []
        self.handlers[tipo_evento].append(handler)

    def disparar(self, evento: Evento):
        """Dispara evento para processamento"""
        self.fila.append(evento)

        # Ordenar por prioridade
        self.fila.sort()

        self.log.registrar(
            origem=evento.origem,
            tipo="evento_disparado",
            dados={
                "evento": evento.nome,
                "gravidade": evento.gravidade,
                "prioridade": evento.prioridade,
                "dados": evento.dados
            }
        )

    def processar(self) -> List[Evento]:
        """Processa eventos na fila"""
        if not self.fila:
            return []

        eventos_processados = []
        eventos_urgentes = [e for e in self.fila if e.prioridade >= 2]
        eventos_normais = [e for e in self.fila if e.prioridade < 2]

        # Processar urgentes primeiro
        for evento in eventos_urgentes:
            self._executar_handlers(evento)
            eventos_processados.append(evento)
            self.fila.remove(evento)

        # Processar até 10 eventos normais por ciclo
        for evento in eventos_normais[:10]:
            self._executar_handlers(evento)
            eventos_processados.append(evento)
            self.fila.remove(evento)

        return eventos_processados

    def _executar_handlers(self, evento: Evento):
        """Executa handlers registrados para o tipo de evento"""
        handlers = self.handlers.get(evento.nome, [])
        for handler in handlers:
            try:
                handler(evento)
            except Exception as e:
                self.log.registrar(
                    origem="GerenciadorEventos",
                    tipo="erro_handler",
                    dados={
                        "evento": evento.nome,
                        "handler": handler.__name__ if hasattr(handler, '__name__') else str(handler),
                        "erro": str(e)
                    }
                )


# ============================================================
# 3. SISTEMA DE TEMPO CORRIGIDO
# ============================================================

class NexusTime:
    """Sistema de tempo com múltiplas linhas temporais"""

    def __init__(self, tempo_inicial: Optional[datetime] = None):
        self.velocidade = 1.0
        self.tempo_jogo = tempo_inicial or datetime(3000, 1, 1, 0, 0, 0)
        self.ultimo_tick = datetime.utcnow()
        self.pausado = False
        self.linhas_temporais: Dict[str, datetime] = {"principal": self.tempo_jogo}

    def tick(self) -> Optional[datetime]:
        """Avança o tempo se não estiver pausado"""
        if self.pausado:
            return self.tempo_jogo

        agora = datetime.utcnow()
        delta_real = (agora - self.ultimo_tick).total_seconds()
        self.ultimo_tick = agora

        avancar = delta_real * self.velocidade
        self.tempo_jogo += timedelta(seconds=avancar)
        self.linhas_temporais["principal"] = self.tempo_jogo

        return self.tempo_jogo

    def definir_velocidade(self, v: float):
        """Define velocidade do tempo (0.01 a 100.0)"""
        self.velocidade = max(0.01, min(100.0, v))

    def pausar(self):
        self.pausado = True

    def despausar(self):
        self.pausado = False
        self.ultimo_tick = datetime.utcnow()

    def criar_linha_temporal(self, nome: str, tempo: Optional[datetime] = None):
        """Cria linha temporal alternativa"""
        self.linhas_temporais[nome] = tempo or self.tempo_jogo

    def saltar_para(self, tempo: datetime, linha: str = "principal"):
        """Salta para tempo específico"""
        if linha in self.linhas_temporais:
            self.linhas_temporais[linha] = tempo
            if linha == "principal":
                self.tempo_jogo = tempo


# ============================================================
# 4. ENTIDADE COM VALIDAÇÃO COMPLETA
# ============================================================

class EnergiaUniversal:
    """Energia com limites e regeneração inteligente"""

    def __init__(self, maxima: float = 1000.0, regeneracao: float = 5.0,
                 custo_regeneracao: float = 0.0):
        self.maxima = float(maxima)
        self.atual = float(maxima)
        self.regeneracao_base = float(regeneracao)
        self.custo_regeneracao = float(custo_regeneracao)
        self.ultima_regeneracao = datetime.utcnow()

    def consumir(self, valor: float, forcar: bool = False) -> Tuple[bool, float]:
        """
        Consome energia. Retorna (sucesso, quantidade_consumida)
        """
        valor = float(valor)
        if valor <= 0:
            return False, 0.0

        if forcar:
            consumido = min(valor, self.atual)
            self.atual -= consumido
            return True, consumido

        if valor <= self.atual:
            self.atual -= valor
            return True, valor

        return False, 0.0

    def regenerar(self) -> float:
        """Regenera energia baseada no tempo passado"""
        agora = datetime.utcnow()
        delta = (agora - self.ultima_regeneracao).total_seconds()
        self.ultima_regeneracao = agora

        regenerado = self.regeneracao_base * delta
        if regenerado > 0 and self.custo_regeneracao > 0:
            # Alguns sistemas podem ter custo para regenerar
            regenerado -= self.custo_regeneracao

        self.atual = min(self.maxima, self.atual + max(0, regenerado))
        return regenerado

    def pode_consumir(self, valor: float) -> bool:
        """Verifica se pode consumir sem realmente consumir"""
        return self.atual >= valor


class StatusEffect:
    """Efeito de status aplicado a entidades"""

    def __init__(self, nome: str, duracao: float, intensidade: float = 1.0):
        self.nome = nome
        self.duracao_total = duracao
        self.duracao_restante = duracao
        self.intensidade = intensidade
        self.aplicado_em = datetime.utcnow()

    def atualizar(self, delta_tempo: float) -> bool:
        """Atualiza duração, retorna True se ainda ativo"""
        self.duracao_restante -= delta_tempo
        return self.duracao_restante > 0


class Entidade:
    """Entidade base com sistema de status effects"""

    def __init__(self, nome: str, nivel: int = 1):
        if not nome or not isinstance(nome, str):
            raise ValueError("Nome da entidade inválido")
        if nivel < 1:
            raise ValueError("Nível deve ser >= 1")

        self.id = str(uuid.uuid4())
        self.nome = nome
        self.nivel = nivel

        # Atributos base
        self.hp_max = 100 + nivel * 10
        self.hp = self.hp_max
        self.energia = EnergiaUniversal(500 + nivel * 25)

        # Status
        self.inventario: List[str] = []
        self.afeto = 0.0  # -100 a 100
        self.volicao = 1.0  # 0.1 a 10.0
        self.status_effects: List[StatusEffect] = []
        self.imunidades: Set[str] = set()
        self.vivo = True

        # Posição
        self.posicao = {"x": 0.0, "y": 0.0, "z": 0.0}

    def receber_dano(self, valor: float, tipo: str = "fisico",
                     origem: Optional[str] = None) -> float:
        """
        Recebe dano com tipo. Retorna dano real recebido.
        """
        if not self.vivo:
            return 0.0

        # Verificar imunidades
        if tipo in self.imunidades:
            return 0.0

        # Aplicar reduções baseadas em status
        dano_real = valor

        # Verificar se tem efeito de vulnerabilidade/resistência
        for effect in self.status_effects:
            if effect.nome == f"vulneravel_{tipo}":
                dano_real *= (1.0 + effect.intensidade)
            elif effect.nome == f"resistente_{tipo}":
                dano_real *= (1.0 - effect.intensidade)

        self.hp = max(0, self.hp - dano_real)

        if self.hp <= 0:
            self.vivo = False
            self.morrer(origem)

        return dano_real

    def curar(self, valor: float, ignorar_maximo: bool = False) -> float:
        """Cura a entidade"""
        if not self.vivo:
            return 0.0

        curado = min(valor, self.hp_max - self.hp) if not ignorar_maximo else valor
        self.hp += curado

        if not ignorar_maximo and self.hp > self.hp_max:
            self.hp = self.hp_max

        return curado

    def aplicar_status(self, effect: StatusEffect) -> bool:
        """Aplica status effect se não for imune"""
        if effect.nome in self.imunidades:
            return False

        # Verificar se já tem o efeito
        for existing in self.status_effects:
            if existing.nome == effect.nome:
                # Renova ou intensifica
                existing.duracao_restante = max(
                    existing.duracao_restante,
                    effect.duracao_restante
                )
                existing.intensidade = max(
                    existing.intensidade,
                    effect.intensidade
                )
                return True

        self.status_effects.append(effect)
        return True

    def atualizar_status(self, delta_tempo: float):
        """Atualiza todos os status effects"""
        ativos = []
        for effect in self.status_effects:
            if effect.atualizar(delta_tempo):
                ativos.append(effect)
        self.status_effects = ativos

    def morrer(self, origem: Optional[str] = None):
        """Processa morte da entidade"""
        self.vivo = False
        self.hp = 0
        # Limpar status effects
        self.status_effects.clear()

    def reviver(self, hp_percent: float = 0.5):
        """Revive a entidade"""
        if self.vivo:
            return False

        self.vivo = True
        self.hp = self.hp_max * hp_percent
        return True

    def __repr__(self):
        status = "VIVO" if self.vivo else "MORTO"
        return f"<Entidade {self.nome} N{self.nivel} HP:{self.hp}/{self.hp_max} [{status}]>"


# ============================================================
# 5. NEXUS ENGINE UNIFICADO
# ============================================================

class NexusEngine:
    """Motor principal unificado"""

    def __init__(self, nome_mundo: str = "Aetheria"):
        self.nome = nome_mundo
        self.log = UniversalLog()
        self.eventos = GerenciadorEventos(self.log)
        self.tempo = NexusTime()

        # Registros
        self.entidades: Dict[str, Entidade] = {}
        self.universos: Dict[str, Dict] = {}
        self.sistemas: Dict[str, Any] = {}

        # Estado
        self.rodando = False
        self.ultimo_update = datetime.utcnow()

        # Registrar handlers básicos
        self._registrar_handlers()

    def _registrar_handlers(self):
        """Registra handlers padrão"""
        self.eventos.registrar_handler("entidade_dano", self._handler_dano)
        self.eventos.registrar_handler("entidade_cura", self._handler_cura)
        self.eventos.registrar_handler("entidade_morte", self._handler_morte)

    def _handler_dano(self, evento: Evento):
        """Handler para eventos de dano"""
        dados = evento.dados
        entidade_id = dados.get("entidade_id")
        dano = dados.get("dano", 0)

        if entidade_id in self.entidades:
            entidade = self.entidades[entidade_id]
            tipo = dados.get("tipo", "fisico")
            origem = dados.get("origem")

            dano_real = entidade.receber_dano(dano, tipo, origem)

            self.log.registrar(
                origem="NexusEngine",
                tipo="dano_aplicado",
                dados={
                    "entidade": entidade.nome,
                    "dano_solicitado": dano,
                    "dano_real": dano_real,
                    "tipo": tipo,
                    "hp_restante": entidade.hp,
                    "vivo": entidade.vivo
                }
            )

            # Se morreu, disparar evento de morte
            if not entidade.vivo:
                self.eventos.disparar(Evento(
                    nome="entidade_morte",
                    origem="NexusEngine",
                    gravidade=3,
                    dados={
                        "entidade_id": entidade_id,
                        "entidade_nome": entidade.nome,
                        "causa": tipo,
                        "origem": origem
                    },
                    prioridade=1
                ))

    def _handler_cura(self, evento: Evento):
        """Handler para eventos de cura"""
        dados = evento.dados
        entidade_id = dados.get("entidade_id")
        cura = dados.get("cura", 0)

        if entidade_id in self.entidades:
            entidade = self.entidades[entidade_id]
            curado = entidade.curar(cura)

            self.log.registrar(
                origem="NexusEngine",
                tipo="cura_aplicada",
                dados={
                    "entidade": entidade.nome,
                    "cura_solicitada": cura,
                    "cura_real": curado,
                    "hp_atual": entidade.hp
                }
            )

    def _handler_morte(self, evento: Evento):
        """Handler para eventos de morte"""
        dados = evento.dados
        entidade_id = dados.get("entidade_id")

        if entidade_id in self.entidades:
            entidade = self.entidades[entidade_id]

            self.log.registrar(
                origem="NexusEngine",
                tipo="entidade_morta",
                dados={
                    "entidade": entidade.nome,
                    "nivel": entidade.nivel,
                    "causa": dados.get("causa", "desconhecida")
                }
            )

    def iniciar(self):
        """Inicia o motor"""
        if self.rodando:
            return

        self.rodando = True
        self.ultimo_update = datetime.utcnow()

        self.log.registrar(
            origem="NexusEngine",
            tipo="sistema_iniciado",
            dados={
                "nome": self.nome,
                "tempo": self.tempo.tempo_jogo.isoformat(),
                "versao": "7K_unificado"
            }
        )

        # Iniciar sistemas registrados
        for nome, sistema in self.sistemas.items():
            if hasattr(sistema, 'iniciar'):
                sistema.iniciar()
                self.log.registrar(
                    origem="NexusEngine",
                    tipo="sistema_iniciado",
                    dados={"sistema": nome}
                )

    def registrar_entidade(self, entidade: Entidade):
        """Registra entidade no motor"""
        if entidade.id in self.entidades:
            raise ValueError(f"Entidade {entidade.id} já registrada")

        self.entidades[entidade.id] = entidade

        self.eventos.disparar(Evento(
            nome="entidade_registrada",
            origem="NexusEngine",
            dados={
                "entidade_id": entidade.id,
                "nome": entidade.nome,
                "nivel": entidade.nivel
            }
        ))

    def registrar_sistema(self, nome: str, sistema: Any):
        """Registra sistema adicional"""
        self.sistemas[nome] = sistema

    def update(self):
        """Atualiza o motor (chamar em loop)"""
        if not self.rodando:
            return

        agora = datetime.utcnow()
        delta_tempo = (agora - self.ultimo_update).total_seconds()
        self.ultimo_update = agora

        # Atualizar tempo
        tempo_atual = self.tempo.tick()

        # Processar eventos
        eventos_processados = self.eventos.processar()

        # Atualizar entidades
        for entidade in self.entidades.values():
            if entidade.vivo:
                # Atualizar status effects
                entidade.atualizar_status(delta_tempo)
                # Regenerar energia
                entidade.energia.regenerar()

        # Atualizar sistemas registrados
        for nome, sistema in self.sistemas.items():
            if hasattr(sistema, 'update'):
                sistema.update(delta_tempo)

        return {
            "tempo": tempo_atual,
            "delta_tempo": delta_tempo,
            "eventos_processados": len(eventos_processados),
            "entidades_vivas": sum(1 for e in self.entidades.values() if e.vivo)
        }

    def parar(self):
        """Para o motor"""
        self.rodando = False

        self.log.registrar(
            origem="NexusEngine",
            tipo="sistema_parado",
            dados={
                "tempo_jogo": self.tempo.tempo_jogo.isoformat(),
                "total_entidades": len(self.entidades)
            }
        )


# ============================================================
# 6. NEXUS GUARDIAN CORRIGIDO
# ============================================================

class StructuralAnalyzer:
    """Analisador estrutural com tratamento de erros"""

    def map_file(self, code: str, name: str) -> Dict:
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {
                "functions": [],
                "classes": [],
                "imports": [],
                "hash": hashlib.sha256(code.encode()).hexdigest(),
                "erro_sintaxe": str(e),
                "valido": False
            }

        structure = {
            "functions": [],
            "classes": [],
            "imports": [],
            "hash": hashlib.sha256(code.encode()).hexdigest(),
            "valido": True
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                structure["functions"].append({
                    "nome": node.name,
                    "args": len(node.args.args),
                    "linha": node.lineno
                })
            elif isinstance(node, ast.ClassDef):
                structure["classes"].append({
                    "nome": node.name,
                    "linha": node.lineno,
                    "metodos": [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                })
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                structure["imports"].append(ast.unparse(node))

        return structure


class AutoHealEngine:
    """Motor de autocura corrigido"""

    def heal_syntax(self, code: str) -> str:
        fixed = code

        # Remover caracteres de controle
        fixed = ''.join(char for char in fixed if ord(char) >= 32 or char in '\n\t\r')

        # Corrigir indentação (substituir tabs por espaços)
        fixed = re.sub(r'\t', '    ', fixed)

        # Contar e corrigir parênteses/colchetes/chaves desbalanceados
        # Usamos uma abordagem mais segura:
        lines = fixed.split('\n')
        fixed_lines = []

        for line in lines:
            # Verificar e adicionar fechamentos necessários no final da linha
            # (esta é uma heurística simples)
            if line.count('(') > line.count(')'):
                line += ')' * (line.count('(') - line.count(')'))
            if line.count('[') > line.count(']'):
                line += ']' * (line.count('[') - line.count(']'))
            if line.count('{') > line.count('}'):
                line += '}' * (line.count('{') - line.count('}'))
            fixed_lines.append(line)

        fixed = '\n'.join(fixed_lines)

        return fixed

    def heal_structure(self, code: str) -> str:
        """Remove duplicações acidentais"""
        lines = code.split('\n')
        cleaned = []
        seen_function_defs = set()

        i = 0
        while i < len(lines):
            line = lines[i]

            # Detectar e corrigir "def def função"
            if re.match(r'^\s*def\s+def\s+', line):
                line = re.sub(r'def\s+def\s+', 'def ', line)

            # Evitar duplicação consecutiva de funções
            if line.strip().startswith('def '):
                func_sig = line.strip()
                if func_sig in seen_function_defs:
                    # Pular até próxima função ou fim
                    i += 1
                    while i < len(lines) and not lines[i].strip().startswith(('def ', 'class ')):
                        i += 1
                    continue
                seen_function_defs.add(func_sig)

            cleaned.append(line)
            i += 1

        return '\n'.join(cleaned)


class PatchSystemCorrigido:
    """Sistema de patches corrigido"""

    def generate_patch(self, original: str, modified: str) -> Dict:
        """Gera patch usando difflib corretamente"""
        diff = list(difflib.unified_diff(
            original.splitlines(keepends=True),
            modified.splitlines(keepends=True),
            fromfile='original',
            tofile='modified',
            lineterm='\n'
        ))

        patch_text = ''.join(diff)
        patch_id = hashlib.sha1(patch_text.encode()).hexdigest()

        return {
            "id": patch_id,
            "timestamp": datetime.now().isoformat(),
            "patch": patch_text,
            "tamanho": len(patch_text)
        }

    def apply_patch(self, base: str, patch_text: str) -> Optional[str]:
        """Aplica patch usando difflib"""
        try:
            # Parse do patch
            patch = difflib.unified_diff(
                [],
                [],
                fromfile='original',
                tofile='modified',
                lineterm=''
            )
            # Esta é uma versão simplificada
            # Em produção, usar biblioteca como unidiff
            lines = patch_text.split('\n')
            result = base.split('\n')

            # Aplicar mudanças (simplificado)
            i = 0
            while i < len(lines):
                line = lines[i]
                if line.startswith('@@'):
                    i += 1
                    continue
                elif line.startswith('+') and not line.startswith('+++'):
                    result.append(line[1:])
                elif line.startswith('-') and not line.startswith('---'):
                    # Remover linha
                    to_remove = line[1:]
                    if to_remove in result:
                        result.remove(to_remove)
                i += 1

            return '\n'.join(result)
        except Exception as e:
            print(f"Erro ao aplicar patch: {e}")
            return None


class TestExecutor:
    """Executor de testes melhorado"""

    def run_basic_tests(self, code: str) -> Dict:
        result = {
            "timestamp": datetime.now().isoformat(),
            "sintaxe": "OK",
            "funcoes_essenciais": {},
            "complexidade": len(code) // 1000,  # Por mil linhas
            "erros": []
        }

        # Teste de sintaxe
        try:
            compile(code, "<string>", "exec")
        except Exception as e:
            result["sintaxe"] = f"ERRO: {str(e)}"
            result["erros"].append(str(e))

        # Verificar funções essenciais
        essential_patterns = {
            "classe": r'class\s+\w+',
            "funcao": r'def\s+\w+',
            "import": r'import\s+\w+|from\s+\w+\s+import'
        }

        for nome, pattern in essential_patterns.items():
            if re.search(pattern, code):
                result["funcoes_essenciais"][nome] = "ENCONTRADO"
            else:
                result["funcoes_essenciais"][nome] = "AUSENTE"

        return result


class MemoryKernel:
    """Kernel de memória para armazenar análises"""

    def __init__(self):
        self.records: Dict[str, Dict] = {}

    def store(self, name: str, data: Dict):
        self.records[name] = {
            "data": data,
            "saved": datetime.now().isoformat(),
            "size": len(str(data))
        }

    def get(self, name: str) -> Optional[Dict]:
        return self.records.get(name)

class SemanticAnalyzer:
    def __init__(self):
        self.semantic_memory = {}

    def analyze(self, code: str, file_name: str):
        """Extrai significado, propósito e domínios de cada arquivo."""
        keywords = [
            "sistema", "engine", "militar", "mundo", "rpg",
            "economia", "AI", "combate", "inventário",
            "classe", "magia", "unificação", "multiverso"
        ]

        detected = [kw for kw in keywords if kw in code.lower()]
        summary = {
            "file": file_name,
            "concepts": detected,
            "complexity": len(code) // 400
        }

        self.semantic_memory[file_name] = summary
        return summary

class NexusGuardian:
    """Sistema de análise e autocorreção unificado"""

    def __init__(self):
        self.analisador = StructuralAnalyzer()
        self.semantico = SemanticAnalyzer()
        self.auto_heal = AutoHealEngine()
        self.patch_system = PatchSystemCorrigido()
        self.testes = TestExecutor()
        self.memoria = MemoryKernel()

    def analisar_codigo(self, codigo: str, nome_arquivo: str) -> Dict:
        """Análise completa de código"""
        # Primeiro, tentar curar
        # codigo_curado = self.auto_heal.heal_syntax(codigo)
        # codigo_curado = self.auto_heal.heal_structure(codigo_curado)
        codigo_curado = codigo

        # Analisar estrutura
        estrutura = self.analisador.map_file(codigo_curado, nome_arquivo)

        # Analisar semântica
        semantica = self.semantico.analyze(codigo_curado, nome_arquivo)

        # Executar testes básicos
        resultados_teste = self.testes.run_basic_tests(codigo_curado)

        # Armazenar na memória
        self.memoria.store(nome_arquivo, {
            "estrutura": estrutura,
            "semantica": semantica,
            "testes": resultados_teste,
            "hash": hashlib.sha256(codigo_curado.encode()).hexdigest()
        })

        return {
            "arquivo": nome_arquivo,
            "curado": codigo != codigo_curado,
            "estrutura": estrutura,
            "semantica": semantica,
            "testes": resultados_teste
        }

# ============================================================
# 7. SISTEMA DE DIAGNÓSTICO
# ============================================================

class NexusDiagnosticCore:
    """Núcleo de diagnóstico completo"""

    def __init__(self, root: str = ".", max_file_size: int = 1024):
        self.root = root
        self.max_file_size_kb = max_file_size
        self.reports: Dict[str, FileReport] = {}
        self.warnings: List[str] = []
        self.errors: List[str] = []
        self.guardian = NexusGuardian()

    def scan_project(self):
        """Escaneia todo o projeto"""
        for root_dir, dirs, files in os.walk(self.root):
            # Ignorar diretórios especiais
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']

            for file in files:
                if file.endswith('.py'):
                    fullpath = os.path.join(root_dir, file)
                    self._analyze_file(fullpath)

    def _analyze_file(self, path: str):
        """Analisa arquivo individual"""
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Analisar com Guardian
            analise = self.guardian.analisar_codigo(content, path)

            report = FileReport(path)
            report.lines = content.count('\n')
            report.size_kb = len(content) / 1024
            report.hash = hashlib.md5(content.encode()).hexdigest()
            report.last_modified = datetime.fromtimestamp(os.path.getmtime(path))
            report.analise = analise

            self.reports[path] = report

            # Verificar problemas
            if report.size_kb > self.max_file_size_kb:
                self.warnings.append(f"Arquivo muito grande: {path} ({report.size_kb:.1f}KB)")

            if analise.get("testes", {}).get("sintaxe", "").startswith("ERRO"):
                self.errors.append(f"Erro de sintaxe em: {path}")

        except Exception as e:
            self.errors.append(f"Erro ao analisar {path}: {str(e)}")

    def detect_name_conflicts(self):
        """Detecta conflitos de nomes"""
        function_map = {}
        class_map = {}

        for path, report in self.reports.items():
            analise = getattr(report, 'analise', {})
            estrutura = analise.get('estrutura', {})

            for func in estrutura.get('functions', []):
                func_name = func.get('nome', '') if isinstance(func, dict) else func
                function_map.setdefault(func_name, []).append(path)

            for cls in estrutura.get('classes', []):
                cls_name = cls.get('nome', '') if isinstance(cls, dict) else cls
                class_map.setdefault(cls_name, []).append(path)

        for name, paths in function_map.items():
            if len(paths) > 1:
                self.warnings.append(f"Função duplicada: '{name}' em {paths}")

        for name, paths in class_map.items():
            if len(paths) > 1:
                self.warnings.append(f"Classe duplicada: '{name}' em {paths}")

    def generate_report(self) -> Dict:
        """Gera relatório completo"""
        return {
            "timestamp": datetime.now().isoformat(),
            "total_arquivos": len(self.reports),
            "warnings": self.warnings,
            "errors": self.errors,
            "files": {
                path: {
                    "lines": report.lines,
                    "size_kb": report.size_kb,
                    "hash": report.hash,
                    "last_modified": report.last_modified.isoformat() if report.last_modified else None,
                    "analise_valida": getattr(report, 'analise', {}).get('estrutura', {}).get('valido', False)
                }
                for path, report in self.reports.items()
            }
        }


class FileReport:
    """Relatório de arquivo"""
    def __init__(self, path: str):
        self.path = path
        self.lines = 0
        self.size_kb = 0
        self.hash = ""
        self.last_modified = None
        self.analise = {}


# ============================================================
# 8. SISTEMA DE BACKUP E RESTAURAÇÃO
# ============================================================

class CronosBackupSystem:
    """Sistema de backup robusto"""

    def __init__(self, root: str = ".", backup_root: str = "./backups"):
        self.root = root
        self.backup_root = backup_root

        # Criar diretório de backups se não existir
        os.makedirs(backup_root, exist_ok=True)

        # Timeline
        self.timeline_path = os.path.join(backup_root, "timeline.json")
        self._ensure_timeline()

    def _ensure_timeline(self):
        """Garante que a timeline existe"""
        if not os.path.exists(self.timeline_path):
            with open(self.timeline_path, 'w') as f:
                json.dump([], f, indent=2)

    def create_snapshot(self, descricao: str = "") -> str:
        """Cria snapshot do projeto"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_name = f"snapshot_{timestamp}"
        snapshot_path = os.path.join(self.backup_root, snapshot_name)

        try:
            # Ignorar o próprio diretório de backup para evitar recursão infinita
            ignore_list = shutil.ignore_patterns('*.pyc', '__pycache__', '.git', os.path.basename(self.backup_root))

            # Copiar diretório
            shutil.copytree(self.root, snapshot_path,
                          dirs_exist_ok=True,
                          ignore=ignore_list)

            # Registrar na timeline
            self._register_snapshot(snapshot_name, descricao)

            return snapshot_path

        except Exception as e:
            raise Exception(f"Erro ao criar snapshot: {str(e)}")

    def _register_snapshot(self, snapshot_name: str, descricao: str):
        """Registra snapshot na timeline"""
        with open(self.timeline_path, 'r') as f:
            timeline = json.load(f)

        timeline.append({
            "name": snapshot_name,
            "timestamp": datetime.now().isoformat(),
            "description": descricao
        })

        with open(self.timeline_path, 'w') as f:
            json.dump(timeline, f, indent=2)

    def list_snapshots(self) -> List[Dict]:
        """Lista snapshots disponíveis"""
        if not os.path.exists(self.backup_root):
            return []

        snapshots = []
        for item in os.listdir(self.backup_root):
            if item.startswith('snapshot_'):
                path = os.path.join(self.backup_root, item)
                if os.path.isdir(path):
                    snapshots.append({
                        "name": item,
                        "path": path,
                        "created": os.path.getctime(path)
                    })

        return sorted(snapshots, key=lambda x: x["created"], reverse=True)

    def restore_snapshot(self, snapshot_name: str, backup_current: bool = True):
        """Restaura snapshot"""
        snapshot_path = os.path.join(self.backup_root, snapshot_name)

        if not os.path.exists(snapshot_path):
            raise FileNotFoundError(f"Snapshot não encontrado: {snapshot_name}")

        # Backup do estado atual
        if backup_current:
            self.create_snapshot(f"Pre-restore de {snapshot_name}")

        # Restaurar
        for item in os.listdir(snapshot_path):
            src = os.path.join(snapshot_path, item)
            dst = os.path.join(self.root, item)

            # Remover destino se existir
            if os.path.exists(dst):
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                else:
                    os.remove(dst)

            # Copiar
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)

        return True


# ============================================================
# 9. SISTEMA DE ESTRUTURA DE PROJETO
# ============================================================

class AtlasStructureGuard:
    """Guarda a estrutura do projeto"""

    def __init__(self, project_name: str = "apolo_engine"):
        self.project_name = project_name
        self.structure = {
            "core": [
                "engine.py",
                "entities.py",
                "world.py",
                "systems.py"
            ],
            "rpg": [
                "characters/",
                "skills/",
                "items/",
                "quests/"
            ],
            "systems": [
                "combat/",
                "economy/",
                "ai/",
                "physics/"
            ],
            "utils": [
                "logger.py",
                "config.py",
                "helpers.py"
            ],
            "assets": [
                "images/",
                "sounds/",
                "data/"
            ]
        }

    def ensure_structure(self, root: str = "."):
        """Garante que a estrutura existe"""
        project_root = os.path.join(root, self.project_name)
        os.makedirs(project_root, exist_ok=True)

        for category, items in self.structure.items():
            category_path = os.path.join(project_root, category)
            os.makedirs(category_path, exist_ok=True)

            for item in items:
                item_path = os.path.join(category_path, item)

                if item.endswith('/'):  # É diretório
                    os.makedirs(item_path, exist_ok=True)
                    self._create_anchor(item_path)
                else:  # É arquivo
                    if not os.path.exists(item_path):
                        self._create_file(item_path, category, item)

    def _create_anchor(self, directory: str):
        """Cria arquivo âncora em diretório vazio"""
        anchor_file = os.path.join(directory, ".anchor")
        if not os.path.exists(anchor_file):
            with open(anchor_file, 'w') as f:
                f.write(f"Diretório criado por AtlasStructureGuard\n")
                f.write(f"Data: {datetime.now().isoformat()}\n")

    def _create_file(self, filepath: str, category: str, name: str):
        """Cria arquivo base com conteúdo padrão"""
        content = f"""# {self.project_name} - {category}/{name}
# Criado automaticamente por AtlasStructureGuard
# Data: {datetime.now().isoformat()}

\"\"\"
Módulo: {category}.{name.replace('.py', '')}
\"\"\"

import sys
from typing import Any, Dict, List, Optional


def init():
    \"\"\"Inicialização do módulo\"\"\"
    return True


if __name__ == "__main__":
    print(f"Módulo {category}.{name} carregado")
"""

        with open(filepath, 'w') as f:
            f.write(content)


# ============================================================
# 10. EXEMPLO DE USO E TESTE
# ============================================================

def test_nexus_engine():
    """Testa o Nexus Engine"""
    print("=" * 60)
    print("TESTE DO NEXUS ENGINE 7K - VERSÃO UNIFICADA")
    print("=" * 60)

    # 1. Criar motor
    engine = NexusEngine("Teste Mundo")

    # 2. Criar entidades
    heroi = Entidade("Herói", nivel=5)
    vilao = Entidade("Vilão", nivel=6)

    engine.registrar_entidade(heroi)
    engine.registrar_entidade(vilao)

    print(f"\nEntidades criadas:")
    print(f"  - {heroi}")
    print(f"  - {vilao}")

    # 3. Iniciar sistema
    engine.iniciar()

    # 4. Simular combate
    print("\nSimulando combate:")

    # Herói ataca vilão
    engine.eventos.disparar(Evento(
        nome="entidade_dano",
        origem="teste",
        dados={
            "entidade_id": vilao.id,
            "dano": 25.0,
            "tipo": "fisico",
            "origem": heroi.nome
        },
        prioridade=1
    ))

    # 5. Executar update
    for i in range(3):
        status = engine.update()
        print(f"\nUpdate {i + 1}:")
        print(f"  Tempo: {status['tempo']}")
        print(f"  Entidades vivas: {status['entidades_vivas']}")
        print(f"  HP Vilão: {vilao.hp}/{vilao.hp_max}")

        if not vilao.vivo:
            print("  Vilão morreu!")
            break

    # 6. Parar engine
    engine.parar()

    print(f"\nLog de eventos ({len(engine.log.eventos)} eventos):")
    for evento in engine.log.consultar(limite=5):
        print(f"  [{evento['timestamp']}] {evento['origem']}: {evento['tipo']}")


def test_diagnostic():
    """Testa o sistema de diagnóstico"""
    print("\n" + "=" * 60)
    print("TESTE DO SISTEMA DE DIAGNÓSTICO")
    print("=" * 60)

    # Criar arquivo de teste
    test_code = """
def hello():
    print("Hello World")

class TestClass:
    def method(self):
        return True
"""

    with open("test_file.py", "w") as f:
        f.write(test_code)

    # Executar diagnóstico
    diagnostic = NexusDiagnosticCore()
    diagnostic.scan_project()
    diagnostic.detect_name_conflicts()

    report = diagnostic.generate_report()

    print(f"\nRelatório de diagnóstico:")
    print(f"  Arquivos analisados: {report['total_arquivos']}")
    print(f"  Warnings: {len(report['warnings'])}")
    print(f"  Errors: {len(report['errors'])}")

    # Limpar
    if os.path.exists("test_file.py"):
        os.remove("test_file.py")


def test_backup():
    """Testa sistema de backup"""
    print("\n" + "=" * 60)
    print("TESTE DO SISTEMA DE BACKUP")
    print("=" * 60)

    backup = CronosBackupSystem(backup_root="./test_backups")

    # Criar snapshot
    snapshot = backup.create_snapshot("Teste de backup")
    print(f"\nSnapshot criado: {snapshot}")

    # Listar snapshots
    snapshots = backup.list_snapshots()
    print(f"\nSnapshots disponíveis: {len(snapshots)}")

    # Limpar
    if os.path.exists("./test_backups"):
        shutil.rmtree("./test_backups")


def main():
    """Função principal de teste"""
    try:
        test_nexus_engine()
        test_diagnostic()
        test_backup()

        print("\n" + "=" * 60)
        print("TESTES CONCLUÍDOS COM SUCESSO!")
        print("=" * 60)

    except Exception as e:
        print(f"\nERRO durante testes: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
