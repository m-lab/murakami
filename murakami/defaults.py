"""
Common default values for Murakami.
"""
SSH_PORT = 22
SSH_TIMEOUT = 5
HTTP_PORT = 80
TESTS_PER_DAY = 4
EXPORT_PATH = "/var/cache/murakami"
DYNAMIC_FILE = "/var/lib/murakami/config.json"
CONFIG_FILES = [
    "/etc/murakami/murakami.toml", "~/.config/murakami/murakami.toml"
]
