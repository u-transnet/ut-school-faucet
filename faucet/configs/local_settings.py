from .private_key import *

NOBROADCAST = True  # Safety mode

MIN_IP_AGE = 300  # How long in secs does an IP need to wait to register a new account?
WITNESS_URL = "wss://node.testnet.bitshares.eu" # Url of node for registering

REGISTRAR = "faucet"
DEFAULT_REFERRER = "xeroc"
REFERRER_PERCENT = 50  # in percent

BALANCE_NOTIFY_THRESHOLD = 500  # if balances goes below this, you will be notified
CORE_ASSET = "bts"  # Main asset used for paying fees

PROXY = None
ADDITIONAL_OWNER_ACCOUNTS = []
ADDITIONAL_ACTIVE_ACCOUNTS = []
ADDITIONAL_OWNER_KEYS = []
ADDITIONAL_ACTIVE_KEYS = []
