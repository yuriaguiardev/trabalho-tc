#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=====================================================================
  EXECUCAO DA MAQUINA DE TRACOS SOBRE OS PROGRAMAS IMPLEMENTADOS
=====================================================================
  Este script:
    1) executa a MT sobre os 4 programas normalizados;
    2) imprime os tracos em formato de fita para n = 3, 4, 5;
    3) demonstra um caso de EQUIVALENCIA FORTE (P1 vs P2);
    4) demonstra um caso de NAO-EQUIVALENCIA FORTE (P2 vs P3),
       ambos com mesma funcao computada, mas tracos distintos;
    5) salva os resultados em arquivos de texto em ./saidas/
=====================================================================
"""

import os
import sys

# garante que o diretorio deste arquivo esta no sys.path
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

from mt import (MaquinaDeTracos, formatar_fita, formatar_tabela,
                sao_fortemente_equivalentes)
from programas import (programa_monolitico, programa_iterativo,
                       programa_iterativo_decrescente, programa_recursivo)


PASTA_SAIDAS = os.path.join(AQUI, "saidas")
os.makedirs(PASTA_SAIDAS, exist_ok=True)


def cabecalho(titulo, caractere="#", largura=78):
    print()
    print(caractere * largura)
    print(f"{caractere}  {titulo}")
    print(caractere * largura)


def salvar(nome_arquivo, conteudo):
    caminho = os.path.join(PASTA_SAIDAS, nome_arquivo)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"  [ok] salvo em saidas/{nome_arquivo}")


# =====================================================================
#  PARTE 1 - Tracos de cada programa para algumas entradas
# =====================================================================

def parte1_tracos_individuais():
    cabecalho("PARTE 1 - TRACOS INDIVIDUAIS (formato de fita)", "=")

    programas = [
        ("monolitico",            programa_monolitico),
        ("iterativo",             programa_iterativo),
        ("iterativo_decrescente", programa_iterativo_decrescente),
        ("recursivo",             programa_recursivo),
    ]
    entradas = [3, 4, 5]

    acumulador_global = []

    for nome_arq, prog in programas:
        buffer = []
        buffer.append("#" * 78)
        buffer.append(f"#  TRACOS DO PROGRAMA: {prog.nome}")
        buffer.append("#" * 78)

        for n in entradas:
            traco = MaquinaDeTracos.executar(prog, {"N": n})
            buffer.append("")
            buffer.append(formatar_fita(traco))
            buffer.append("")
            buffer.append(" Visao tabular:")
            buffer.append(formatar_tabela(traco))
            buffer.append("")

        conteudo = "\n".join(buffer)
        acumulador_global.append(conteudo)
        salvar(f"traco_{nome_arq}.txt", conteudo)

    # tambem salva um arquivo com tudo junto
    salvar("tracos_todos.txt", "\n\n".join(acumulador_global))


# =====================================================================
#  PARTE 2 - Equivalencia forte: P1 (monolitico) vs P2 (iterativo)
# =====================================================================

def parte2_equivalencia():
    cabecalho("PARTE 2 - EQUIVALENCIA FORTE: P1 (Monolitico) vs P2 (Iterativo)",
              "=")

    # Renomeacao de rotulos para alinhar P1 e P2 (diferem apenas em
    # nomes: "1" <-> "i1", "2" <-> "i2", ...).
    mapa_rotulos = {"i1": "1", "i2": "2", "i3": "3",
                    "i4": "4", "i5": "5", "i7": "7"}

    buffer = []
    buffer.append("#" * 78)
    buffer.append("#  ANALISE DE EQUIVALENCIA FORTE  -  P1 vs P2")
    buffer.append("#" * 78)
    buffer.append("""
HIPOTESE: P1 (monolitico com goto) e P2 (iterativo com while) sao
          FORTEMENTE EQUIVALENTES, porque a normalizacao monolitica
          de P2 produz exatamente a mesma sequencia de instrucoes
          rotuladas de P1 (a menos de renomeacao de rotulos).

METODO:   Para cada entrada N, executa-se a Maquina de Tracos sobre
          ambos os programas e compara-se configuracao a configuracao.
