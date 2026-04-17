#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=====================================================================
  PROGRAMAS NORMALIZADOS - forma aceita pela Maquina de Tracos
=====================================================================
  Todo programa analisado pela MT precisa estar na forma MONOLITICA
  NORMALIZADA. Os programas iterativo e recursivo escritos em C nao
  estao diretamente nessa forma, por isso aqui sao apresentadas as
  NORMALIZACOES correspondentes - exatamente as cadeias de instrucoes
  rotuladas que a MT vai interpretar.

  Cada programa aqui computa a funcao f(n) = n! e representa,
  conceitualmente, um dos programas implementados em C.
=====================================================================
"""

from mt import Programa, Atribuicao, Teste, Pare


# ---------------------------------------------------------------------
#  P1 - MONOLITICO CRESCENTE (espelha src/monolitico.c)
# ---------------------------------------------------------------------
#
#    1: faca RES <- 1                           ; va_para 2
#    2: faca I   <- 1                           ; va_para 3
#    3: se I > N entao va_para 7 senao va_para 4
#    4: faca RES <- RES * I                     ; va_para 5
#    5: faca I   <- I + 1                       ; va_para 6
#    6: va_para 3   (implementado como teste trivial "true")
#    7: pare
# ---------------------------------------------------------------------

programa_monolitico = Programa(
    nome="P1 - Monolitico crescente (goto)",
    entradas=["N"],
    saida="RES",
    inicio="1",
    instrucoes={
        "1": Atribuicao(var="RES",
                        expr=lambda s: 1,
                        descricao="RES <- 1",
                        proximo="2"),
        "2": Atribuicao(var="I",
                        expr=lambda s: 1,
                        descricao="I <- 1",
                        proximo="3"),
        "3": Teste(cond=lambda s: s["I"] > s["N"],
                   descricao="I > N",
                   rotulo_verdadeiro="7",
                   rotulo_falso="4"),
        "4": Atribuicao(var="RES",
                        expr=lambda s: s["RES"] * s["I"],
                        descricao="RES <- RES * I",
                        proximo="5"),
        "5": Atribuicao(var="I",
                        expr=lambda s: s["I"] + 1,
                        descricao="I <- I + 1",
                        proximo="3"),        # desvio incondicional para 3
        "7": Pare(),
    },
)


# ---------------------------------------------------------------------
#  P2 - ITERATIVO CRESCENTE NORMALIZADO (espelha src/iterativo.c)
# ---------------------------------------------------------------------
# O laco "while (I <= N)" e' normalizado para a mesma estrutura do
# programa monolitico crescente. E' EXATAMENTE o mesmo conjunto de
# instrucoes (apenas com rotulos renomeados) - por isso P1 e P2 sao
# FORTEMENTE EQUIVALENTES.
#
#    i1: faca RES <- 1
#    i2: faca I   <- 1
#    i3: se I > N entao va_para i7 senao va_para i4
#    i4: faca RES <- RES * I
#    i5: faca I   <- I + 1    (va_para i3)
#    i7: pare
# ---------------------------------------------------------------------

programa_iterativo = Programa(
    nome="P2 - Iterativo crescente (while, i:1->n)",
    entradas=["N"],
    saida="RES",
    inicio="i1",
    instrucoes={
        "i1": Atribuicao("RES", lambda s: 1, "RES <- 1", "i2"),
        "i2": Atribuicao("I",   lambda s: 1, "I <- 1",   "i3"),
        "i3": Teste(lambda s: s["I"] > s["N"], "I > N",
                    rotulo_verdadeiro="i7", rotulo_falso="i4"),
        "i4": Atribuicao("RES", lambda s: s["RES"] * s["I"],
                         "RES <- RES * I", "i5"),
        "i5": Atribuicao("I",   lambda s: s["I"] + 1, "I <- I + 1", "i3"),
        "i7": Pare(),
    },
)


# ---------------------------------------------------------------------
#  P3 - ITERATIVO DECRESCENTE NORMALIZADO
#                             (espelha src/iterativo_decrescente.c)
# ---------------------------------------------------------------------
# Mesmo resultado final (n!), mas as multiplicacoes ocorrem em ORDEM
# INVERSA. A sequencia de configuracoes difere - portanto P3 NAO e'
# fortemente equivalente a P1/P2, embora seja FUNCIONALMENTE igual.
#
#    d1: faca RES <- 1
#    d2: faca I   <- N
#    d3: se I < 1 entao va_para d7 senao va_para d4
#    d4: faca RES <- RES * I
#    d5: faca I   <- I - 1    (va_para d3)
#    d7: pare
# ---------------------------------------------------------------------

programa_iterativo_decrescente = Programa(
    nome="P3 - Iterativo decrescente (while, i:n->1)",
    entradas=["N"],
    saida="RES",
    inicio="d1",
    instrucoes={
        "d1": Atribuicao("RES", lambda s: 1,      "RES <- 1",  "d2"),
        "d2": Atribuicao("I",   lambda s: s["N"], "I <- N",    "d3"),
        "d3": Teste(lambda s: s["I"] < 1, "I < 1",
                    rotulo_verdadeiro="d7", rotulo_falso="d4"),
        "d4": Atribuicao("RES", lambda s: s["RES"] * s["I"],
                         "RES <- RES * I", "d5"),
        "d5": Atribuicao("I",   lambda s: s["I"] - 1, "I <- I - 1", "d3"),
        "d7": Pare(),
    },
)


# ---------------------------------------------------------------------
#  P4 - RECURSIVO NORMALIZADO (espelha src/recursivo.c)
# ---------------------------------------------------------------------
# A recursao e' simulada por uma PILHA explicita. Esta e' a tecnica
# classica de normalizacao: toda funcao recursiva pode ser escrita
# como programa monolitico usando uma pilha de ativacao.
#
# Variaveis:
#    N       - entrada
#    RES     - resultado
#    PILHA   - lista (usamos uma unica variavel int como "tamanho"
#              e armazenamos os valores em PILHA_<i>)  [simplificacao
#              didatica: modelamos a pilha conceitualmente]
#
# A MT, para efeito de exibicao na fita, imprimira os valores
# empilhados, deixando visivel a cadeia de ativacoes.
# ---------------------------------------------------------------------
# Fase 1 - DESCIDA: empilha N, N-1, N-2, ..., 1
#    r1 : faca RES   <- 1
#    r2 : faca TOPO  <- N
#    r3 : se TOPO < 1 entao va_para r7 senao va_para r4
#    r4 : faca empilha(TOPO)                    [PILHA cresce]
#    r5 : faca TOPO  <- TOPO - 1
#    r6 : va_para r3
# Fase 2 - SUBIDA: desempilha multiplicando
#    r7 : se PILHA vazia entao va_para r10 senao va_para r8
#    r8 : faca RES <- RES * topo(PILHA)
#    r9 : faca desempilha()                     ;  va_para r7
#    r10: pare
# ---------------------------------------------------------------------

def _empilha(s, valor):
    s.setdefault("_PILHA", [])
    s["_PILHA"].append(valor)
    s["TAM_PILHA"] = len(s["_PILHA"])
    return s["TAM_PILHA"]


def _desempilha(s):
    s["_PILHA"].pop()
    s["TAM_PILHA"] = len(s["_PILHA"])
    return s["TAM_PILHA"]


def _topo(s):
    return s["_PILHA"][-1] if s.get("_PILHA") else 0


programa_recursivo = Programa(
    nome="P4 - Recursivo normalizado (via pilha)",
    entradas=["N"],
    saida="RES",
    inicio="r1",
    instrucoes={
        "r1":  Atribuicao("RES",  lambda s: 1, "RES <- 1", "r2"),
        "r2":  Atribuicao("TOPO", lambda s: s["N"], "TOPO <- N", "r3"),
        "r3":  Teste(lambda s: s["TOPO"] < 1, "TOPO < 1",
                     rotulo_verdadeiro="r7", rotulo_falso="r4"),
        "r4":  Atribuicao("TAM_PILHA",
                          lambda s: _empilha(s, s["TOPO"]),
                          "empilha(TOPO)", "r5"),
        "r5":  Atribuicao("TOPO", lambda s: s["TOPO"] - 1,
                          "TOPO <- TOPO - 1", "r3"),
        "r7":  Teste(lambda s: s.get("TAM_PILHA", 0) == 0, "PILHA vazia",
                     rotulo_verdadeiro="r10", rotulo_falso="r8"),
        "r8":  Atribuicao("RES", lambda s: s["RES"] * _topo(s),
                          "RES <- RES * topo(PILHA)", "r9"),
        "r9":  Atribuicao("TAM_PILHA", lambda s: _desempilha(s),
                          "desempilha()", "r7"),
        "r10": Pare(),
    },
)


# ---------------------------------------------------------------------
#  Exportacao
# ---------------------------------------------------------------------

TODOS_PROGRAMAS = {
    "monolitico":             programa_monolitico,
    "iterativo":              programa_iterativo,
    "iterativo_decrescente":  programa_iterativo_decrescente,
    "recursivo":              programa_recursivo,
}
