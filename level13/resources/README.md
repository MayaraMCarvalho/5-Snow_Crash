# 𝕃𝕖𝕧𝕖𝕝 𝟙𝟛

## Objetivo
O objetivo deste nível é contornar uma verificação de identificação de usuário (UID) embutida em um executável compilado. A resolução documenta duas abordagens de Engenharia Reversa: a Análise Estática (extração e reconstrução do algoritmo) e a Análise Dinâmica (manipulação de memória e registradores em tempo de execução).

## Análise da Vulnerabilidade
* **Tipo:** _Hardcoded Cryptography / Insecure Authorization Check / Reverse Engineering._
* **Arquivo Alvo:** `level13` (Executável SUID em C).
* **Comportamento:** O binário utiliza a função `getuid()` do sistema operacional para verificar se o usuário que está executando o programa possui o ID `4242` (0x1092 em hexadecimal).

    * Se o UID for diferente, o programa exibe uma mensagem de erro e é encerrado (`exit(1)`).

    * Se o UID for igual a `4242`, ele chama uma função de descriptografia customizada chamada `ft_des()`, passando uma string ofuscada (`"boe]!ai0FB@.:|L6l@A?>qJ}I"`) como argumento, e imprime o token resultante na tela.

A vulnerabilidade estrutural é que **toda a lógica de geração do token já está presente no código do cliente**. O binário não pede a flag para um servidor, ele mesmo a calcula. Isso permite que um atacante extraia o algoritmo ou minta para o processador sobre o seu UID real.

## Passos para Exploração (Exploit)

### Abordagem 1: Análise Estática
_Esta técnica envolve extrair a matemática do programa e executá-la em um ambiente controlado._

1. **Reconhecimento:**
    Executamos `file level13` e descobrimos que é um executável ELF 32-bit. O comando `ltrace ./level13` revela a chamada de sistema de checagem: `UID 2013 started us but we we expect 4242.`

2. **Descompilação:**
    Baixamos o executável e o analisamos em um descompilador. Extraímos o código da função `main` e, principalmente, o corpo inteiro da função criptográfica `ft_des()`.

3. **Reconstrução (Bypass lógico):**
    Ignoramos completamente a checagem de UID original. Criamos um novo arquivo em C copiando a função `ft_des()` exata que estava no binário e escrevemos um `main()` limpo que simplesmente chama a função e imprime o resultado.

4. **Execução:**
    Compilamos o nosso código "clonado" (via compilador online) e o executamos. Como a lógica matemática e a string ofuscada eram as mesmas, ele gerou o token válido para a próxima fase.


### Abordagem 2: Análise Dinâmica
_Esta técnica usa um debugger para sequestrar o fluxo do programa em tempo de execução, mentindo para o processador._

1. **Iniciando o Debugger:**
    Abrimos o binário utilizando o GNU Debugger direto no terminal do servidor.

    ```bash
    gdb ./level13
    ```

2. **Análise de Assembly:**
    Inspecionamos as instruções em linguagem de máquina da função principal para encontrar o momento exato da comparação.

    ```bash
    (gdb) disas main
    ```
    > Identificamos a linha que chama o `getuid` e a instrução `cmp eax, 0x1092` logo em seguida.

3. **Adição do Breakpoint:**
Adicionamos um ponto de parada (_breakpoint_) no endereço de memória exato onde a instrução de comparação (`cmp`) ocorre (ex: `*0x0804859a`).

    ```bash
    (gdb) break *0x0804859a
    ```

4. **Execução e Sequestro:**
Rodamos o programa (`run`). Ele congela no momento do breakpoint. A função `getuid` já rodou e guardou o nosso UID real no registrador `$eax`. Forçamos a substituição desse valor na memória para o UID esperado (`4242`).

    ```bash
    (gdb) set $eax = 4242
    ```

5. **Continuação do Fluxo:**
Com o valor da variável do programa alterado, mandamos a execução continuar (`continue`). A matemática da instrução de comparação agora resulta em verdadeiro, o programa "acredita" que somos o usuário correto e exibe o token na tela.

## Solução / Flag
Ambas as abordagens revelaram que o texto descriptografado pela função `ft_des` geram o mesmo token de acesso.

## Prevenção (Como corrigir)
1. **Não armazenar segredos no binário cliente:** Lógicas de geração de tokens críticos e chaves simétricas de criptografia nunca devem residir no código-fonte que será entregue ao usuário, pois podem ser facilmente extraídas por engenharia reversa estática.

2. **Validação do Lado do Servidor:** A verificação de quem o usuário é não deve ser feita de forma local (`getuid` dentro do app). O aplicativo deveria solicitar o token para um servidor remoto protegido, o qual validaria os cookies/sessão do usuário antes de devolver a string secreta.

3. **Ofuscação e Anti-Debugging:** Em casos onde o cliente _precisa_ calcular algo, o uso de técnicas de ofuscação pesada (packers) e proteções nativas no código para detectar a presença do `ptrace` (a chamada de sistema que o GDB usa) pode dificultar bastante a análise dinâmica, mitigando ataques de manipulação de memória.
