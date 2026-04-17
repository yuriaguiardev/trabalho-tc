/*
 * ============================================================
 *  PROGRAMA ITERATIVO - Fatorial de n
 *  Trabalho de Teoria da Computabilidade
 * ============================================================
 *  Caracteristica iterativa: uso explicito de estrutura de
 *  repeticao (while). Nao ha goto nem chamadas recursivas.
 *  O controle de fluxo e' determinado pela condicao do laco.
 *
 *  Funcao computada: f(n) = n! = 1 * 2 * 3 * ... * n, com f(0)=1
 *
 *  Observacao: este programa foi escrito em ordem CRESCENTE
 *  (i = 1, 2, 3, ..., n). Existe uma segunda versao iterativa
 *  em ordem DECRESCENTE (iterativo_decrescente.c) que e' usada
 *  para ilustrar o caso de NAO-EQUIVALENCIA forte entre dois
 *  programas que computam a mesma funcao.
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
    i = 1;

    while (i <= n) {
        resultado = resultado * i;
        i = i + 1;
    }

    printf("Fatorial(%d) = %d\n", n, resultado);
    return 0;
}
