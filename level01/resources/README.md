# 𝕃𝕖𝕧𝕖𝕝 𝟘𝟙

## 🎯 Objetivo
O objetivo deste nível é obter a senha do usuário `flag01`. Nesse nível, será exploarada uma falha na configuração de armazenamento de credenciais do sistema.

## 🔍 Análise da Vulnerabilidade

* **Tipo:** Armazenamento Inseguro de Credenciais (Insecure Credential Storage) / Hash Legado.
* **Arquivo Alvo:** `/etc/passwd`
* **Comportamento:** O sistema Linux moderno utiliza dois arquivos para gerenciar usuários:
    1. `/etc/passwd`: Contém informações públicas do usuário (UID, GID, Home, Shell). Deve ser legível por todos (`world-readable`).
    2. `/etc/shadow`: Contém os **Hashes das senhas**. Deve ser legível apenas pelo `root`.

A vulnerabilidade reside no fato de que a senha do usuário `flag01` não estava armazenada no `/etc/shadow` (representada por um `x` no arquivo passwd), mas sim inserida diretamente no `/etc/passwd`.

Isso expõe o hash da senha para qualquer usuário do sistema, permitindo um ataque de força bruta offline (Cracking).

## 💻 Passos para Exploração (Exploit)

1. **Reconhecimento:**
    Inspecionamos o arquivo de usuários para entender a estrutura do sistema.

    ```bash
    cat /etc/passwd
    ```

    **Resultado**:
    Identificamos uma anomalia na linha do usuário `flag01`:

    ```plaintext
    flag00:x:3000:3000::/home/flag/flag00:/bin/bashh  <-- Usuário seguro (tem 'x')
    flag01:42hDRfypTqqnw:3001:3001::/home/flag/flag01:/bin/bash  <-- VULNERÁVEL
    ```
    A string `42hDRfypTqqnw` é o hash da senha.

2. **Identificação do Hash:**
    Pelo formato curto e pelos caracteres utilizados, identificamos que se trata de um hash **DES (Unix Crypt)** padrão antigo.
    * **Hash**: 42hDRfypTqqnw
    * **Salt**: 42 (os dois primeiros caracteres no DES padrão).

3. **Cracking (Quebra da Senha):**
    Como temos o hash e o salt, podemos usar uma ferramenta de força bruta como o **John the Ripper**.

    Utilizando o **John the Ripper** (ferramenta padrão em CTFs):

    ```bash
    sudo apt install John

    echo "flag01:42hDRfypTqqnw:3001:3001::/home/flag01:/bin/bash" > passwd.txt
    john --show passwd.txt

    flag01:abcdefg:3001:3001::/home/flag/flag01:/bin/bash

    1 password hash cracked, 0 left
    ```

    **Resultado**:
    A ferramenta encontrou a senha: `abcdefg`

## 🚩 Solução / Flag
Com a senha decifrada, logamos na conta `flag01` e capturamos o token final.

```bash
su flag01
# Inserir a senha decifrada: `abcdefg`
getflag
```

Senha para o próximo nível: `abcdefg`

## 🛡️ Prevenção (Como corrigir)

1. **Shadow Suite**: Garantir que o sistema utilize a suite `shadow` corretamente. No arquivo `/etc/passwd`, o campo de senha deve conter apenas um `x`.

2. **Permissões**: O arquivo real de senhas (`/etc/shadow`) deve ter permissão `600 `ou `400` (leitura apenas pelo root).

3. **Algoritmo Forte**: Não utilizar DES ou MD5. Configurar o sistema (via `/etc/login.defs` ou PAM) para usar algoritmos modernos como **SHA-512** (id `$6$`) ou **bcrypt** / **Argon2**, que são resistentes a ataques de força bruta devido ao custo computacional elevado (são lentos de propósito).
