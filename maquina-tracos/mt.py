#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=====================================================================
  MAQUINA DE TRACOS (MT) - Teoria da Computabilidade
=====================================================================
  Implementacao do metodo da Maquina de Tracos conforme apresentado
  na disciplina (livro de Tiaraju A. Diverio e Paulo F. B. Menezes,
  "Teoria da Computacao - Maquinas Universais e Computabilidade").

  CONCEITO (resumo formal):
  -------------------------
  Um programa monolitico normalizado P e' uma sequencia finita de
  instrucoes rotuladas (r : I), onde cada I e':
      - uma atribuicao     "faca X <- expr"
      - um teste           "se cond entao va_para r1 senao va_para r2"
      - uma parada         "pare"
  A Maquina de Tracos simula a execucao de P sobre uma entrada,
  gerando uma CADEIA (ou TRACO) de configuracoes:

      C0 |- C1 |- C2 |- ... |- Cf

  onde cada Ci = <rotulo_atual, estado_das_variaveis>.

  EQUIVALENCIA FORTE:
  -------------------
  Dois programas P e Q sao FORTEMENTE EQUIVALENTES sse, para TODA
  entrada valida, produzem a MESMA cadeia de tracos (a menos de
  renomeacao de rotulos e variaveis, i.e., a mesma SEQUENCIA de
  operacoes e testes realizados).

  Observacao importante: equivalencia forte implica equivalencia
  funcional (mesma funcao computada), mas a reciproca NAO vale.
  Dois programas podem computar a MESMA funcao e ainda assim NAO
  serem fortemente equivalentes (vide exemplo de nao-equivalencia
  neste trabalho: fatorial crescente vs. fatorial decrescente).
=====================================================================
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------
#  Tipos de instrucao
# ---------------------------------------------------------------------

@dataclass
class Atribuicao:
    """faca  VAR <- expr   -- expr e' uma funcao lambda(estado) -> valor"""
    var: str
    expr: Callable[[Dict[str, int]], int]
    descricao: str          # forma textual para exibicao, ex: "RES <- RES * I"
    proximo: str            # proximo rotulo a executar

@dataclass
class Teste:
    """se cond entao va_para r_v senao va_para r_f"""
    cond: Callable[[Dict[str, int]], bool]
    descricao: str          # forma textual, ex: "I > N"
    rotulo_verdadeiro: str
    rotulo_falso: str

@dataclass
class Pare:
    """pare -- encerra a execucao"""
    descricao: str = "pare"


Instrucao = object  # Atribuicao | Teste | Pare


# ---------------------------------------------------------------------
#  Programa monolitico normalizado
# ---------------------------------------------------------------------

@dataclass
class Programa:
    """
    Programa monolitico na forma normalizada exigida pela MT.
    instrucoes: dicionario rotulo -> Instrucao
    inicio:     rotulo da primeira instrucao
    entradas:   lista de nomes de variaveis de entrada
    saida:      nome da variavel de saida
    """
    nome: str
    instrucoes: Dict[str, Instrucao]
    inicio: str
    entradas: List[str]
    saida: str


# ---------------------------------------------------------------------
#  Configuracao e traco
# ---------------------------------------------------------------------

@dataclass
class Configuracao:
    """Um 'instante' da execucao: <rotulo, estado>."""
    passo: int
    rotulo: str
    estado: Dict[str, int]
    acao: str = ""          # descricao da instrucao acabada de executar
    ramo: str = ""          # para testes: "V" ou "F"


@dataclass
class Traco:
    """Cadeia de configuracoes produzida pela MT para uma entrada."""
    programa: str
    entrada: Dict[str, int]
    configuracoes: List[Configuracao] = field(default_factory=list)
    resultado: Optional[int] = None


# ---------------------------------------------------------------------
#  Nucleo da Maquina de Tracos
# ---------------------------------------------------------------------

class MaquinaDeTracos:
    """
    Executa um programa monolitico normalizado, instrucao por
    instrucao, produzindo a cadeia de configuracoes (traco).
    """

    LIMITE_PASSOS = 10_000       # salvaguarda contra lacos infinitos

    @staticmethod
    def executar(prog: Programa, entrada: Dict[str, int]) -> Traco:
        estado: Dict[str, int] = dict(entrada)
        traco = Traco(programa=prog.nome, entrada=dict(entrada))

        rotulo_atual = prog.inicio
        passo = 0

        # configuracao inicial
        traco.configuracoes.append(
            Configuracao(passo=passo, rotulo=rotulo_atual,
                         estado=dict(estado), acao="(inicio)")
        )

        while True:
            if passo > MaquinaDeTracos.LIMITE_PASSOS:
                raise RuntimeError("Limite de passos excedido (possivel laco infinito).")

            instr = prog.instrucoes[rotulo_atual]
            passo += 1

            if isinstance(instr, Atribuicao):
                valor = instr.expr(estado)
                estado[instr.var] = valor
                acao = f"{instr.descricao}   [{instr.var}={valor}]"
                rotulo_atual = instr.proximo
                traco.configuracoes.append(
                    Configuracao(passo=passo, rotulo=rotulo_atual,
                                 estado=dict(estado), acao=acao)
                )

            elif isinstance(instr, Teste):
                resultado_teste = instr.cond(estado)
                ramo = "V" if resultado_teste else "F"
                acao = f"teste: {instr.descricao}  ->  {ramo}"
                rotulo_atual = (instr.rotulo_verdadeiro if resultado_teste
                                else instr.rotulo_falso)
                traco.configuracoes.append(
                    Configuracao(passo=passo, rotulo=rotulo_atual,
                                 estado=dict(estado), acao=acao, ramo=ramo)
                )

            elif isinstance(instr, Pare):
                traco.configuracoes.append(
                    Configuracao(passo=passo, rotulo=rotulo_atual,
                                 estado=dict(estado), acao="pare")
                )
                traco.resultado = estado.get(prog.saida)
                return traco

            else:
                raise RuntimeError(f"Instrucao desconhecida em {rotulo_atual}")


