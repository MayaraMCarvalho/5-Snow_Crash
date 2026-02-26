# Level 𝟘𝟚

## 🎯 Objetivo
O objetivo deste nível é recuperar uma senha interceptada em uma captura de tráfego de rede antiga. O desafio envolve análise de pacotes (Packet Analysis) e reconstrução de fluxo TCP.

## 🔍 Análise da Vulnerabilidade

* **Tipo:** Protocolo Não Criptografado (Cleartext Protocol) / Sniffing.
* **Arquivo Alvo:** `level02.pcap` (Packet Capture)
* **Ferramenta:** Wireshark.

A vulnerabilidade reside no uso de um protocolo de comunicação inseguro (**Telnet** antigo) que transmite dados, incluindo credenciais de login, em texto plano (cleartext). Diferente do SSH (que é encriptado), tudo o que passa pelo fio no Telnet pode ser lido por qualquer pessoa que esteja "escutando" a rede (Man-in-the-Middle).

Além disso, a captura revela o comportamento de digitação do usuário, incluindo erros e correções (backspaces).

## 💻 Passos para Exploração (Exploit)

1. **Extração:**
    Transferimos o arquivo `level02.pcap` da VM para a máquina local para análise gráfica.

    ```bash
    # No computador local (Host):
    scp -P 4242 level02@<IP_VM>:level02.pcap level02.pcap
    ```

2. **Identificação do arquivo:**
    Para confirmar o tipo de arquivo que encontramos, usamos o comando `file`:

    ```bash
    file level02.pcap
    # Saída: level02.pcap: tcpdump capture file (little-endian) - version 2.4 (Ethernet, capture length 16777216)
    ```

3. **Análise com Wireshark:**
    Abrimos o arquivo no Wireshark, em Analisar selecionamos `level02.pcap`.
    1. Clicamos com o botão direito em um dos pacotes TCP.
    2. Selecionamos **Follow -> TCP Stream (Seguir -> Fluxo TCP)**.

    Isso reconstrói a conversa inteira entre o cliente e o servidor. Visualisamos o seguinte:

    ```plaintext
    Password:
    ft_wandr...NDRel.L0L
    ```
    > *Os pontos representam caracteres não imprimíveis na interface.*

4. **Reconstrução da Senha:**
    Ao verificar a representação **Hexdump** (dados brutos) dentro do Wireshark, notamos o byte `7f`.
    * `7f` em ASCII é o código para **DELETE (DEL)**.
    * Isso significa que o usuário errou a senha enquanto digitava e pressionou "Backspace".
    Devemos aplicar essa ação para revelar a senha real.

    **Senha Final Reconstruída:**
    `ft_waNDReL0L`

## 🚩 Solução / Flag
Com a senha decifrada, logamos na conta `flag02` e capturamos o token final.

```bash
su flag02
# Inserir a senha decifrada: `ft_waNDReL0L`
getflag
```

## 🛡️ Prevenção (Como corrigir)
1. **Use Criptografia**: Nunca utilize protocolos de texto plano como Telnet, FTP ou HTTP para transmitir credenciais. Sempre utilize suas verões seguras: **SSH**, **SFTP** e **HTTPS**.
2. **VPNs**: Se for necessário usar protocolos legados inseguros, eles devem ser encapsulados dentro de um túnel VPN criptografado.
