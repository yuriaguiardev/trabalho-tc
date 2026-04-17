# Trabalho de Teoria da Computabilidade

## Programas Monolíticos, Iterativos, Recursivos e Máquina de Traços

> **Disciplina:** Teoria da Computabilidade
> **Professor:** Daniel Leal Souza
> **Turma:** CC5NA
> **Data de entrega:** _(15/04/2026 ou 17/04/2026 — conforme turma)_

---

## 1. Integrantes da equipe

Nomes: Yuri Aguiar, Pedro Paulo e Joao Rath

---

## 2. Função computada

O trabalho implementa, nos três estilos de programa exigidos, a função
**fatorial de um número natural**:

$$f(n) = n! = \begin{cases} 1, & \text{se } n \leq 1 \\ n \cdot (n-1)!, & \text{se } n > 1 \end{cases}$$

- **Entrada:** inteiro `N ≥ 0`
- **Saída:** inteiro `RES = N!`
- **Exemplos de execução:**

| N | Saída esperada |
|---|---------------|
| 0 | 1             |
| 1 | 1             |
| 3 | 6             |
| 4 | 24            |
| 5 | 120           |
| 7 | 5040          |

A escolha do fatorial é justificada por três razões didáticas:

1. **Simples**: uma função primitiva recursiva elementar, cuja implementação
   monolítica é quase trivial — isso permite que o foco do trabalho seja a
   **Máquina de Traços**, e não a lógica do algoritmo.
2. **Três estilos naturais**: o fatorial admite implementação monolítica
   com `goto`, iterativa com laço e recursiva com caso-base — sem precisar de
   adaptações artificiais.
3. **Não-equivalência clara**: o fatorial pode ser calculado em **ordem
   crescente** (`1 × 2 × 3 × ... × n`) ou **decrescente** (`n × (n−1) × ... × 1`),
   produzindo traços diferentes apesar do mesmo resultado — exemplo canônico
   de duas implementações *funcionalmente iguais* mas *não fortemente
   equivalentes*.

---

## 3. Linguagens utilizadas

| Componente | Linguagem | Observação |
|------------|-----------|------------|
| Programa monolítico | **C** (com `goto`) | lógica monolítica explícita |
| Programa iterativo | **C** (com `while`) | laço estruturado |
| Programa iterativo decrescente | **C** (com `while`) | usado p/ não-equivalência |
| Programa recursivo | **C** (com chamada recursiva) | caso-base `n ≤ 1` |
| **Bônus: monolítico em Assembly** | **x86-64 NASM** | pontuação extra (+0,5) |
| Máquina de Traços | **Python 3** | implementação + formatação em fita |

---

## 4. Organização do repositório

```
.
├── README.md                        <- este arquivo
├── src/
│   ├── monolitico.c                 <- programa monolítico (goto)
│   ├── iterativo.c                  <- programa iterativo (while crescente)
│   ├── iterativo_decrescente.c      <- usado p/ não-equivalência
│   ├── recursivo.c                  <- programa recursivo
│   └── monolitico.asm               <- BÔNUS: monolítico em Assembly x86-64
├── maquina-tracos/
│   ├── mt.py                        <- núcleo da MT (formalismo)
│   ├── programas.py                 <- programas normalizados (P1, P2, P3, P4)
│   ├── executar.py                  <- script que gera todos os traços
│   └── saidas/                      <- traços em formato de fita (.txt)
│       ├── traco_monolitico.txt
│       ├── traco_iterativo.txt
│       ├── traco_iterativo_decrescente.txt
│       ├── traco_recursivo.txt
│       ├── traco_recursivo_detalhado.txt
│       ├── tracos_todos.txt
│       ├── analise_equivalencia.txt
│       └── analise_nao_equivalencia.txt
├── docs/
│   ├── analise_formal.md            <- documento teórico-formal
│   ├── uso_de_ia.md                 <- registro do uso de IA
│   └── apresentacao.pptx            <- apresentação em sala
└── exemplos/
    └── execucao.md                  <- log de execuções comentadas
```

