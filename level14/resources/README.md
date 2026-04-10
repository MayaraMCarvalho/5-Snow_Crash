# 𝕃𝕖𝕧𝕖𝕝 𝟙𝟜

## 🎯 Objetivo
O objetivo deste nível final é comprometer o próprio validador do sistema (`/bin/getflag`), utilizando Análise Dinâmica para contornar proteções _anti-debugging_ e forjar uma identidade de usuário (UID) em tempo de execução, escalando privilégios sem a necessidade de explorar arquivos locais.

## 🔍 Análise da Vulnerabilidade
* **Tipo:** _Anti-Debugging Bypass / Dynamic Memory Manipulation / Insecure Authorization._
* **Arquivo Alvo:** `/bin/getflag` (O executável universal que gerencia as flags do sistema).
* **Comportamento:** Ao notar que o diretório do usuário `level14` não possuía nenhum vetor de ataque e que varreduras no sistema (`find`) não retornavam nada, o foco foi redirecionado para o binário principal. O `/bin/getflag` possui duas barreiras:

    1. **Proteção Anti-Debugging:** Usa a chamada de sistema `ptrace` para detectar se está sendo executado dentro de um depurador (como o GDB). Se o `ptrace` falhar (retornando `-1` no registrador EAX), o programa aborta com a mensagem `"You should not reverse this"`.

    2. **Verificação de Autorização:** Usa `getuid()` para checar se quem está chamando o programa tem o direito de ver a flag.

    A vulnerabilidade consiste em utilizar o GDB para sequestrar a execução em múltiplos pontos, neutralizando o detector de depurador e forjando o UID alvo (`3014` pertencente ao `flag14`) forçando a entrega da flag.

## 💻 Passos para Exploração (Exploit)

1.  **Reconhecimento:**
    Sem vetores locais, buscamos o UID do usuário alvo (flag14) no arquivo de senhas do sistema.

    ```bash
    cat /etc/passwd
    # Identificamos o UID: 3014
    ```

2.  **Análise e Descompilação:**
    Rodamos `ltrace /bin/getflag` e identificamos a chamada ao `ptrace`. Baixamos o executável e analisamos o Assembly no GDB para mapear os endereços de memória cruciais.

3.  **Configuração do GDB:**
    Iniciamos o `/bin/getflag` no GDB e configuramos dois breakpoints estratégicos: um logo após a execução do `ptrace` e outro logo após a execução do `getuid`.

    ```bash
    gdb /bin/getflag
    (gdb) disas main
    (gdb) break *0x0804898e  # Logo após o call ptrace
    (gdb) break *0x08048b0a  # Logo após a verificação do getuid
    ```

4.  **Bypass do Anti-Debugging:**
    Iniciamos a execução. O programa congela no primeiro breakpoint. O `ptrace` já detectou o GDB e preencheu o registrador de retorno com `-1`. Alteramos esse valor para 0 na força bruta, enganando a validação de segurança.

    ```bash
    (gdb) run
    (gdb) set $eax = 0
    (gdb) continue
    ```

5.  **Falsificação de Identidade (Spoofing de UID):**
    O programa avança e congela no segundo breakpoint após verificar o nosso UID real. Sobrescrevemos a memória novamente, injetando o UID `3014` (`flag14`) no registrador para que a matemática de autorização seja válida.

    ```bash
    (gdb) set $eax = 3014
    (gdb) continue
    ```
    > Totalmente enganado pelo estado corrompido de seus registradores, o programa processa a criptografia e entrega a flag na tela.

## 🚩 Solução / Flag
O bypass duplo na memória retornou a flag corretamente.

## 🛡️ Prevenção (Como corrigir)
1. **Verificação Remota (Server-side):** A falha fundamental é a mesma do Nível 13: o cliente não deve tomar decisões de segurança sobre si mesmo. A entrega de flags deveria depender de uma verificação do lado do servidor via sockets ou APIs autenticadas.

2. **Anti-Debugging Resiliente**: Apenas chamar `ptrace` e checar o retorno `if (lVar2 < 0)` é fraco, pois o retorno pode ser manipulado em tempo de execução. Proteções avançadas envolvem ofuscação pesada, checagens de _timing_ (medir quanto tempo uma instrução levou para rodar, já que o GDB deixa tudo mais lento) e cálculo de integridade da própria memória (checksum do código em execução).
