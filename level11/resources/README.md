# 𝕃𝕖𝕧𝕖𝕝 𝟙𝟙

## 🎯 Objetivo
O objetivo deste nível é escalar privilégios explorando uma vulnerabilidade de Injeção de Comandos Cega (_Blind Command Injection_) em um serviço escrito em Lua que roda continuamente no sistema.

## 🔍 Análise da Vulnerabilidade
* **Tipo:** _Blind OS Command Injection_ (Injeção de Comando do Sistema Operacional Cega).
* **Arquivo Alvo:** `level11.lua` (Serviço rodando em background na porta 5151 com privilégios de `flag11`).
* **Comportamento:** O script Lua inicia um servidor TCP que escuta na porta 5151. Ao receber um texto (a senha), ele utiliza a função `io.popen()` para invocar o shell do Linux e calcular a hash SHA1 da entrada:

    ```Lua
    prog = io.popen("echo "..pass.." | sha1sum", "r")
    ```

    A vulnerabilidade ocorre porque a variável `pass` (controlada pelo usuário) é concatenada diretamente na string do comando sem nenhuma sanitização. O atacante pode injetar comandos arbitrários (como uma subshell `$()`).
    No entanto, trata-se de uma injeção "cega" (_blind_). A saída do comando injetado não é devolvida pela conexão de rede, pois o pipe `|` e o `sha1sum` mascaram o resultado, e o script Lua apenas retorna um "Erf nope.." se a hash resultante não for a esperada.

## 💻 Passos para Exploração (Exploit)

1.  **Reconhecimento:**
    Listamos o diretório e encontramos o arquivo `level11.lua` configurado com permissões SUID (`-rwsr-sr-x`).
    ```Bash
    ls -al
    ```

2.  **Análise de Código:**
    Transferimos e lemos o arquivo Lua localmente e identificamos a porta de escuta (`5151`) e a falha de concatenação no `io.popen`.
    ```Bash
    scp -P 4242 level11@192.168.56.101:level11.lua level11.lua
    # Arquivo:
    # ...
    # prog = io.popen("echo "..pass.." | sha1sum", "r")
    # ...
    ```

3.  **Teste de Contexto:**
    Testar o comando `getflag` diretamente no terminal atual retorna uma mensagem de erro falsa, provando que o comando precisa obrigatoriamente ser executado pelo serviço (que possui os privilégios do usuário `flag11`).
    ```bash
    echo $(getflag)
    # Check flag.Here is your token : Nope there is no token here for you sorry. Try again :)
    ```

4.  **Exploração:**
    Conectamos ao serviço usando o Netcat. Como não podemos ver a saída do nosso comando diretamente na tela (Blind Injection), injetamos uma subshell `$()` executando o `getflag` e redirecionamos `>` a saída dele para um arquivo de texto na pasta pública `/tmp/`. Depois lemos o arquivo gerado na pasta temporária, que agora contém a execução bem-sucedida do comando com os privilégios corretos.
    ```bash
    nc 127.0.0.1 5151
    Password: $(getflag > /tmp/flag_level)
    # Saída: Erf nope.. (Comportamento esperado)
    cat /tmp/flag_level
    # Saída: Check flag.Here is your token : fa6v5ate...
    ```

## 🚩 Solução / Flag
O comando injetado foi executado pelo shell do sistema via Lua, redirecionando o token de acesso da conta `flag11` para um arquivo legível pelo nosso usuário.

## 🛡️ Prevenção (Como corrigir)
1. **Evitar Execução via Shell:** Em Lua (ou qualquer outra linguagem), evite usar funções que invocam o shell do sistema operacional (como `io.popen`, `os.execute` ou `system()`) para processar dados de entrada do usuário.

2. **Uso de Bibliotecas Nativas:** Se o objetivo é calcular a hash SHA1 de uma string, o código deve utilizar uma biblioteca criptográfica nativa da linguagem (ex: `lua-crypto`, `lua-resty-string`) para calcular a hash diretamente na memória, sem invocar o `/bin/sh` ou utilitários externos.