""")

    todos_iguais = True
    for n in [0, 1, 3, 5, 7]:
        t1 = MaquinaDeTracos.executar(programa_monolitico, {"N": n})
        t2 = MaquinaDeTracos.executar(programa_iterativo,  {"N": n})
        equiv, msg = sao_fortemente_equivalentes(
            t1, t2, mapa_rotulos=mapa_rotulos
        )
        buffer.append("-" * 78)
        buffer.append(f" Entrada N = {n}")
        buffer.append(f"   passos P1 = {len(t1.configuracoes)-1}   "
                      f"passos P2 = {len(t2.configuracoes)-1}")
        buffer.append(f"   resultado P1 = {t1.resultado}   "
                      f"resultado P2 = {t2.resultado}")
        buffer.append(f"   equivalentes ? {equiv}")
        buffer.append(f"   justificativa: {msg}")
        if not equiv:
            todos_iguais = False

    buffer.append("")
    buffer.append("=" * 78)
    if todos_iguais:
        buffer.append(" CONCLUSAO: P1 e P2 sao FORTEMENTE EQUIVALENTES.")
        buffer.append(" Os tracos coincidem passo a passo (apos renomeacao")
        buffer.append(" de rotulos) e produzem o mesmo resultado final.")
    else:
        buffer.append(" CONCLUSAO: os tracos divergem em alguma entrada.")
    buffer.append("=" * 78)

    # adiciona os dois tracos lado a lado para n = 4 (demonstracao visual)
    buffer.append("")
    buffer.append("## DEMONSTRACAO VISUAL - TRACOS LADO A LADO (N = 4)")
    buffer.append("")
    t1 = MaquinaDeTracos.executar(programa_monolitico, {"N": 4})
    t2 = MaquinaDeTracos.executar(programa_iterativo,  {"N": 4})
    buffer.append(">>> P1 (monolitico)")
    buffer.append(formatar_fita(t1))
    buffer.append("")
    buffer.append(">>> P2 (iterativo)")
    buffer.append(formatar_fita(t2))
    buffer.append("")
    buffer.append(" Observe: as duas fitas tem o mesmo numero de")
    buffer.append(" configuracoes, as mesmas acoes na mesma ordem e o")
    buffer.append(" mesmo resultado final. A unica diferenca sao os NOMES")
    buffer.append(" dos rotulos (1,2,3,... em P1  vs  i1,i2,i3,... em P2),")
    buffer.append(" o que e' irrelevante para equivalencia forte.")

    conteudo = "\n".join(buffer)
    print(conteudo)
    salvar("analise_equivalencia.txt", conteudo)


# =====================================================================
#  PARTE 3 - Nao-equivalencia: P2 (crescente) vs P3 (decrescente)
# =====================================================================

def parte3_nao_equivalencia():
    cabecalho("PARTE 3 - NAO-EQUIVALENCIA FORTE: P2 vs P3 "
              "(mesma funcao, tracos distintos)", "=")

    buffer = []
    buffer.append("#" * 78)
    buffer.append("#  ANALISE DE NAO-EQUIVALENCIA FORTE  -  P2 vs P3")
    buffer.append("#" * 78)
    buffer.append("""
HIPOTESE: P2 (iterativo crescente, i=1..N) e P3 (iterativo decrescente,
          i=N..1) computam a MESMA funcao (ambos retornam N!), mas
          NAO sao fortemente equivalentes, porque as sequencias de
          configuracoes geradas pela MT diferem:
            - em P2 a 1a multiplicacao e' RES <- RES * 1;
            - em P3 a 1a multiplicacao e' RES <- RES * N.
          A ordem das operacoes realizadas e', portanto, diferente.

METODO:   gera-se os dois tracos para a mesma entrada N e identifica-se
          o PRIMEIRO passo em que as configuracoes divergem.