# ---------------------------------------------------------------------
#  Formatacao da saida em formato de FITA
# ---------------------------------------------------------------------

def formatar_fita(traco: Traco, largura: int = 78) -> str:
    """
    Produz a cadeia de tracos no formato de FITA, como visto em sala:

       <r1, sigma1> |- <r2, sigma2> |- <r3, sigma3> |- ...

    Cada celula exibe (rotulo, estado) e a operacao correspondente
    fica anotada no lado direito.
    """
    linhas: List[str] = []
    linhas.append("=" * largura)
    linhas.append(f" TRACO DO PROGRAMA: {traco.programa}")
    linhas.append(f" Entrada: {traco.entrada}")
    linhas.append("=" * largura)
    linhas.append("")
    linhas.append(" Fita de configuracoes  <rotulo, estado>  |-  proxima")
    linhas.append("-" * largura)

    for i, cfg in enumerate(traco.configuracoes):
        sep = "  |-  " if i > 0 else "       "
        est = ", ".join(f"{k}={v}" for k, v in cfg.estado.items()
                        if not k.startswith("_"))
        linhas.append(f" {sep}<{cfg.rotulo:>6}, [{est}]>")
        if cfg.acao and cfg.acao != "(inicio)":
            linhas.append(f"         acao: {cfg.acao}")

    linhas.append("-" * largura)
    linhas.append(f" Resultado final: {traco.resultado}")
    linhas.append(f" Total de passos : {len(traco.configuracoes) - 1}")
    linhas.append("=" * largura)
    return "\n".join(linhas)


def formatar_tabela(traco: Traco) -> str:
    """
    Versao tabular compacta do traco, util para comparacoes visuais.
    """
    todas_vars = []
    for cfg in traco.configuracoes:
        for k in cfg.estado:
            # ignora variaveis "internas" (prefixo _) na visualizacao
            if k.startswith("_"):
                continue
            if k not in todas_vars:
                todas_vars.append(k)

    cab = f"| {'#':>3} | {'rotulo':<8} |"
    for v in todas_vars:
        cab += f" {v:>5} |"
    cab += f" {'acao':<40} |"

    sep = "-" * len(cab)
    linhas = [sep, cab, sep]
    for cfg in traco.configuracoes:
        linha = f"| {cfg.passo:>3} | {cfg.rotulo:<8} |"
        for v in todas_vars:
            valor = cfg.estado.get(v, "")
            linha += f" {str(valor):>5} |"
        linha += f" {cfg.acao[:40]:<40} |"
        linhas.append(linha)
    linhas.append(sep)
    return "\n".join(linhas)


# ---------------------------------------------------------------------
#  Comparacao de tracos para equivalencia forte
# ---------------------------------------------------------------------

def assinatura_configuracao(cfg: Configuracao,
                            mapa_rotulos: Optional[Dict[str, str]] = None,
                            mapa_vars: Optional[Dict[str, str]] = None
                            ) -> Tuple:
    """
    Constroi uma assinatura canonica de uma configuracao, aplicando
    opcionalmente renomeacoes de rotulos e variaveis. Isso permite
    comparar dois programas que usam nomes distintos mas tem a mesma
    estrutura de execucao.
    """
    r = mapa_rotulos.get(cfg.rotulo, cfg.rotulo) if mapa_rotulos else cfg.rotulo
    if mapa_vars:
        est = tuple(sorted(
            (mapa_vars.get(k, k), v) for k, v in cfg.estado.items()
        ))
    else:
        est = tuple(sorted(cfg.estado.items()))
    return (r, est, cfg.acao, cfg.ramo)


def sao_fortemente_equivalentes(t1: Traco, t2: Traco,
                                mapa_rotulos: Optional[Dict[str, str]] = None,
                                mapa_vars: Optional[Dict[str, str]] = None
                                ) -> Tuple[bool, str]:
    """
    Verifica equivalencia forte entre dois tracos: mesma sequencia de
    operacoes/testes e mesmo resultado final. Permite renomeacao.
    Retorna (equivalentes?, explicacao).
    """
    if len(t1.configuracoes) != len(t2.configuracoes):
        return False, (f"Tamanhos diferentes: {len(t1.configuracoes)} vs "
                       f"{len(t2.configuracoes)} configuracoes.")

    for i, (c1, c2) in enumerate(zip(t1.configuracoes, t2.configuracoes)):
        # O mapa_rotulos traduz nomes de T2 para T1.
        # Ex.: {"i1":"1"} diz "i1 de P2 equivale a 1 de P1".
        a1 = assinatura_configuracao(c1)
        a2 = assinatura_configuracao(c2, mapa_rotulos, mapa_vars)
        # comparamos a *estrutura* (ignorando a descricao textual exata,
        # que pode variar por detalhes de formatacao)
        if a1[0] != a2[0] or a1[1] != a2[1] or a1[3] != a2[3]:
            return False, (f"Divergencia no passo {i}:\n"
                           f"   P1: <{c1.rotulo}, {c1.estado}>  acao={c1.acao}\n"
                           f"   P2: <{c2.rotulo}, {c2.estado}>  acao={c2.acao}")

    if t1.resultado != t2.resultado:
        return False, f"Resultado final difere: {t1.resultado} vs {t2.resultado}."

    return True, "Tracos identicos em todos os passos e mesmo resultado final."


# ---------------------------------------------------------------------
#  FIM do modulo nucleo
# ---------------------------------------------------------------------
