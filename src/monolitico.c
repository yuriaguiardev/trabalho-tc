/*
 * ============================================================
 *  PROGRAMA MONOLITICO - Fatorial de n
 *  Trabalho de Teoria da Computabilidade
 * ============================================================
 *  Caracteristica monolitica: uso explicito de 'goto'.
 *  Nao ha sub-rotinas, laços estruturados, nem recursao.
 *  O fluxo de controle e' guiado exclusivamente por desvios
 *  incondicionais/condicionais entre rotulos.
 *
 *  Funcao computada: f(n) = n! = 1 * 2 * 3 * ... * n, com f(0)=1
 *
 *  Estrutura conceitual (programa monolitico normalizado):
 *    1: faca RES <- 1
 *    2: faca  I  <- 1
 *    3: se (I > N) entao va_para 7
 *    4: faca RES <- RES * I
 *    5: faca  I  <- I + 1
 *    6: va_para 3
 *    7: retorne RES
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

    /* Instrucao 1: inicializa RES */
    resultado = 1;

    /* Instrucao 2: inicializa I */
    i = 1;

inicio:
    /* Instrucao 3: teste de parada */
    if (i > n) goto fim;

    /* Instrucao 4: acumulacao */
    resultado = resultado * i;

    /* Instrucao 5: incremento */
    i = i + 1;

    /* Instrucao 6: desvio incondicional */
    goto inicio;

fim:
    /* Instrucao 7: retorno */
    printf("Fatorial(%d) = %d\n", n, resultado);
    return 0;
}
