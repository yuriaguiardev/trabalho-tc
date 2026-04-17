/*
 * ============================================================
 *  PROGRAMA ITERATIVO DECRESCENTE - Fatorial de n
 *  Trabalho de Teoria da Computabilidade
 * ============================================================
 *  Este programa computa a MESMA funcao que iterativo.c
 *  (f(n) = n!) mas percorre o indice em ordem DECRESCENTE
 *  (i = n, n-1, n-2, ..., 1).
 *
 *  Sua existencia justifica-se exclusivamente para ilustrar o
 *  conceito formal de NAO-EQUIVALENCIA FORTE: embora a FUNCAO
 *  COMPUTADA seja identica a iterativo.c para qualquer entrada
 *  valida, as CADEIAS de execucao produzidas pela Maquina de
 *  Tracos sao distintas (a ordem das multiplicacoes e' outra).
 *
 *  Portanto:
 *    - equivalencia funcional:  SIM
 *    - equivalencia forte    :  NAO
 * ============================================================
 */

#include <stdio.h>

int main(void) {
    int n;
    int i;
    int resultado;

    printf("Entre com n (inteiro >= 0): ");
    if (scanf("%d", &n) != 1) {
        printf("Entrada invalida.\n");
        return 1;
    }

    resultado = 1;
    i = n;

    while (i >= 1) {
        resultado = resultado * i;
        i = i - 1;
    }

    printf("Fatorial(%d) = %d\n", n, resultado);
    return 0;
}
