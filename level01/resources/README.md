# Level XX

## 🎯 Objetivo
O objetivo deste nível é obter acesso ao usuário `flag00`. Para isso, precisamos encontrar onde a senha ou um método de escalação de privilégio foi deixado no sistema.

## 🔍 Análise da Vulnerabilidade

**Tipo:** Exposição de Informação Sensível (Sensitive Information Exposure) / Permissões de Arquivo Inseguras.

* **Arquivo Alvo:** `/usr/sbin/john`
    ```bash
    ----r--r-- 1 flag00 flag00 15 Mar  5  2016 /usr/sbin/john
    ```

* **Comportamento:** A vulnerabilidade consiste no fato de que um arquivo pertencente ao usuário alvo (`flag00`) foi deixado no sistema com permissões de leitura para "outros" (world-readable). Isso permite que qualquer usuário logado no sistema (neste caso, `level00`) leia seu conteúdo.

Além disso, o conteúdo do arquivo estava ofuscado com uma cifra de substituição simples, o que não constitui uma proteção real de segurança ("Security by Obscurity").

## 💻 Passos para Exploração (Exploit)

1. **Reconhecimento:**
    Primeiro, buscamos por todos os arquivos no sistema que pertencem ao usuário `flag00` e ignoramos os erros de permissão para limpar a saída.

    Comando utilizado:
    ```bash
    find / -user flag00 2>/dev/null
    ```

    **Resultado**:
    O comando retornou um arquivo suspeito fora dos diretórios padrões:
    `/usr/sbin/john`

2. **Extração:**
    Lemos o conteúdo do arquivo encontrado:

    ```bash
    cat /usr/sbin/john
    ```

    **Saída**:

    ```plaintext
    cdiiddwpgswtgt (string encriptada)
    ```
    > Ao tentar usar essa senha, resultou em `Authentication failure`

3. **Decriptação:**

    A string encontrada não era a senha direta. Identificamos que se tratava de uma **Cifra de Rotação (Caesar Cipher / ROT)**.

    * **String original**: `cdiiddwpgswtgt`
    * **Método**: Rotação de caracteres (ROT11).
    * **Resultado**: `nottoohardhere`
    > Utilizamos ferramentas online (como dcode.fr) ou o comando tr para decifrar.

## 📜 Scripts Utilizados

Para automatizar o processo de decriptação e evitar tentativas manuais, foi criado um script em Python (`resources/decript.py`). Este script realiza um ataque de força bruta local no espaço de chaves da Cifra de César (apenas 26 possibilidades).

**Explicação Técnica**:
O script itera por um `range(26)`, representando todas as rotações possíveis do alfabeto.

1. `ord(char) - ord('a')`: Transforma o alfabeto ASCII (97 a 122) num alfabeto matemático simples (0 a 25).
2. `+ i`: Aplica o deslocamento da rotação atual.
3. `% 26` **(Módulo)**: Garante a circularidade da cifra. Se a soma ultrapassar 25 (letra 'z'), o operador de resto da divisão faz o valor "dar a volta" e recomeçar do 'a'.
4. `chr(...)`: Converte o valor numérico resultante de volta para um caractere legível.

> Nota: Este script roda localmente sobre uma string já capturada. Ele não realiza força bruta contra o serviço SSH ou login do sistema, respeitando as regras do projeto.

## 🚩 Solução / Flag

Com a senha decifrada, logamos na conta `flag00` e capturamos o token final.

    ```bash
    su flag00
    # Inserir a senha decifrada: `nottoohardhere`
    getflag
    ```

Senha para o próximo nível: `nottoohardhere`

## 🛡️ Prevenção (Como corrigir)

Para evitar essa falha, o administrador do sistema deveria ter seguido o princípio do menor privilégio:

1. **Permissões**: O arquivo `/usr/sbin/john` deveria ter permissões restritas (ex: `600` ou `rw-------`), permitindo leitura apenas pelo dono (`root` ou `flag00`).

2. **Armazenamento**: Senhas nunca devem ser armazenadas em arquivos de texto plano ou com criptografia reversível simples. O ideal é usar Hashes fortes (como SHA-256 ou bcrypt) com Salt (uma string aleatória de caracteres que é adicionada à senha antes de ela criptografada pelo Hash).
O banco de dados deve guardar: `Hash(bcrypt(Senha + Salt_Aleatório))`

Isso garante que:
1. Ninguém consegue ler a senha (Hash).
2. Tabelas prontas não funcionam (Salt).
3. Tentativa e erro (Força Bruta) é lenta demais para ser viável (bcrypt).
