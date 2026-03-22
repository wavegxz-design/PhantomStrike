#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════════╗
# ║   PhantomStrike — Red Team Recon & Pentest Framework           ║
# ║   Maintained by : krypthane | wavegxz-design                   ║
# ║   GitHub        : github.com/wavegxz-design                    ║
# ║   Telegram      : t.me/Skrylakk                                ║
# ║   Email         : Workernova@proton.me                         ║
# ║   Location      : Mexico 🇲🇽 UTC-6                             ║
# ║                                                                 ║
# ║   Bugs fixed v1.0 (krypthane):                                 ║
# ║   [BUG-01] scan_ftp.py: self.nmsc → self.nm (NameError crash)  ║
# ║   [BUG-02] penta.py: str.strip() → str.replace() URL parsing   ║
# ║   [BUG-03] ip_menu/report_menu: infinite recursion → loop      ║
# ║   [BUG-04] logging.warn() → logging.warning() (deprecated)     ║
# ║   [BUG-05] scan_ssh: ProcessPoolExecutor → ThreadPoolExecutor  ║
# ║   [BUG-06] is_online(): missing return False in KeyError        ║
# ║   [BUG-07] get_local_ip(): hardcoded wlan0 + no Windows guard  ║
# ║   [BUG-08] yaml.BaseLoader → yaml.SafeLoader (security)        ║
# ║   [BUG-09] os.system('clear') → subprocess                     ║
# ║   [BUG-10] shodan init: crash if config.yaml missing           ║
# ║                                                                 ║
# ║   Authorized use only. Ethical hacking only.                   ║
# ╚══════════════════════════════════════════════════════════════════╝

import argparse
import logging
import os
import readline  # noqa: F401
import socket
import subprocess
import sys
import time

import config
import fetch
import lib
from lib.menu import Menu
from lib.utils import ColorfulHandler, Colors, system_exit
import modules


hostname = None
ip       = None

# ── COLORS ──────────────────────────────────────────────────────────
R  = "\033[38;5;196m"
RD = "\033[38;5;160m"
G  = "\033[38;5;46m"
GD = "\033[38;5;34m"
CY = "\033[38;5;51m"
WH = "\033[1;97m"
DM = "\033[38;5;240m"
YL = "\033[38;5;226m"
BL = "\033[38;5;27m"
RS = "\033[0m"


def logo():
    # FIX [BUG-09]: subprocess instead of os.system
    try:
        subprocess.run(["clear"], check=False)
    except Exception:
        pass

    print(f"""
{R}  ██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ███╗
{R}  ██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║
{RD}  ██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║
{RD}  ██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║
{R}  ██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║
{R}  ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝
{DM}  ╔══════════════════════════════════════════════════════════════╗
{DM}  ║{R}  ███████╗████████╗██████╗ ██╗██╗  ██╗███████╗              {DM}║
{DM}  ║{R}  ██╔════╝╚══██╔══╝██╔══██╗██║██║ ██╔╝██╔════╝              {DM}║
{DM}  ║{RD}  ███████╗   ██║   ██████╔╝██║█████╔╝ █████╗                {DM}║
{DM}  ║{RD}  ╚════██║   ██║   ██╔══██╗██║██╔═██╗ ██╔══╝                {DM}║
{DM}  ║{R}  ███████║   ██║   ██║  ██║██║██║  ██╗███████╗              {DM}║
{DM}  ║{R}  ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝              {DM}║
{DM}  ╚══════════════════════════════════════════════════════════════╝{RS}
{DM}  ┌──────────────────────────────────────────────────────────────┐
{DM}  │{WH}  Red Team Recon & Pentest Framework  {DM}│{YL}  v1.0             {DM}│
{DM}  ├──────────────────────────────────────────────────────────────┤
{DM}  │{WH}  Author    : {G}krypthane{DM} · wavegxz-design                    {DM}│
{DM}  │{WH}  GitHub    : {CY}github.com/wavegxz-design                     {DM}│
{DM}  │{WH}  Telegram  : {CY}t.me/Skrylakk                                 {DM}│
{DM}  │{R}  ⚠ Authorized use only — Ethical hacking only             {DM}│
{DM}  └──────────────────────────────────────────────────────────────┘{RS}
""")
    time.sleep(0.3)


def main_menu_list():
    menu = Menu(False)
    title = f"{R}  ╔══ PHANTOMSTRIKE — MAIN MENU ═══════════════════════════════╗{RS}"
    menu_list = [
        f'{WH}[01]{RS} IP-based Recon & Attack Modules',
        f'{WH}[02]{RS} VulnDB — CVE / Exploits / Metasploit',
        f'{R}[00]{RS} Exit'
    ]
    return menu.show(title, menu_list)


def ip_menu_list():
    menu = Menu(False)
    title = f"{R}  ╔══ RED TEAM MODULE LIST ═════════════════════════════════════╗{RS}"
    menu_list = [
        f'{WH}[01]{RS} Port Scan                 {DM}→ TCP range scan',
        f'{WH}[02]{RS} Nmap Deep Scan            {DM}→ Service detect + vuln scripts',
        f'{WH}[03]{RS} HTTP Options Check        {DM}→ Methods audit (PUT/DELETE/TRACE)',
        f'{WH}[04]{RS} DNS Reconnaissance        {DM}→ WHOIS + records (A/MX/NS/TXT...)',
        f'{WH}[05]{RS} Shodan Intelligence       {DM}→ Host info + CVE lookup',
        f'{WH}[06]{RS} FTP Anonymous Access      {DM}→ Anonymous login test',
        f'{WH}[07]{RS} SSH Brute Force           {DM}→ Credential attack (authorized only)',
        f'{WH}[08]{RS} Metasploit RPC            {DM}→ Module execution via MSGRPC',
        f'{WH}[09]{RS} Change Target             {DM}→ Set new IP/hostname',
        f'{R}[00]{RS} Return to Main Menu',
    ]
    return menu.show(title, menu_list)