""")

    for n in [3, 4, 5]:
        t2 = MaquinaDeTracos.executar(programa_iterativo,             {"N": n})
        t3 = MaquinaDeTracos.executar(programa_iterativo_decrescente, {"N": n})

        buffer.append("-" * 78)
        buffer.append(f" Entrada N = {n}")
        buffer.append(f"   funcao computada P2 = {t2.resultado}   "
                      f"funcao computada P3 = {t3.resultado}   "
                      f"(iguais? {t2.resultado == t3.resultado})")

        # localiza primeiro passo em que divergem (ignorando nome de rotulo)
        divergencia = None
        for i, (c2, c3) in enumerate(zip(t2.configuracoes, t3.configuracoes)):
            # comparamos somente o estado das variaveis "visiveis" (N, I, RES)
            vars_rel = ("N", "I", "RES")
            est2 = {k: c2.estado.get(k) for k in vars_rel if k in c2.estado}
            est3 = {k: c3.estado.get(k) for k in vars_rel if k in c3.estado}
            if est2 != est3:
                divergencia = (i, c2, c3, est2, est3)
                break
        if divergencia is None:
            buffer.append("   (tracos coincidem? nao deveria - verificar)")
        else:
            i, c2, c3, e2, e3 = divergencia
            buffer.append(f"   PRIMEIRA DIVERGENCIA no passo {i}:")
            buffer.append(f"     P2: {e2}   acao: {c2.acao}")
            buffer.append(f"     P3: {e3}   acao: {c3.acao}")

    buffer.append("")
    buffer.append("=" * 78)
    buffer.append(" CONCLUSAO: P2 e P3 NAO sao fortemente equivalentes.")
    buffer.append(" Embora computem a mesma funcao (n!), os tracos gerados")
    buffer.append(" pela MT diferem a partir do passo em que a variavel I")
    buffer.append(" e' inicializada de forma distinta (I<-1 em P2, I<-N em P3).")
    buffer.append(" Este e' um exemplo classico de que equivalencia funcional")
    buffer.append(" NAO IMPLICA equivalencia forte.")
    buffer.append("=" * 78)

    # Tracos lado a lado para N = 4
    buffer.append("")
    buffer.append("## DEMONSTRACAO VISUAL - TRACOS LADO A LADO (N = 4)")
    buffer.append("")
    t2 = MaquinaDeTracos.executar(programa_iterativo,             {"N": 4})
    t3 = MaquinaDeTracos.executar(programa_iterativo_decrescente, {"N": 4})
    buffer.append(">>> P2 (iterativo crescente)")
    buffer.append(formatar_fita(t2))
    buffer.append("")
    buffer.append(">>> P3 (iterativo decrescente)")
    buffer.append(formatar_fita(t3))
    buffer.append("")
    buffer.append(" Repare, em particular, no estado da variavel I ao longo")
    buffer.append(" da fita: em P2 ela assume a sequencia 1,2,3,4,5; em P3")
    buffer.append(" assume 4,3,2,1,0. As multiplicacoes que poduzem RES sao,")
    buffer.append(" respectivamente: (1,2,3,4)  vs  (4,3,2,1). Mesmo produto")
    buffer.append(" (24), ordem distinta -> nao sao fortemente equivalentes.")

    conteudo = "\n".join(buffer)
    print(conteudo)
    salvar("analise_nao_equivalencia.txt", conteudo)


# =====================================================================
#  PARTE 4 - Demonstracao da recursao (programa recursivo normalizado)
# =====================================================================

def parte4_recursivo():
    cabecalho("PARTE 4 - TRACO DO PROGRAMA RECURSIVO NORMALIZADO", "=")

    buffer = []
    buffer.append("#" * 78)
    buffer.append("#  TRACO DO PROGRAMA RECURSIVO (via pilha)")
    buffer.append("#" * 78)
    buffer.append("""
O programa recursivo em C (src/recursivo.c) usa a pilha de ativacao
implicita da linguagem. Para analisa-lo pela MT, ele foi NORMALIZADO
em um programa monolitico com pilha EXPLICITA. Observe, no traco:
  - Fase de DESCIDA: empilhamento de N, N-1, ..., 1 (rotulos r3-r6).
  - Fase de SUBIDA : desempilhamento com multiplicacoes (rotulos r7-r9).
A variavel TAM_PILHA torna visivel o crescimento e a contracao da
pilha de ativacao recursiva.
""")

    for n in [3, 4]:
        t = MaquinaDeTracos.executar(programa_recursivo, {"N": n})
        buffer.append(formatar_fita(t))
        buffer.append("")

    conteudo = "\n".join(buffer)
    print(conteudo)
    salvar("traco_recursivo_detalhado.txt", conteudo)


# =====================================================================

def main():
    parte1_tracos_individuais()
    parte2_equivalencia()
    parte3_nao_equivalencia()
    parte4_recursivo()

    print()
    print("=" * 78)
    print(" EXECUCAO CONCLUIDA - todos os arquivos foram gerados em saidas/ ")
    print("=" * 78)


if __name__ == "__main__":
    main()