---

## 5. Pré-requisitos

Antes de compilar e executar, é preciso ter instalado:

- **`gcc`** — compilador C
- **`python`** (Python 3.9 ou superior) — sem dependências externas
- **`nasm`** (opcional, só para o bônus Assembly)

### 5.1 Instalação no Windows

Recomenda-se o **MSYS2**, que fornece `gcc` e `nasm` de forma nativa.

1. Baixe o instalador em https://www.msys2.org e instale aceitando os padrões.
2. Abra o terminal **"MSYS2 UCRT64"** que aparece no menu Iniciar e execute:
   ```bash
   pacman -S --noconfirm mingw-w64-ucrt-x86_64-gcc mingw-w64-ucrt-x86_64-nasm
   ```
3. Adicione `C:\msys64\ucrt64\bin` ao **PATH** do Windows:
   - tecla **Windows** → digite "variáveis de ambiente" → abrir "Editar as variáveis de ambiente do sistema"
   - botão **Variáveis de ambiente...** → em "Variáveis do usuário", selecionar `Path` → **Editar** → **Novo**
   - colar `C:\msys64\ucrt64\bin` → OK em tudo.
4. O Python para Windows está disponível em https://www.python.org/downloads/ (na instalação, marque a opção **"Add Python to PATH"**).
5. **Feche e reabra o PowerShell** (ou Prompt de Comando) e verifique:
   ```powershell
   gcc --version
   nasm --version
   python --version
   ```

### 5.2 Instalação no Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install -y gcc nasm python3
```

### 5.3 Instalação no macOS

```bash
# gcc/clang costumam estar disponíveis via Xcode Command Line Tools
xcode-select --install

# nasm via Homebrew
brew install nasm
```

Python 3 já acompanha o macOS moderno.

---

## 6. Instruções de compilação e execução

### 6.1 Windows (PowerShell)

```powershell
# compilação
cd trabalho-tc\src
gcc monolitico.c             -o monolitico
gcc iterativo.c              -o iterativo
gcc iterativo_decrescente.c  -o iterativo_decrescente
gcc recursivo.c              -o recursivo

# execução interativa (digite o valor de N e pressione Enter)
.\monolitico.exe
.\iterativo.exe
.\iterativo_decrescente.exe
.\recursivo.exe

# execução com entrada automática (útil para a demo)
Write-Output 5 | .\monolitico.exe              # Fatorial(5) = 120
Write-Output 5 | .\iterativo.exe               # Fatorial(5) = 120
Write-Output 5 | .\iterativo_decrescente.exe   # Fatorial(5) = 120
Write-Output 5 | .\recursivo.exe               # Fatorial(5) = 120
Write-Output 7 | .\recursivo.exe               # Fatorial(7) = 5040
Write-Output 0 | .\monolitico.exe              # Fatorial(0) = 1
```

### 6.2 Linux / macOS (bash / zsh)

```bash
# compilação
cd trabalho-tc/src
gcc monolitico.c             -o monolitico
gcc iterativo.c              -o iterativo
gcc iterativo_decrescente.c  -o iterativo_decrescente
gcc recursivo.c              -o recursivo

# execução interativa
./monolitico
./iterativo
./iterativo_decrescente
./recursivo

