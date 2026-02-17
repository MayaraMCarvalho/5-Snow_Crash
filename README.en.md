# ❄️ Snow Crash
(42 São Paulo)

Available in: [🇧🇷 Português](README.md)

![42 São Paulo](https://img.shields.io/badge/42-São_Paulo-black)
![Security](https://img.shields.io/badge/Focus-Cybersecurity-red)
![Language](https://img.shields.io/badge/Language-C_/_ASM_/_Python-blue)
![Status](https://img.shields.io/badge/Status-In_Progress-yellow)

This project is a practical introduction to Cybersecurity in a **CTF (Capture The Flag)** format. The goal is to exploit vulnerabilities in a Linux system to escalate privileges, level by level, using reverse engineering, binary exploitation, and scripting techniques.

## 📜 Table of Contents

* [Overview](#-overview)
* [Challenge Structure](#%EF%B8%8F-challenge-structure)
* [Tools Used](#%EF%B8%8F-tools-used)
* [Repository Structure](#-repository-structure)
* [Usage](#-usage)
* [Disclaimer](#%EF%B8%8F-disclaimer)
* [Author](#-author)

---

## 📖 Overview

**Snow Crash** is a security _Wargame_. You are provided with a Virtual Machine (ISO) containing various users (`level00` to `level14`). The goal is to find security flaws — ranging from misconfigured permissions to Buffer Overflows — to obtain the password for the next level.

### 🎯 Learning Objectives

The project aims to develop a security "mindset":

1. **Spot**: Identify where the software is fragile.
2. **Exploit**: Understand how the flaw works and create a method to exploit it.
3. **Fix**: (Conceptual) Understand how the code should have been written to avoid the flaw.


This project focuses on developing **security logic** and **attention to detail**. Key competencies worked on include:

-   🕵️ **Reverse Engineering:** Analysis of compiled binaries (Assembly x86).
-   🛡️ **Binary Exploitation:** Buffer Overflows, Shellcode Injection, Format String Attacks.
-   🐧 **Linux Internals:** Handling SUID/SGID, permissions, environment variables.
-   🐛 **Scripting:** Automating attacks with Python, Perl, and Bash.
-   🕸️ **Network Basics:** Traffic analysis (Packet Analysis).
-   🔒 **Cryptography:** Identifying and cracking hashes and ancient ciphers.

---

## 🏗️ Challenge Structure

The project is divided into levels that must be solved sequentially.

🟢 **Mandatory Part**
- **Level 00 to 09**: Introduction to the Linux environment, SUID permissions, vulnerable scripts (Perl/PHP), and basic command injection.

🔴 **Bonus Part**
- **Level 10 to 14**: Advanced challenges involving Race Conditions, complex memory manipulation, and Shellcode Injection.

🚩 **The Flag**

To pass a level, you must log into the `flagXX` account (where XX is the current level) by exploiting a vulnerability and run the command:

    getflag
> This will return the password (token) for the next level's login.

---

## 🛠️ Tools Used

During the resolution of the challenges, the following tools and technologies are employed:

-   **GDB (GNU Debugger):** For real-time inspection of memory and registers.
-   **GCC:** For compiling exploits.
-   **Python / Perl:** For creating injection scripts and byte manipulation.
-   **Objdump / Strings:** For static analysis of binaries.
-   **Wireshark:** For network packet analysis (.pcap files).
-   **VirtualBox / VMWare:** For running the project ISO.

---

## 📂 Repository Structure

Following 42 standards, this repository contains a folder for each solved level. Inside each folder, you will find the obtained flag and documentation on how the vulnerability was exploited.

```text
.
├── level00/
│   ├── flag            # The password for the next level
│   └── resources/      # Scripts, notes, and files used for the exploit
├── level01/
├── level02/
├── ...
└── README.md
```

### 🚩 Levels and Vulnerabilities

Below is a summary of the concepts covered in each completed level:

| Level | Vulnerability Type / Key Concept | Status |
| :---: | :--- | :---: |
| **00** | _Find / Basic Linux Commands_ | ✅ |
| **01** | _Vulnerability to be defined_ | ✅ |
| **02** | _Vulnerability to be defined_ | ✅ |
| **03** | _Vulnerability to be defined_ | ⏳ |
| **04** | _Vulnerability to be defined_ | ⏳ |
| **05** | _Vulnerability to be defined_ | ⏳ |
| **06** | _Vulnerability to be defined_ | ⏳ |
| **07** | _Vulnerability to be defined_ | ⏳ |
| **08** | _Vulnerability to be defined_ | ⏳ |
| **09** | _Vulnerability to be defined_ | ⏳ |
| **10** | _+Bonus Levels (Hardcore)_ | 🔒 |

> Note: The table will be updated as the project progresses.

---

## 🚀 Usage

This project requires the specific Snow Crash ISO provided by 42 (available on the intra). You must connect to the virtual machine via SSH. The default SSH port on the VM is **4242**.

### 1. Initial Connection

1.  Start the VM with the Snow Crash ISO.
2.  Identify the machine's IP (usually displayed at boot or via `ifconfig`).
3.  Connect via SSH on port 4242:

    ```bash
    ssh levelXX@<VM_IP> -p 4242
    ```

> The initial password for level00 is `level00`.

### 2. Resolution Flow

Once logged in:

1.  Analyze files in the home directory or `/var/www` etc.
2.  Find the vulnerability.
3.  Exploit it to run a command as user `flagXX`.
4.  Run `getflag`.
5.  Note the password and use it to connect to the next level: `su level01`.

---

## ⚠️ Disclaimer

All content in this repository was developed for strictly **educational** purposes as part of the 42 school curriculum. The techniques demonstrated here are performed in a controlled and isolated environment (Sandbox). Using these techniques on systems without explicit authorization is illegal and unethical.

---

## 👩🏻 Author

**Mayara Carvalho**
<br>
[:octocat: @MayaraMCarvalho](https://github.com/MayaraMCarvalho) | 42 Login: `macarval`

---
