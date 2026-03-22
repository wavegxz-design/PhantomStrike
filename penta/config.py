#!/usr/bin/env python3
"""
PhantomStrike — config.py
FIX [BUG-08]: yaml.BaseLoader → yaml.SafeLoader (prevents arbitrary object execution)
"""
import inspect
import logging
import os
import re

import yaml

# ── REGEX ────────────────────────────────────────────────────────────
CPE_REGEX = re.compile(
    r"cpe:?:[^:]+:[^:]+:(?P<vendor>[^:]+):(?P<package>[^:]+):(?P<version>[^:]+)"
)
IPV4_REGEX = re.compile(
    r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}"
    r"(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
)
DOMAIN_REGEX = re.compile(
    r"^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*"
    r"([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
)

# ── EXTERNAL URLS ────────────────────────────────────────────────────
GH_URL         = "https://api.github.com/graphql"
NPM_URL        = "https://registry.npmjs.org/-/npm/v1/security/audits"
NVD_URL        = "https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-%(year)s.json.gz"
CHUNK_SIZE     = 128
EDB_CSV_URL    = "https://raw.githubusercontent.com/offensive-security/exploitdb/master/files_exploits.csv"
EDB_MAP_URL    = "https://raw.githubusercontent.com/andreafioraldi/cve_searchsploit/master/cve_searchsploit/exploitdb_mapping.json"
MSF_URL        = "https://www.rapid7.com/db/modules"
MSF_MODULE_DEFAULT   = ["exploits", "auxiliary"]
MSF_FETCH_PAGE_LIMIT = 10


class FileConfig:
    def __init__(self, path=None):
        self.PENTA_HOME = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        self.PENTA      = os.path.dirname(self.PENTA_HOME)
        self.settings   = {}

        self.path = path if path else os.path.join(self.PENTA, "config.yaml")

    def load_yaml(self) -> None:
        """
        FIX [BUG-08]: Use SafeLoader — BaseLoader allows arbitrary Python object construction.
        FIX [BUG-10]: Return gracefully if config.yaml is missing (was crashing on __init__).
        """
        if not os.path.isfile(self.path):
            logging.warning(
                "config.yaml not found. Copy config_example.yaml → config.yaml "
                "and fill in your API keys. Shodan and Metasploit modules will be disabled."
            )
            self.settings = {}
            return

        try:
            with open(self.path, "r") as cfg:
                loaded = yaml.load(cfg, Loader=yaml.SafeLoader)  # FIX: SafeLoader
                self.settings = loaded if loaded else {}
        except IOError as e:
            logging.error(f"Unable to read config file: {e}")
        except yaml.YAMLError as e:
            logging.error(f"Invalid YAML in config file: {e}")

    def get(self, key: str, default=None):
        """Safe key access with default fallback."""
        return self.settings.get(key, default)
