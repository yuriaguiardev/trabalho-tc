; ============================================================
;  PROGRAMA MONOLITICO EM ASSEMBLY - Fatorial de n
;  Trabalho de Teoria da Computabilidade (pontuacao extra)
; ============================================================
;  Arquitetura: x86-64 Linux, sintaxe NASM, chamadas libc.
;
;  Equivalencia conceitual com o programa monolitico em C:
;  a logica monolitica fica AINDA MAIS evidente em Assembly,
;  pois o codigo e' naturalmente formado por rotulos e desvios
;  (jmp/je/jg). Nao existem lacos estruturados nem chamadas
;  recursivas nesta implementacao - somente desvios diretos
;  entre rotulos, o que e' a essencia de um programa monolitico.
;
;  Registradores usados:
;     r12  -> N         (entrada)
;     r13  -> I         (contador, inicia em 1)
;     r14  -> RESULTADO (acumulador, inicia em 1)
;
;  Mapeamento para o pseudocodigo monolitico normalizado:
;     1: RES <- 1                     ; mov r14, 1
;     2: I   <- 1                     ; mov r13, 1
;     3: se I > N entao va_para 7     ; cmp r13, r12 / jg fim
;     4: RES <- RES * I               ; imul r14, r13
;     5: I   <- I + 1                 ; inc r13
;     6: va_para 3                    ; jmp inicio
;     7: retorne RES                  ; printf e exit
;
;  Compilacao:
;     nasm -f elf64 monolitico.asm -o monolitico.o
;     gcc -no-pie monolitico.o -o monolitico_asm
;  Execucao:
;     ./monolitico_asm
; ============================================================

        global  main
        extern  printf
        extern  scanf

        section .data
msg_in:  db "Entre com n (inteiro >= 0): ", 0
fmt_in:  db "%d", 0
msg_out: db "Fatorial(%d) = %ld", 10, 0

        section .bss
n_val:   resq 1

        section .text
main:
        push    rbp
        mov     rbp, rsp
        sub     rsp, 16                 ; alinhamento de pilha

        ; ---- prompt ----
        lea     rdi, [rel msg_in]
        xor     eax, eax
        call    printf

        ; ---- scanf("%d", &n) ----
        lea     rdi, [rel fmt_in]
        lea     rsi, [rel n_val]
        xor     eax, eax
        call    scanf

        ; ---- carrega N em r12 ----
        mov     eax, dword [rel n_val]
        movsxd  r12, eax                ; r12 = N

        ; Instrucao 1: RES <- 1
        mov     r14, 1

        ; Instrucao 2: I <- 1
        mov     r13, 1

inicio:                                 ; rotulo 'inicio' (instrucao 3)
        ; Instrucao 3: se I > N entao va_para fim
        cmp     r13, r12
        jg      fim

        ; Instrucao 4: RES <- RES * I
        imul    r14, r13

        ; Instrucao 5: I <- I + 1
        inc     r13

        ; Instrucao 6: va_para inicio
        jmp     inicio

fim:                                    ; rotulo 'fim' (instrucao 7)
        ; Instrucao 7: imprime RES e retorna
        lea     rdi, [rel msg_out]
        mov     esi, r12d               ; primeiro %d -> N
        mov     rdx, r14                ; segundo %ld -> RES
        xor     eax, eax
        call    printf

        xor     eax, eax                ; return 0
        leave
        ret