# execução com entrada automática
echo 5 | ./monolitico              # Fatorial(5) = 120
echo 5 | ./iterativo               # Fatorial(5) = 120
echo 5 | ./iterativo_decrescente   # Fatorial(5) = 120
echo 5 | ./recursivo               # Fatorial(5) = 120
echo 7 | ./recursivo               # Fatorial(7) = 5040
echo 0 | ./monolitico              # Fatorial(0) = 1
```

### 6.3 Bônus — monolítico em Assembly

> ⚠️ **Atenção:** o formato de objeto muda entre Windows e Linux.
> Use `-f win64` no Windows e `-f elf64` no Linux.

**Windows (PowerShell):**
```powershell
cd trabalho-tc\src
nasm -f win64 monolitico.asm -o monolitico_asm.o
gcc monolitico_asm.o -o monolitico_asm
.\monolitico_asm.exe
Write-Output 5 | .\monolitico_asm.exe     # Fatorial(5) = 120
```

**Linux:**
```bash
cd trabalho-tc/src
nasm -f elf64 monolitico.asm -o monolitico_asm.o
gcc  -no-pie  monolitico_asm.o -o monolitico_asm
./monolitico_asm
echo 5 | ./monolitico_asm                  # Fatorial(5) = 120
```

**macOS (Intel):**
```bash
cd trabalho-tc/src
nasm -f macho64 monolitico.asm -o monolitico_asm.o
gcc monolitico_asm.o -o monolitico_asm
./monolitico_asm
```

### 6.4 Máquina de Traços

Pré-requisito: Python 3.9+ (sem dependências externas).

**Windows (PowerShell):**
```powershell
cd ..\maquina-tracos
python executar.py
```

**Linux / macOS:**
```bash
cd ../maquina-tracos
python3 executar.py
```

O script imprime todos os traços no console **e** salva os resultados em
`maquina-tracos/saidas/`:

| Arquivo | Conteúdo |
|---------|----------|
| `traco_monolitico.txt` | fita do programa monolítico (N=3, 4, 5) |
| `traco_iterativo.txt` | fita do programa iterativo (N=3, 4, 5) |
| `traco_iterativo_decrescente.txt` | fita da versão decrescente |
| `traco_recursivo.txt` | fita do programa recursivo normalizado |
| `traco_recursivo_detalhado.txt` | versão anotada do recursivo |
| `tracos_todos.txt` | concatenação de todos os traços |
| **`analise_equivalencia.txt`** | demonstração P1 ≡ P2 (equivalência forte) |
| **`analise_nao_equivalencia.txt`** | demonstração P2 ≢ P3 (não-equivalência) |

---

## 7. Roteiro de demonstração em sala

Sugestão de sequência para a apresentação (use os binários **já
compilados** em casa, para não perder tempo).

### Parte 1 — a função computada (slide 9)

Abra um terminal na pasta `src/` e mostre que os quatro programas
produzem a mesma saída.

**Windows:**
```powershell
Write-Output 5 | .\monolitico.exe
Write-Output 5 | .\iterativo.exe
Write-Output 5 | .\iterativo_decrescente.exe
Write-Output 5 | .\recursivo.exe
```

**Linux / macOS:**
```bash
echo 5 | ./monolitico
echo 5 | ./iterativo
echo 5 | ./iterativo_decrescente
echo 5 | ./recursivo
```

Comentário sugerido:
> "Os quatro programas computam a mesma função — todos retornam n!.
> Mas isso só mostra equivalência funcional, não forte. Para distinguir,
> precisamos da Máquina de Traços."

### Parte 2 — a Máquina de Traços (slide 11)

**Windows:**
```powershell
cd ..\maquina-tracos
python executar.py
type saidas\traco_monolitico.txt
```

**Linux / macOS:**
```bash
cd ../maquina-tracos
python3 executar.py
cat saidas/traco_monolitico.txt
```

Comentário sugerido:
> "Aqui está a fita da Máquina de Traços para o programa monolítico com
> N = 3. Cada linha é uma configuração ⟨rótulo, estado⟩. Treze passos
> até o `pare`."

### Parte 3 — o caso de equivalência (slide 12)

**Windows:**
```powershell
type saidas\analise_equivalencia.txt
```

**Linux / macOS:**
```bash
cat saidas/analise_equivalencia.txt
```

Destaque as cinco linhas `equivalentes ? True`:
> "Para N = 0, 1, 3, 5, 7, a MT confirma: P1 e P2 são fortemente
> equivalentes. Mesma cadeia de configurações, passo a passo."

### Parte 4 — o caso de NÃO-equivalência (slide 13)

**Windows:**
```powershell
type saidas\analise_nao_equivalencia.txt
```

**Linux / macOS:**
```bash
cat saidas/analise_nao_equivalencia.txt
```

Este é **o ponto central do trabalho**. Mostre a seção
`PRIMEIRA DIVERGENCIA no passo 2` e comente:
> "P2 e P3 computam a mesma função — ambos dão 24 para N = 4. Mas os
> traços divergem já no passo 2: em P2, `I ← 1`; em P3, `I ← N`. Mesmo
> resultado final, cadeias diferentes — não são fortemente equivalentes."

### Parte 5 — o bônus Assembly (opcional, +0,5)

**Windows:**
```powershell
cd ..\src
Write-Output 5 | .\monolitico_asm.exe
```

**Linux:**
```bash
cd ../src
echo 5 | ./monolitico_asm
```

Comentário sugerido:
> "Mesmo programa monolítico, mas em Assembly x86-64. Veja como `cmp/jg`,
> `imul`, `inc`, `jmp` correspondem diretamente às instruções rotuladas
> 3, 4, 5, 6 do pseudocódigo."

---

## 8. Como este trabalho atende à rubrica

| # | Critério | Onde encontrar |
|---|----------|----------------|
| 1 | Definição do problema e aderência ao escopo | Seção 2 deste README + `docs/analise_formal.md` |
| 2 | Três programas (monolítico, iterativo, recursivo) | Pasta `src/` (4 arquivos .c + 1 .asm bônus) |
| 3 | Aplicação da MT e análise formal | Pasta `maquina-tracos/` e saídas em `maquina-tracos/saidas/` |
| 4 | Exemplo de equivalência e não-equivalência | `saidas/analise_equivalencia.txt` e `saidas/analise_nao_equivalencia.txt` |
| 5 | Função computada e exemplos de execução | `exemplos/execucao.md` + tabela na Seção 2 |
| 6 | Organização, GitHub, apresentação, uso de IA | Este README + `docs/apresentacao.pptx` + `docs/uso_de_ia.md` |
| Bônus | Programa monolítico em Assembly | `src/monolitico.asm` |

---

## 9. Troubleshooting

### `gcc` / `python` / `nasm` não é reconhecido (Windows)
O executável não está no PATH. Siga a seção **5.1** — em especial o
passo 3 (adicionar `C:\msys64\ucrt64\bin` ao PATH) e o passo 5 (fechar
e reabrir o PowerShell). Para o Python, reinstale marcando
**"Add Python to PATH"** na primeira tela.

### "Permission denied" ao executar `./programa` (Linux/macOS)
Dê permissão de execução:
```bash
chmod +x monolitico iterativo iterativo_decrescente recursivo
```

### O `nasm` reclama de formato desconhecido
Verifique o sistema operacional e use o formato correto:
- Windows → `-f win64`
- Linux → `-f elf64`
- macOS → `-f macho64`

### A MT reclama de "limite de passos excedido"
Significa que um programa normalizado entrou em laço infinito. Verifique
a definição em `maquina-tracos/programas.py`.

### `ModuleNotFoundError: No module named 'mt'`
Você precisa executar o script **de dentro da pasta** `maquina-tracos/`.
Entre primeiro com `cd maquina-tracos` e depois rode `python executar.py`
(ou `python3 executar.py` no Linux/macOS).

### Acentos aparecem errados no PowerShell
O PowerShell às vezes mostra caracteres acentuados de forma estranha.
Rode antes:
```powershell
chcp 65001
```
para forçar UTF-8.

---

## 10. Referências

- DIVERIO, T. A.; MENEZES, P. F. B. *Teoria da Computação: Máquinas
  Universais e Computabilidade*. 3ª ed. Porto Alegre: Bookman.
- Material didático da disciplina (slides do Prof. Daniel Leal Souza).

---

## 11. Uso de Inteligência Artificial

O uso de IA no desenvolvimento deste trabalho está documentado em
[`docs/uso_de_ia.md`](docs/uso_de_ia.md), conforme exigido pelas
orientações do trabalho.
