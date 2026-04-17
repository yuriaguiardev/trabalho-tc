/*
 * ============================================================
 *  PROGRAMA RECURSIVO - Fatorial de n
 *  Trabalho de Teoria da Computabilidade
 * ============================================================
 *  Caracteristica recursiva: a funcao fatorial() invoca a si
 *  mesma ate atingir a CONDICAO-BASE de parada (n <= 1).
 *  Nao ha goto nem laco explicito; o fluxo e' determinado pelo
 *  empilhamento e desempilhamento de chamadas.
 *
 *  Funcao computada:
 *     f(0) = 1                            (caso base)
 *     f(1) = 1                            (caso base)
 *     f(n) = n * f(n-1) , para n > 1      (passo recursivo)
 * ============================================================
 */

#include <stdio.h>

int fatorial(int n) {
    /* condicao-base de parada */
    if (n <= 1) {
        return 1;
    }
    /* passo recursivo */
    return n * fatorial(n - 1);
}

int main(void) {
    int n;

    printf("Entre com n (inteiro >= 0): ");
    if (scanf("%d", &n) != 1) {
        printf("Entrada invalida.\n");
        return 1;
    }

    printf("Fatorial(%d) = %d\n", n, fatorial(n));
    return 0;
}
