<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=ff2d2d&height=200&section=header&text=PhantomStrike&fontSize=60&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Red+Team+Recon+%26+Pentest+Framework&descAlignY=60&descSize=18&descColor=ffffff" width="100%"/>

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Share+Tech+Mono&size=20&pause=1000&color=FF2D2D&center=true&vCenter=true&width=700&lines=Nmap+%7C+Shodan+%7C+Metasploit+%7C+SSH+BruteForce;DNS+Recon+%7C+FTP+%7C+CVE+%2F+EDB+%2F+MSF+VulnDB;Red+Team+%7C+Pentest+%7C+Bug+Bounty;Authorized+Use+Only+%E2%80%94+Stay+Legal" alt="Typing SVG"/>
</a>

<br/><br/>

![Python](https://img.shields.io/badge/Python-3.8%2B-ff2d2d?style=for-the-badge&logo=python&logoColor=ff2d2d&labelColor=0d1117)
![Platform](https://img.shields.io/badge/Linux%20%7C%20macOS-supported-ff2d2d?style=for-the-badge&logo=linux&logoColor=ff2d2d&labelColor=0d1117)
![Version](https://img.shields.io/badge/Version-1.0-00cfff?style=for-the-badge&labelColor=0d1117)
![Bugs Fixed](https://img.shields.io/badge/Bugs_Fixed-10-ff2d2d?style=for-the-badge&labelColor=0d1117)
![License](https://img.shields.io/badge/License-MIT-gray?style=for-the-badge&labelColor=0d1117)
![Ethics](https://img.shields.io/badge/Authorized_Use_Only-⚠️-ff2d2d?style=for-the-badge&labelColor=0d1117)

</div>

---

## 🔴 What is PhantomStrike?

**PhantomStrike** is a modular Red Team recon and pentest semi-automation framework. It integrates Nmap, Shodan, Metasploit RPC, SSH brute force, DNS recon, FTP probing, and a full CVE/EDB/MSF VulnDB into a single terminal-driven interface built for authorized engagements.

Forked from `penta`, security-audited and rebuilt by **[krypthane](https://github.com/wavegxz-design)** — Red Team Operator from Mexico 🇲🇽.

---

## 🧩 Modules

```
╔══════════════════════════════════════════════════════════════════╗
║               PhantomStrike  v1.0  —  Module Map                ║
╠══════════════════════════════════╦═══════════════════════════════╣
║  RED TEAM RECON                  ║  VULNDB                       ║
╠══════════════════════════════════╬═══════════════════════════════╣
║  [01] Port Scan                  ║  [01] Daily Report            ║
║  [02] Nmap Deep Scan + Scripts   ║  [02] View Saved Reports      ║
║  [03] HTTP Options Audit         ║  [03] Fetch CVEs (NVD)        ║
║  [04] DNS Recon (WHOIS + records)║  [04] Fetch Exploits (EDB)    ║
║  [05] Shodan Intelligence        ║  [05] Fetch MSF Modules       ║
║  [06] FTP Anonymous Login Test   ║  [06] Database Query          ║
║  [07] SSH Brute Force            ╚═══════════════════════════════╣
║  [08] Metasploit RPC             ║                               ║
║  [09] Change Target              ║                               ║
╚══════════════════════════════════╩═══════════════════════════════╝
```

---

## 🔥 Bug Fixes & Security Audit — v1.0

> Full security audit and patch by **krypthane**

| ID | File | Bug | Severity | Fix |
|----|------|-----|----------|-----|
| BUG-01 | `scan_ftp.py` | `self.nmsc` → NameError crash | 🔴 HIGH | Fixed → `self.nm` |
| BUG-02 | `penta.py` | `str.strip('http://')` removes chars, not prefix | 🟡 MED | Fixed → `str.removeprefix()` |
| BUG-03 | `penta.py` | `ip_menu()` / `report_menu()` infinite recursion | 🔴 HIGH | Fixed → `while` loops |
| BUG-04 | `scan_nmap.py` `scan_dns.py` | `logging.warn()` deprecated since Python 3.2 | 🟢 LOW | Fixed → `logging.warning()` |
| BUG-05 | `scan_ssh.py` | `ProcessPoolExecutor` — paramiko not picklable | 🔴 HIGH | Fixed → `ThreadPoolExecutor` |
| BUG-06 | `scan_nmap.py` | `is_online()` KeyError has no `return False` | 🟡 MED | Fixed → explicit `return False` |
| BUG-07 | `utils.py` | `get_local_ip()` hardcoded `wlan0`, Linux-only | 🟡 MED | Fixed → cross-platform socket method |
| BUG-08 | `config.py` | `yaml.BaseLoader` allows arbitrary objects | 🟡 MED | Fixed → `yaml.SafeLoader` |
| BUG-09 | `penta.py` | `os.system('clear')` | 🟢 LOW | Fixed → `subprocess.run()` |
| BUG-10 | `scan_shodan.py` | Crash on init if `config.yaml` missing | 🟡 MED | Fixed → graceful fallback |

---

## 🚀 Installation

```bash
git clone https://github.com/wavegxz-design/PhantomStrike
cd PhantomStrike
pip install -r requirements.txt
cp config_example.yaml config.yaml
# Fill in your API keys in config.yaml
python penta/phantomstrike.py -vv
```

---

## ⚙️ Configuration

```yaml
# config.yaml — never commit this file
SHODAN_API_KEY: "your_key_here"    # shodan.io
GITHUB_TOKEN:   "your_token_here"  # GitHub API

METASPLOIT:
  MODULE_PATH: "/usr/share/metasploit-framework"
  MSGRPC_PASS: "your_msfrpc_password"

MYSQL:
  USER: "root"
  PASS: "yourpassword"
  HOST: "localhost"
  DB_NAME: "phantomstrike"
```

> `config.yaml` is in `.gitignore` — it will never be committed.

---

## 🖥️ Usage

```bash
# Standard
python penta/phantomstrike.py -vv

# Verbose debug
python penta/phantomstrike.py -vvv

# With proxy
python penta/phantomstrike.py -vv --proxy 127.0.0.1:8080
```

```
  ██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ███╗
  ██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║
  ...

  ╔══ PHANTOMSTRIKE — MAIN MENU ════════════════════╗
  >  [01] IP-based Recon & Attack Modules
     [02] VulnDB — CVE / Exploits / Metasploit
     [00] Exit
```

---

## 📁 Project Structure

```
PhantomStrike/
├── penta/
│   ├── phantomstrike.py      ← Main launcher (rebuilt)
│   ├── config.py             ← Config loader (SafeLoader fix)
│   ├── fetch/                ← CVE / EDB / MSF fetchers
│   ├── lib/
│   │   ├── utils.py          ← Cross-platform utils (fixed)
│   │   ├── menu.py           ← Arrow-key interactive menu
│   │   ├── db.py             ← SQLAlchemy VulnDB
│   │   └── models.py         ← DB models
│   └── modules/
│       ├── scan_nmap.py      ← Nmap scanner (fixed)
│       ├── scan_ssh.py       ← SSH brute force (ThreadPool fix)
│       ├── scan_ftp.py       ← FTP anonymous (NameError fix)
│       ├── scan_dns.py       ← DNS recon (warn fix)
│       ├── scan_shodan.py    ← Shodan intel (graceful init)
│       ├── scan_msf.py       ← Metasploit RPC
│       ├── inspector.py      ← HTTP options checker
│       └── report_vuln.py    ← Vulnerability reporter
├── data/
│   ├── dict/                 ← SSH/FTP wordlists
│   ├── msf/                  ← MSF module DB
│   └── shodan/               ← Shodan queries
├── config_example.yaml       ← Template (copy → config.yaml)
└── requirements.txt
```

---

## 🤝 Contributing

```bash
git checkout -b feat/module-name
git commit -m "feat: [module] — description"
git push origin feat/module-name
```

**Before PR:**
- [ ] No hardcoded API keys
- [ ] No `shell=True` with user input
- [ ] No infinite recursion in menu loops
- [ ] Tested on Linux

---

## ⚠️ Legal Disclaimer

```
For AUTHORIZED security research and penetration testing ONLY.

✅  Authorized engagements (signed scope)
✅  CTF competitions
✅  Bug bounty programs (within scope)
✅  Personal lab environments

❌  Unauthorized scanning or exploitation
❌  Any illegal activity under local or international law

The author assumes NO responsibility for misuse.
```

---

## 👤 Author & Maintainer

<div align="center">

| | |
|:---:|:---|
| <img src="https://github.com/wavegxz-design.png" width="80" style="border-radius:50%"/> | **krypthane** — Red Team Operator & Open Source Developer<br/>📍 Mexico 🇲🇽 UTC-6<br/>*"Know the attack to build the defense."* |

<br/>

[![GitHub](https://img.shields.io/badge/GitHub-wavegxz--design-ff2d2d?style=for-the-badge&logo=github&labelColor=0d1117)](https://github.com/wavegxz-design)
[![Telegram](https://img.shields.io/badge/Telegram-Skrylakk-00cfff?style=for-the-badge&logo=telegram&labelColor=0d1117)](https://t.me/Skrylakk)
[![Email](https://img.shields.io/badge/Email-Workernova@proton.me-ff2d2d?style=for-the-badge&logo=protonmail&labelColor=0d1117)](mailto:Workernova@proton.me)
[![Portfolio](https://img.shields.io/badge/Portfolio-krypthane-ff2d2d?style=for-the-badge&logo=cloudflare&labelColor=0d1117)](https://krypthane.workernova.workers.dev)

</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=ff2d2d&height=120&section=footer&fontColor=ffffff&animation=fadeIn&text=krypthane+%C2%B7+wavegxz-design+%C2%B7+Ethical+Hacking+Only" width="100%"/>

</div>
