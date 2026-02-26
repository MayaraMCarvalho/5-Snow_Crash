# 𝕃𝕖𝕧𝕖𝕝 𝟘𝟠

## 🎯 Objetivo
Descrever brevemente o que encontramos ao logar neste nível (ex: um executável SUID, um script perl, um arquivo pcap).

## 🔍 Análise da Vulnerabilidade
Explique aqui qual foi a falha encontrada.
* **Tipo:** (Ex: Stack Buffer Overflow, Command Injection, Race Condition).
* **Arquivo Alvo:** `/home/user/levelXX/binario`
* **Comportamento:** O programa usa a função `strcpy` sem verificar o tamanho da entrada... (explique tecnicamente).

## 💻 Passos para Exploração (Exploit)

1.  **Reconhecimento:**
    Identificamos que o binário tem permissão SUID para o usuário `flagXX`.
    Comando: `ls -l`

2.  **Debugging (se aplicável):**
    Encontramos o offset de memória 76 usando o GDB pattern create...
    Endereço do buffer: `0xbffff...`

3.  **Payload:**
    Criamos um payload contendo:
    `[Padding] + [Endereço de Retorno] + [NOP Sled] + [Shellcode]`

    Comando exato utilizado:
    ```bash
    (python -c 'print "A"*76 + "\xef\xbe\xad\xde"') | ./levelXX
    ```

## 📜 Scripts Utilizados
Se você criou um script python ou bash para automatizar, coloque-o na pasta `resources` e referencie aqui.

* `resources/exploit.py`: Script que gera a string maliciosa.

## 🚩 Solução / Flag
(Opcional, mas útil para referência futura. Não coloque a flag literal se preferir, mas sim a senha obtida).

Senha para o próximo nível: `xxxxxxxxxxxx`

## 🛡️ Prevenção (Como corrigir)
Como esse código deveria ter sido escrito para ser seguro?
* *Exemplo:* Deveria ter sido usada a função `strncpy` ao invés de `strcpy` para limitar o tamanho da cópia.
