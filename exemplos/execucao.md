# Exemplos de execução

Este documento consolida exemplos concretos de execução dos quatro
programas, com entradas escolhidas pela equipe, ilustrando a **função
computada** e a **cadeia de traços**.

---

## 1. Função computada — tabela de equivalência funcional

Todos os quatro programas (P1, P2, P3, P4) produzem, para as mesmas
entradas, a mesma saída:

| N | P1 (monolítico) | P2 (iterativo) | P3 (iter. decr.) | P4 (recursivo) |
|---|-----------------|----------------|------------------|----------------|
| 0 | 1               | 1              | 1                | 1              |
| 1 | 1               | 1              | 1                | 1              |
| 2 | 2               | 2              | 2                | 2              |
| 3 | 6               | 6              | 6                | 6              |
| 4 | 24              | 24             | 24               | 24             |
| 5 | 120             | 120            | 120              | 120            |
| 6 | 720             | 720            | 720              | 720            |
| 7 | 5040            | 5040           | 5040             | 5040           |

Todos retornam `N!` — portanto são **equivalentes funcionalmente**.

---

## 2. Comandos executados no terminal

> Os comandos abaixo assumem que os pré-requisitos já estão instalados
> (ver Seção 5 do README principal). Os exemplos cobrem Windows,
> Linux e macOS.

### 2.1 Windows (PowerShell)

```powershell
# --- Compilação ---
cd trabalho-tc\src
gcc monolitico.c             -o monolitico
gcc iterativo.c              -o iterativo
gcc iterativo_decrescente.c  -o iterativo_decrescente
gcc recursivo.c              -o recursivo

# --- Execução interativa (digita-se N e pressiona-se Enter) ---
.\monolitico.exe
.\iterativo.exe
.\iterativo_decrescente.exe
.\recursivo.exe

# --- Execução com entrada automática ---
Write-Output 0 | .\monolitico.exe              # Fatorial(0) = 1
Write-Output 3 | .\monolitico.exe              # Fatorial(3) = 6
Write-Output 5 | .\monolitico.exe              # Fatorial(5) = 120
Write-Output 7 | .\monolitico.exe              # Fatorial(7) = 5040

Write-Output 5 | .\iterativo.exe               # Fatorial(5) = 120
Write-Output 5 | .\iterativo_decrescente.exe   # Fatorial(5) = 120
Write-Output 5 | .\recursivo.exe               # Fatorial(5) = 120

# --- Máquina de Traços ---
cd ..\maquina-tracos
python executar.py

# --- Abrir as saídas ---
type saidas\traco_monolitico.txt
type saidas\analise_equivalencia.txt
type saidas\analise_nao_equivalencia.txt
```

### 2.2 Linux / macOS (bash/zsh)

```bash
# --- Compilação ---
cd trabalho-tc/src
gcc monolitico.c             -o monolitico
gcc iterativo.c              -o iterativo
gcc iterativo_decrescente.c  -o iterativo_decrescente
gcc recursivo.c              -o recursivo

# --- Execução interativa ---
./monolitico
./iterativo
./iterativo_decrescente
./recursivo

# --- Execução com entrada automática ---
echo 0 | ./monolitico              # Fatorial(0) = 1
echo 3 | ./monolitico              # Fatorial(3) = 6
echo 5 | ./monolitico              # Fatorial(5) = 120
echo 7 | ./monolitico              # Fatorial(7) = 5040

echo 5 | ./iterativo               # Fatorial(5) = 120
echo 5 | ./iterativo_decrescente   # Fatorial(5) = 120
echo 5 | ./recursivo               # Fatorial(5) = 120

# --- Máquina de Traços ---
cd ../maquina-tracos
python3 executar.py

# --- Abrir as saídas ---
cat saidas/traco_monolitico.txt
cat saidas/analise_equivalencia.txt
cat saidas/analise_nao_equivalencia.txt
```

### 2.3 Bônus Assembly (monolítico em x86-64)

> **Atenção ao formato de objeto:** `-f win64` no Windows, `-f elf64`
> no Linux, `-f macho64` no macOS.

**Windows (PowerShell):**
```powershell
cd trabalho-tc\src
nasm -f win64 monolitico.asm -o monolitico_asm.o
gcc monolitico_asm.o -o monolitico_asm
Write-Output 5 | .\monolitico_asm.exe          # Fatorial(5) = 120
```

**Linux:**
```bash
cd trabalho-tc/src
nasm -f elf64 monolitico.asm -o monolitico_asm.o
gcc  -no-pie  monolitico_asm.o -o monolitico_asm
echo 5 | ./monolitico_asm                       # Fatorial(5) = 120
```

**macOS (Intel):**
```bash
cd trabalho-tc/src
nasm -f macho64 monolitico.asm -o monolitico_asm.o
gcc monolitico_asm.o -o monolitico_asm
./monolitico_asm
```

---

## 3. Saída esperada dos programas em C

Para `N = 5`, todos os quatro programas imprimem (após o prompt):

```
Entre com n (inteiro >= 0): Fatorial(5) = 120
```

Para `N = 0` (caso-base do fatorial):

```
Entre com n (inteiro >= 0): Fatorial(0) = 1
```

