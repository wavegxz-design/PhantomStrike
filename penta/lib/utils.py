#!/usr/bin/env python3
"""
PhantomStrike — utils.py
FIX [BUG-04]: logging.warn() -> logging.warning() (deprecated since Python 3.2)
FIX [BUG-07]: get_local_ip() hardcoded 'wlan0' + no Windows -> auto-detect
"""
import codecs
import json
import logging
import mimetypes
import pathlib
import platform
import random
import re
import socket
import sys

SYSTEMOS = platform.system()

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/605.1.15 Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
]


class Colors:
    BLACK        = "\033[30m"
    RED          = "\033[31m"
    GREEN        = "\033[32m"
    YELLOW       = "\033[33m"
    BLUE         = "\033[34m"
    DARKGRAY     = "\033[90m"
    PURPLE       = "\033[35m"
    CYAN         = "\033[36m"
    LIGHTMAGENTA = "\033[95m"
    LIGHTBLUE    = "\033[94m"
    LIGHTYELLOW  = "\033[93m"
    LIGHTGREEN   = "\033[92m"
    LIGHTRED     = "\033[91m"
    LIGHTCYAN    = "\033[96m"
    LIGHTGRAY    = "\033[37m"
    BG_WHITE     = "\033[7m"
    BG_RED       = "\033[41m"
    BG_GREEN     = "\033[42m"
    BG_YELLOW    = "\033[43m"
    BOLD         = "\033[1m"
    UNDERLINE    = "\033[4m"
    END          = "\033[0m"


class ColorfulHandler(logging.StreamHandler):
    _levels = {
        "DEBUG":    "\033[90mDEBUG\033[0m",
        "INFO":     "\033[32mINFO\033[0m",
        "WARNING":  "\033[33mWARNING\033[0m",
        "ERROR":    "\033[31mERROR\033[0m",
        "CRITICAL": "\033[41mCRITICAL\033[0m",
    }
    def emit(self, record):
        record.levelname = self._levels.get(record.levelname, record.levelname)
        super().emit(record)


def save_logfile(filename, content):
    base = pathlib.Path(__file__).parent.parent
    log_dir = base / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / filename
    with log_file.open("w") as f:
        mime = mimetypes.guess_type(filename)[0]
        if mime == "application/json":
            json.dump(content, f)
        else:
            f.write(content)


def system_exit():
    from lib.menu import Menu
    menu = Menu(False)
    choice = menu.show("\n[?] Exit PhantomStrike?", ["[Return to menu]", "[Exit]"])
    if choice in (-1, 1):
        logging.info("PhantomStrike exiting. Stay ethical.")
        sys.exit(0)


def get_version(inc_version, exc_version):
    if inc_version and inc_version != "*":
        return inc_version
    return exc_version


def get_random_user_agent():
    return random.choice(USER_AGENTS)


def get_val(elements):
    if len(elements) == 1:
        try:
            return elements[0].strip()
        except Exception:
            return ""
    elif len(elements) > 1:
        return ",".join(elements)
    return ""


def get_val_deal(element, key_name):
    try:
        return element[key_name]
    except (KeyError, TypeError):
        return ""


def get_local_ip(interface=None):
    """
    FIX [BUG-07]: Cross-platform local IP detection.
    Old code used hardcoded wlan0 via fcntl (Linux-only, breaks on eth0/ens33).
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        pass
    try:
        candidates = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                      if not ip.startswith("127.")]
        if candidates:
            return candidates[0]
    except Exception:
        pass
    logging.error("Could not detect local IP address.")
    return "127.0.0.1"


def is_url(url):
    pattern = (r"^(https?://)?(([a-zA-Z0-9_-]+\.)+[a-zA-Z]{2,}"
               r"|(\d{1,3}\.){3}\d{1,3}|localhost)(:[1-9][0-9]*)?(\/.*)?$")
    return bool(re.search(pattern, url))


def decode_utf_8_text(text):
    try:
        return codecs.decode(text, "utf-8")
    except (TypeError, ValueError):
        return text


def encode_utf_8_text(text):
    try:
        return codecs.encode(text, "utf-8", "ignore")
    except (TypeError, ValueError):
        return text