def report_menu_list():
    menu = Menu(False)
    title = f"{R}  ╔══ VULNDB MENU ══════════════════════════════════════════════╗{RS}"
    menu_list = [
        f'{WH}[01]{RS} Daily Report              {DM}→ CVE + EDB + MSF combined',
        f'{WH}[02]{RS} View Report               {DM}→ Show saved reports',
        f'{WH}[03]{RS} Fetch CVEs                {DM}→ Download NVD feed',
        f'{WH}[04]{RS} Fetch Exploits            {DM}→ Update ExploitDB index',
        f'{WH}[05]{RS} Fetch MSF Modules         {DM}→ Sync Metasploit module list',
        f'{WH}[06]{RS} Database Menu             {DM}→ Query local VulnDB',
        f'{R}[00]{RS} Return to Main Menu',
    ]
    return menu.show(title, menu_list)


def initialize_variable(options):
    """Resolve target hostname and IP."""
    global hostname, ip
    result = get_ip()
    if result is not None:
        hostname, ip = result


def get_ip():
    """
    FIX [BUG-02]: str.strip('http://') was removing individual characters,
    not the full prefix string. Now uses str.removeprefix() / replace().
    """
    while True:
        try:
            addr = input(f"\n{R}  [?]{RS}{WH} Target IP or hostname: {RS}").strip()
        except KeyboardInterrupt:
            system_exit()
            return None

        # FIX: proper prefix removal
        for prefix in ("https://", "http://"):
            if addr.startswith(prefix):
                addr = addr[len(prefix):]
                break
        addr = addr.split("/")[0]  # strip any path

        if config.IPV4_REGEX.match(addr) or config.DOMAIN_REGEX.match(addr):
            hostname_local = addr
            print(f"{DM}  [*] Resolving {addr}...{RS}")
            try:
                ip_local = socket.gethostbyname(hostname_local)
                print(f'{G}  [+] {hostname_local} → {ip_local}{RS}\n')
                return [hostname_local, ip_local]
            except Exception as e:
                logging.error(f"  [!] Resolution failed: {e}")
                continue
        else:
            print(f"{R}  [!] Invalid input. Use an IPv4 address or domain name.{RS}")
            continue


# FIX [BUG-03]: ip_menu and report_menu used recursion for looping.
# Replaced with explicit while loops to prevent stack overflow on long sessions.
def ip_menu(options):
    global hostname, ip

    if hostname is None:
        initialize_variable(options)

    checker     = modules.Inspect()
    nmap_scan   = modules.NmapScanner()
    dns_scan    = modules.DnsScanner()
    shodan_srch = modules.ShodanSearch()
    ftp_access  = modules.FtpConnector()
    ssh_access  = modules.SshConnector()
    msf_rpc     = modules.MetaSploitRPC()

    while True:
        print(f"\n{DM}  Target → {G}{hostname}{DM} ({ip}){RS}")
        num_menu = ip_menu_list()

        if num_menu is None:
            print(f"{R}  [!] Incorrect choice{RS}")
            continue
        if num_menu == -1 or num_menu == 9:
            break
        elif num_menu == 0:
            nmap_scan.port_scan(ip)
        elif num_menu == 1:
            nmap_scan.menu(ip)
        elif num_menu == 2:
            checker.check_option_methods(hostname)
        elif num_menu == 3:
            dns_scan.scan(ip, hostname)
        elif num_menu == 4:
            shodan_srch.shodan_ip_to_service(ip)
        elif num_menu == 5:
            ftp_access.ftp_connect_anonymous(ip)
        elif num_menu == 6:
            ssh_access.ssh_connect(ip)
        elif num_menu == 7:
            msf_rpc.scan(ip)
        elif num_menu == 8:
            initialize_variable(options)


def report_menu(options):
    nvd    = fetch.NvdCveCollector()
    msf    = fetch.MsfSelector()
    edb    = fetch.EdbSelector()
    report = modules.DailyReportor()

    while True:
        num_menu = report_menu_list()

        if num_menu is None:
            print(f"{R}  [!] Incorrect choice{RS}")
            continue
        if num_menu == -1 or num_menu == 6:
            break
        elif num_menu == 0:
            report.fetch_report()
        elif num_menu == 1:
            report.view_report()
        elif num_menu == 2:
            nvd.download()
        elif num_menu == 3:
            edb.update()
        elif num_menu == 4:
            msf.update()
        elif num_menu == 5:
            lib.db_menu()


def main_menu(options):
    while True:
        menu_num = main_menu_list()
        if menu_num is None:
            print(f"{R}  [!] Incorrect choice{RS}")
            continue
        if menu_num == 0:
            ip_menu(options)
        elif menu_num == 1:
            report_menu(options)
        elif menu_num == -1 or menu_num == 2:
            logging.info("PhantomStrike exiting. Stay ethical.")
            sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description='PhantomStrike — Red Team Recon & Pentest Framework')
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Verbosity level (-v, -vv, -vvv)")
    parser.add_argument("--proxy", help="Proxy [IP:PORT]")
    options = parser.parse_args()

    loglevel = {0: logging.ERROR, 1: logging.WARN, 2: logging.INFO, 3: logging.DEBUG}.get(
        options.verbose, logging.DEBUG
    )

    logging.basicConfig(
        handlers=[ColorfulHandler()],
        level=loglevel,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    if options.verbose < 3:
        logging.getLogger().setLevel(loglevel)

    logo()
    main_menu(options)


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise SystemExit("[!] Python 3 required. Run with python3 phantomstrike.py")
    main()
