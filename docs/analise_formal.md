# Análise formal — Trabalho de Teoria da Computabilidade

> Documento complementar que consolida a fundamentação teórica do trabalho,
> articulando a implementação com os conceitos da disciplina:
> programa, máquina, computação, função computada, equivalência forte
> e Máquina de Traços.

---

## 1. Definições fundamentais

### 1.1 Programa monolítico normalizado

Seguindo a abordagem de Diverio & Menezes, um **programa monolítico
normalizado** `P` é uma sequência finita de **instruções rotuladas**:

```
    P = ( r₁ : I₁,  r₂ : I₂,  ...,  rₖ : Iₖ )
```

onde cada `rᵢ` é um rótulo único e cada `Iᵢ` é uma das três formas:

- **Atribuição:** `faça VAR ← expressão` — avalia a expressão no estado
  corrente e atualiza uma variável; em seguida desvia para o próximo
  rótulo (implícito ou explícito).
- **Teste:** `se cond então vá_para r_v senão vá_para r_f` — desvia de
  acordo com o valor-verdade da condição.
- **Parada:** `pare` — encerra a execução do programa.

### 1.2 Estado e configuração

Dado um conjunto finito de variáveis `V = {v₁, v₂, ..., vₙ}`, um
**estado** é uma função `σ : V → ℤ`. Uma **configuração** (ou "instante
de execução") é o par:

```
    C = ⟨r, σ⟩
```

onde `r` é o rótulo corrente e `σ` é o estado corrente.

### 1.3 Relação de transição `⊢`

A execução de `P` induz uma relação de transição `⊢` entre configurações.
Por exemplo, se `r : faça X ← expr  ;  vá_para r'`, então:

```
    ⟨r, σ⟩  ⊢  ⟨r', σ[X := σ(expr)]⟩
```

### 1.4 Cadeia de traços (fita da MT)

A **Máquina de Traços** executa `P` a partir de uma configuração inicial
`C₀ = ⟨r_ini, σ₀⟩` e produz a cadeia:

```
    C₀  ⊢  C₁  ⊢  C₂  ⊢  ...  ⊢  C_f
```

onde `C_f` corresponde a um rótulo de `pare`. Essa cadeia é o **traço**
(ou **fita**) do programa para a entrada `σ₀`.

### 1.5 Função computada

O programa `P` **computa** a função `φ_P : ℤⁿ → ℤ` que, para cada entrada
`σ₀`, retorna o valor da variável de saída na configuração final `C_f`,
se a execução parar. Se não parar, a função não está definida naquele
ponto.

### 1.6 Equivalência forte

Dois programas `P` e `Q` são **fortemente equivalentes** se, e somente
se, para **toda entrada válida**, as cadeias de traços produzidas por
`P` e `Q` são **idênticas em estrutura** — isto é, possuem o mesmo
número de configurações, executam a mesma sequência de operações e
testes, e produzem o mesmo resultado final (a menos de renomeação
sistemática de rótulos e variáveis).

> **Importante:** equivalência forte ⟹ mesma função computada.
> A recíproca **não** vale: dois programas podem computar a mesma
> função sem serem fortemente equivalentes.

---

## 2. A função computada neste trabalho

Todos os quatro programas (P1, P2, P3, P4) implementam a função:

```
    f : ℕ → ℕ
    f(n) = n!
```

com `f(0) = f(1) = 1` e `f(n) = n · f(n−1)` para `n > 1`.

- Variáveis de entrada: `N`
- Variável de saída:    `RES`
- Domínio assumido:     `N ≥ 0` (natural)

---

## 3. Os programas normalizados

### 3.1 P1 — Monolítico crescente (espelho de `src/monolitico.c`)

```
    1 : faça RES ← 1                                       ; vá_para 2
    2 : faça I   ← 1                                       ; vá_para 3
    3 : se I > N então vá_para 7 senão vá_para 4
    4 : faça RES ← RES × I                                 ; vá_para 5
    5 : faça I   ← I + 1                                   ; vá_para 3
    7 : pare
```

### 3.2 P2 — Iterativo crescente normalizado (espelho de `src/iterativo.c`)

```
    i1 : faça RES ← 1                                      ; vá_para i2
    i2 : faça I   ← 1                                      ; vá_para i3
    i3 : se I > N então vá_para i7 senão vá_para i4
    i4 : faça RES ← RES × I                                ; vá_para i5
    i5 : faça I   ← I + 1                                  ; vá_para i3
    i7 : pare
```

### 3.3 P3 — Iterativo decrescente (espelho de `src/iterativo_decrescente.c`)

```
    d1 : faça RES ← 1                                      ; vá_para d2
    d2 : faça I   ← N                                      ; vá_para d3
    d3 : se I < 1 então vá_para d7 senão vá_para d4
    d4 : faça RES ← RES × I                                ; vá_para d5
    d5 : faça I   ← I − 1                                  ; vá_para d3
    d7 : pare
```

### 3.4 P4 — Recursivo normalizado (espelho de `src/recursivo.c`)

A recursão é eliminada pela técnica clássica de uma **pilha explícita**:

```
    --- Fase de DESCIDA (empilhamento) ---
    r1  : faça RES  ← 1                                    ; vá_para r2
    r2  : faça TOPO ← N                                    ; vá_para r3
    r3  : se TOPO < 1 então vá_para r7 senão vá_para r4
    r4  : faça empilha(TOPO)                               ; vá_para r5
    r5  : faça TOPO ← TOPO − 1                             ; vá_para r3

    --- Fase de SUBIDA (desempilhamento) ---
    r7  : se PILHA vazia então vá_para r10 senão vá_para r8
    r8  : faça RES ← RES × topo(PILHA)                     ; vá_para r9
    r9  : faça desempilha()                                ; vá_para r7
    r10 : pare
```

---

## 4. Demonstração da equivalência forte entre P1 e P2

**Proposição.** `P1` e `P2` são **fortemente equivalentes**.

**Justificativa.** Os programas P1 e P2 possuem exatamente a mesma
estrutura de instruções normalizadas: as únicas diferenças estão nos
nomes dos rótulos (`1, 2, 3, 4, 5, 7` em P1 vs. `i1, i2, i3, i4, i5, i7`
em P2) e na forma sintática em alto nível (`goto` em C monolítico vs.
`while` em C iterativo). Sob a renomeação bijetiva de rótulos

```
    φ :  i1 ↦ 1,  i2 ↦ 2,  i3 ↦ 3,  i4 ↦ 4,  i5 ↦ 5,  i7 ↦ 7
```

as cadeias de traços coincidem configuração a configuração.

**Verificação empírica pela MT.** O script `executar.py` testou
entradas `N ∈ {0, 1, 3, 5, 7}`. Em todas elas:

- Número de configurações em P1 = número de configurações em P2.
- Para todo `i`, `⟨r_i^{P1}, σ_i⟩ = ⟨φ(r_i^{P2}), σ_i⟩`.
- Resultado final idêntico.

A saída completa está em `maquina-tracos/saidas/analise_equivalencia.txt`.

---

## 5. Demonstração da NÃO-equivalência forte entre P2 e P3

**Proposição.** `P2` e `P3` computam a **mesma função**
(`φ_{P2} = φ_{P3} = f`, o fatorial), mas **não** são fortemente
equivalentes.

**Justificativa.**

1. *Mesma função computada.* Tanto P2 quanto P3 calculam
   `1 × 2 × 3 × ... × N`; a multiplicação é comutativa, logo
   `φ_{P2}(n) = φ_{P3}(n) = n!` para todo `n ≥ 0`.

2. *Traços distintos.* O primeiro ponto de divergência ocorre no **passo 2**
   das cadeias:

   - Em P2: `I ← 1` (estado: `I = 1`).
   - Em P3: `I ← N` (estado: `I = N`).

   A partir desse instante, os estados das variáveis `I` e `RES` diferem
   em toda configuração subsequente. Por exemplo, para `N = 4`:

   | Passo | P2 (I, RES)  | P3 (I, RES)  |
   |-------|--------------|--------------|
   | 2     | (1, 1)       | (4, 1)       |
   | 4     | (1, 1)       | (4, 4)       |
   | 7     | (2, 2)       | (3, 12)      |
   | 10    | (3, 6)       | (2, 24)      |
   | 13    | (4, 24)      | (1, 24)      |

   As **operações de multiplicação** que constroem `RES` ocorrem em
   ordem diferente:

   - P2: `1 × 1 = 1`, `1 × 2 = 2`, `2 × 3 = 6`, `6 × 4 = 24`.
   - P3: `1 × 4 = 4`, `4 × 3 = 12`, `12 × 2 = 24`, `24 × 1 = 24`.

   Embora o resultado final seja o mesmo, **a cadeia de configurações
   é outra**, o que viola o critério de equivalência forte.

**Conclusão.**
```
    φ_{P2} = φ_{P3}         (equivalência funcional)
    P2    ≢_forte   P3      (não-equivalência forte)
```

Saída detalhada: `maquina-tracos/saidas/analise_nao_equivalencia.txt`.

---

## 6. Sobre o programa recursivo (P4)

O programa `src/recursivo.c` não é, por si só, um programa monolítico
normalizado — ele usa a pilha de ativação **implícita** fornecida pela
linguagem C. Para submetê-lo à Máquina de Traços, foi produzida a
**normalização monolítica** `P4` com pilha **explícita** (descrita na
seção 3.4).

O traço de `P4` para `N = 4` tem 29 configurações, divididas em:

- 4 configurações de "cabeçalho" (inicialização de `RES` e `TOPO`),
- 12 configurações da fase de descida (testes + empilhamentos),
- 12 configurações da fase de subida (testes + multiplicações +
  desempilhamentos),
- 1 configuração de parada.

A variável `TAM_PILHA`, visível na fita, torna observável o crescimento
e a contração da pilha de ativações que caracterizam a recursão.

P4 **não é fortemente equivalente** a P1 nem a P2 (pois sua cadeia de
traços envolve duas fases adicionais de empilhamento/desempilhamento),
mas **compute a mesma função** (n!). É, portanto, um segundo exemplo
— estrutural — de não-equivalência forte entre programas funcionalmente
idênticos.

---

## 7. Conclusão

A utilização conjunta de:

1. **três estilos de programa** implementando a mesma função,
2. uma **Máquina de Traços** com saída em formato de fita,
3. um **par de programas com equivalência forte confirmada** (P1 × P2) e
4. um **par de programas funcionalmente iguais mas não fortemente
   equivalentes** (P2 × P3 — e também P2 × P4)

permitiu demonstrar, de forma concreta e fundamentada no formalismo da
disciplina, a distinção entre *equivalência funcional* e *equivalência
forte*, bem como o papel da MT como ferramenta formal para a segunda.
