# ❄️ Snow Crash
(42 São Paulo)

Available in: [🇺🇸 English](README.en.md)

![42 São Paulo](https://img.shields.io/badge/42-São_Paulo-black)
![Security](https://img.shields.io/badge/Focus-Cybersecurity-red)
![Language](https://img.shields.io/badge/Language-C_/_ASM_/_Python-blue)
![Status](https://img.shields.io/badge/Status-In_Progress-yellow)

Este projeto é uma introdução prática à Segurança Cibernética no formato **CTF (Capture The Flag)**. O objetivo é explorar vulnerabilidades em um sistema Linux para escalar privilégios, nível por nível, utilizando técnicas de engenharia reversa, exploração de binários e scripting.

## 📜 Índice

* [Visão Geral](#-vis%C3%A3o-geral)
* [Estrutura do Desafio](#%EF%B8%8F-estrutura-do-desafio)
* [Ferramentas Utilizadas](#%EF%B8%8F-ferramentas-utilizadas)
* [Estrutura do Repositório](#-estrutura-do-repositório)
* [Modo de Uso](#-modo-de-uso)
* [Disclaimer](#%EF%B8%8F-disclaimer)
* [Autora](#-autora)

---

## 📖 Visão Geral

**Snow Crash** é um _Wargame_ de segurança. Você recebe uma Máquina Virtual (ISO) com diversos usuários (`level00` a `level14`). O objetivo é encontrar falhas de segurança — desde permissões mal configuradas até estouros de buffer (Buffer Overflows) — para obter a senha do próximo nível.

### 🎯 Objetivos de Aprendizado

O projeto visa desenvolver o "mindset" de segurança:

1. **Spot**: Identificar onde o software é frágil.
2. **Exploit**: Entender como a falha funciona e criar um método para explorá-la.
3. **Fix**: (Conceitual) Entender como o código deveria ter sido escrito para evitar a falha.


Este projeto foca no desenvolvimento de **lógica de segurança** e **atenção aos detalhes**. As principais competências trabalhadas incluem:

-   🕵️ **Engenharia Reversa:** Análise de binários compilados (Assembly x86).
-   🛡️ **Exploração de Binários:** Buffer Overflows, Shellcode Injection, Format String Attacks.
-   🐧 **Linux Internals:** Manipulação de SUID/SGID, permissões, variáveis de ambiente.
-   🐛 **Scripting:** Automação de ataques com Python, Perl e Bash.
-   🕸️ **Network Basics:** Análise de tráfego (Packet Analysis).
-   🔒 **Criptografia:** Identificação e quebra de hashes e cifras antigas.

---

## 🏗️ Estrutura do Desafio

O projeto é dividido em níveis que devem ser resolvidos sequencialmente.

🟢 **Parte Obrigatória**
- **Level 00 a 09**: Introdução ao ambiente Linux, permissões SUID, scripts vulneráveis (Perl/PHP) e injeção de comandos básicos.

🔴 **Parte Bônus**
- **Level 10 a 14**: Desafios avançados envolvendo Race Conditions, manipulação complexa de memória e Shellcode Injection.

🚩 **A Flag**

Para passar de nível, você deve logar na conta `flagXX` (onde XX é o nível atual) explorando uma vulnerabilidade e executar o comando:

	getflag
> Isso retornará a senha (token) para o login do próximo nível.

---

## 🛠️ Ferramentas Utilizadas

Durante a resolução dos desafios, as seguintes ferramentas e tecnologias são empregadas:

-   **GDB (GNU Debugger):** Para inspeção de memória e registradores em tempo real.
-   **GCC:** Para compilação de exploits.
-   **Python / Perl:** Para criação de scripts de injeção e manipulação de bytes.
-   **Objdump / Strings:** Para análise estática de binários.
-   **Wireshark:** Para análise de pacotes de rede (arquivos .pcap).
-   **VirtualBox / VMWare:** Para execução da ISO do projeto.

---

## 📂 Estrutura do Repositório

Seguindo as normas da 42, este repositório contém uma pasta para cada nível resolvido. Dentro de cada pasta, encontram-se a flag obtida e a documentação de como a vulnerabilidade foi explorada.

```text
.
├── level00/
│   ├── flag            # A senha para o próximo nível
│   └── resources/      # Scripts, notas e arquivos usados para o exploit
├── level01/
├── level02/
├── ...
└── README.md
```

### 🚩 Níveis e Vulnerabilidades

Abaixo está um resumo dos conceitos abordados em cada nível completado:

| Nível | Tipo de Vulnerabilidade / Conceito Chave | Status |
| :---: | :--- | :---: |
| **00** | _Exposição de Dados Sensíveis / Permissões_ | ✅ |
| **01** | _Armazenamento Inseguro de Senha (Legacy Shadow)_ | ✅ |
| **02** | _Protocolos em Texto Plano / Captura de Pacotes_ | ✅ |
| **03** | _PATH inseguro/Sequestro de SUID_ | ✅ |
| **04** | _Injeção de comandos do sistema operacional / CGI inseguro_ | ✅ |
| **05** | _Tarefa Cron Insegura / Execução Arbitrária de Código_ | ✅ |
| **06** | _Injeção de código / Modificador PHP preg_replace() /e_ | ✅ |
| **07** | _Injeção de comandos do sistema operacional via variável de ambiente ($LOGNAME)_ | ✅ |
| **08** | _Vulnerabilidade a definir_ | ⏳ |
| **09** | _Vulnerabilidade a definir_ | ⏳ |
| **10** | _+Níveis Bônus (Hardcore)_ | 🔒 |

> Nota: A tabela será atualizada conforme o progresso no projeto.

---

## 🚀 Modo de Uso

Este projeto requer a ISO específica do Snow Crash fornecida pela 42 (disponível na intra). Você deve se conectar à máquina virtual via SSH. A porta padrão do serviço SSH na VM é **4242**.

1. **Conexão Inicial**

	1. Inicie a VM com a ISO do Snow Crash.
	2. Identifique o IP da máquina (geralmente exibido no boot ou via ifconfig).
	3. Conecte-se via SSH na porta 4242:

		```bash
		ssh levelXX@<IP_DA_VM> -p 4242
		```

	> A senha inicial para o level00 é `level00`.

2. **Fluxo de Resolução**

Uma vez logado:

1. Analise os arquivos no diretório home ou `/var/www` etc.
2. Encontre a vulnerabilidade.
3. Explore-a para rodar um comando como o usuário `flagXX`.
4. Execute `getflag`.
5. Anote a senha e use-a para conectar no próximo nível: `su level01`.

---

## ⚠️ Disclaimer

Todo o conteúdo deste repositório foi desenvolvido para fins estritamente **educacionais** como parte do currículo da escola 42. As técnicas demonstradas aqui são realizadas em um ambiente controlado e isolado (Sandbox). O uso dessas técnicas em sistemas sem autorização explicita é ilegal e antiético.

---

## 👩🏻 Autora

**Mayara Carvalho**
<br>
[:octocat: @MayaraMCarvalho](https://github.com/MayaraMCarvalho) | 42 Login: `macarval`

---
