### GDD_APOLO — Resumo Executivo

* Título: **APOLO — O DOMÍNIO ÔMEGA**
* Gênero: RPG tático híbrido + Tycoon de base + ação psíquica (Sci-Fi Militar épico + Multiverso)
* Plataforma alvo: Android (APK), PC (Python protótipo) — futura conversão Godot/Unity
* Público: Adulto (temas psicológicos e violência estilizada)
* Estética: Neon militar + arquitetura monumental + efeitos cósmicos (paleta: preto, azul-cobalto, neon laranja, púrpura)
* Loop principal:

  1. Ciclo (turno) de gestão: operar base, gastar Éter, produzir SSSS
  2. Conflito (combate): Zarkon e legiões aplicam ataques psíquicos
  3. Suporte (AI): AICardinal e Calia mitigam, ativam defesas
  4. Reação (Monarca): Agony Overflow ativa quando Moral < 20
  5. Progresso (tycoon): Pesquisas e upgrades desbloqueiam mitigação

### Mecânicas chave

* Monarca: moral como recurso primário; Agony Overflow é a habilidade reativa que transforma derrota em ascensão
* Economia: Éter e Matéria Escura SSSS como recursos críticos para defesa psíquica
* Base: componentes que consomem mana e produzem recursos; upgrade psíquico reduz dano mental
* IA: Calia (campo) e Ciel (sistema global) — scripts para restauração automática (fail-safe)
* Combate: ataques físicos e psíquicos (psíquicos ignoram HP e reduzem Moral)
* Veículos: mechas com munição limitada e alcance tático

### Entregáveis técnicos

* Protótipo Python (protótipo funcional) — pronto (este que você recebeu)
* Projeto Godot 4 (próxima etapa) — GDScript + Scenes + Export presets para Android
* Pipeline de build: GitHub Actions que gera APK (keystore como secret) — eu preparo

### UI & UX principais

* HUD: Moral (barra), Mana/Éter, Recursos principais, Código de Protocolo
* Tela de batalha: grid tático + efeitos psíquicos (vfx shader)
* Menus: Pesquisa/Tech tree, Base overview, Logs do Nexus
* Audiovisual: trilha épica sintetizada + efeitos psíquicos graves
