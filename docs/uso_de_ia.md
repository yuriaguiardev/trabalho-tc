# Registro do uso de Inteligência Artificial

> Documento exigido pelas orientações do trabalho (seção "Uso de
> Inteligência Artificial e integridade acadêmica").

---

## 1. Ferramenta utilizada

- **Nome:** Claude (Anthropic), modelo Claude Opus 4.7.
- **Interface:** Claude.ai (aplicativo web).
- **Data de uso:** _(preencher)_
- **Responsável pela interação:** _(preencher)_

## 2. Finalidades do uso

A ferramenta foi utilizada como **apoio** nos seguintes aspectos:

1. **Pesquisa e revisão conceitual** — esclarecimento de definições da
   disciplina (programa monolítico normalizado, relação de transição,
   equivalência forte vs. funcional, método da Máquina de Traços).
2. **Apoio ao desenvolvimento de código** — sugestão de estrutura para
   os programas em C, redação do programa monolítico em Assembly
   x86-64, esqueleto inicial da Máquina de Traços em Python.
3. **Redação e revisão textual** — melhoria de clareza nos comentários
   dos códigos-fonte, do README e dos documentos em `docs/`.
4. **Organização do repositório** — sugestões sobre estrutura de pastas
   e conteúdo mínimo do README.

## 3. Trechos/artefatos aproveitados

- Esqueleto das classes `Atribuicao`, `Teste`, `Pare`, `Programa`,
  `Configuracao` e `Traco` em `maquina-tracos/mt.py`.
- Formatação do traço em "formato de fita" (`formatar_fita`) e em
  tabela (`formatar_tabela`).
- Versão inicial dos quatro programas normalizados em
  `maquina-tracos/programas.py`.
- Esboço inicial dos programas em C (monolítico, iterativo,
  iterativo decrescente, recursivo).
- Esboço inicial do programa monolítico em Assembly NASM x86-64.
- Estrutura base deste próprio documento e do `README.md`.

## 4. Revisões/validações feitas pela equipe

A equipe realizou, por conta própria:

- **Teste de execução** de todos os programas em C, comparando a saída
  com valores esperados para `N ∈ {0, 1, 3, 5, 7}`.
- **Revisão da sintaxe NASM** e verificação de que o mapeamento para as
  instruções monolíticas normalizadas (rótulos 1–7) está correto.
- **Execução da Máquina de Traços** (`python3 executar.py`) e inspeção
  das oito saídas geradas em `maquina-tracos/saidas/`.
- **Verificação manual** da equivalência forte P1 × P2 e da
  não-equivalência forte P2 × P3 (conferindo, em tabelas, os estados
  passo a passo).
- **Revisão crítica do texto** em `docs/analise_formal.md` para
  garantir aderência à terminologia utilizada em sala de aula.
- **Preparação da apresentação** em sala, adaptando o conteúdo gerado
  ao contexto da disciplina e ao tempo disponível.

## 5. Declaração

A equipe declara que:

- o conteúdo entregue foi **compreendido, revisado e validado** por
  todos os integrantes;
- cada integrante é capaz de **explicar oralmente** o funcionamento de
  qualquer parte do trabalho durante a apresentação;
- a IA foi utilizada como ferramenta de apoio, **não substituindo** a
  responsabilidade acadêmica da equipe pelo conteúdo entregue.