Para `N = 7`:

```
Entre com n (inteiro >= 0): Fatorial(7) = 5040
```

A validação cruzada é trivial: os quatro binários produzem exatamente a
mesma saída para cada entrada — o que é suficiente para demonstrar
**equivalência funcional**.

---

## 4. Traço do programa monolítico (P1) para N = 3

*(extraído de `maquina-tracos/saidas/traco_monolitico.txt`)*

```
⟨ 1, [N=3]⟩
|- ⟨ 2, [N=3, RES=1]⟩                  RES ← 1
|- ⟨ 3, [N=3, RES=1, I=1]⟩             I ← 1
|- ⟨ 4, [N=3, RES=1, I=1]⟩             teste: I > N → F
|- ⟨ 5, [N=3, RES=1, I=1]⟩             RES ← RES × I   [RES=1]
|- ⟨ 3, [N=3, RES=1, I=2]⟩             I ← I + 1       [I=2]
|- ⟨ 4, [N=3, RES=1, I=2]⟩             teste: I > N → F
|- ⟨ 5, [N=3, RES=2, I=2]⟩             RES ← RES × I   [RES=2]
|- ⟨ 3, [N=3, RES=2, I=3]⟩             I ← I + 1       [I=3]
|- ⟨ 4, [N=3, RES=2, I=3]⟩             teste: I > N → F
|- ⟨ 5, [N=3, RES=6, I=3]⟩             RES ← RES × I   [RES=6]
|- ⟨ 3, [N=3, RES=6, I=4]⟩             I ← I + 1       [I=4]
|- ⟨ 7, [N=3, RES=6, I=4]⟩             teste: I > N → V
|- ⟨ 7, [N=3, RES=6, I=4]⟩             pare

Resultado: 6     Passos: 13
```

---

## 5. Os oito arquivos de saída da MT

Após executar `python executar.py` (Windows) ou `python3 executar.py`
(Linux/macOS), a pasta `maquina-tracos/saidas/` contém:

1. `traco_monolitico.txt`              — fita e tabela para P1 com N ∈ {3,4,5}
2. `traco_iterativo.txt`               — fita e tabela para P2 com N ∈ {3,4,5}
3. `traco_iterativo_decrescente.txt`   — fita e tabela para P3 com N ∈ {3,4,5}
4. `traco_recursivo.txt`               — fita e tabela para P4 com N ∈ {3,4,5}
5. `tracos_todos.txt`                  — concatenação de todos os traços
6. `analise_equivalencia.txt`          — demonstração P1 ≡ P2 (equivalência forte)
7. `analise_nao_equivalencia.txt`      — demonstração P2 ≢ P3 (não-equivalência)
8. `traco_recursivo_detalhado.txt`     — traço completo de P4 com comentários

### 5.1 O que procurar em cada arquivo

| Arquivo | O que demonstrar ao professor |
|---------|-------------------------------|
| `traco_monolitico.txt` | A fita: cadeia C₀ ⊢ C₁ ⊢ ... ⊢ C_f com cada configuração ⟨rótulo, estado⟩ |
| `analise_equivalencia.txt` | As cinco linhas `equivalentes ? True` (para N = 0, 1, 3, 5, 7) |
| `analise_nao_equivalencia.txt` | A linha **`PRIMEIRA DIVERGENCIA no passo 2`** — ponto central da análise |
| `traco_recursivo_detalhado.txt` | A variável `TAM_PILHA` crescendo (fase de descida) e decrescendo (subida) |

---

## 6. Operações e testes relevantes para a análise formal

| Tipo | Descrição                 | Onde aparece |
|------|---------------------------|--------------|
| **Atribuição** | `RES ← 1`            | inicialização do acumulador |
| **Atribuição** | `I ← 1` (ou `N`)     | inicialização do índice |
| **Atribuição** | `RES ← RES × I`      | passo do acumulador |
| **Atribuição** | `I ← I ± 1`          | incremento/decremento |
| **Teste**      | `I > N` (ou `I < 1`) | condição de parada do laço |
| **Parada**     | `pare`               | fim da execução |

São estas operações e testes que compõem a **sequência observada** na
fita da Máquina de Traços e que fundamentam a comparação de
equivalência forte.

---

## 7. Resumo — o que cada execução prova

| Execução | O que demonstra | Conceito ilustrado |
|----------|-----------------|--------------------|
| Todos os 4 programas com mesma entrada produzindo mesma saída | P1, P2, P3, P4 computam a mesma função | **Equivalência funcional** |
| `cat saidas/analise_equivalencia.txt` → `equivalentes ? True` | Os traços de P1 e P2 coincidem | **Equivalência forte** (P1 ≡ P2) |
| `cat saidas/analise_nao_equivalencia.txt` → divergência no passo 2 | Os traços de P2 e P3 divergem apesar de P2(n)=P3(n)=n! | **Não-equivalência forte** (P2 ≢ P3) |
| `traco_recursivo_detalhado.txt` | Fase de descida + fase de subida com pilha explícita | Normalização de recursão em programa monolítico |
| `monolitico.asm` executando | Lógica monolítica em rótulos/desvios de baixo nível | Programa monolítico em Assembly (bônus) |
