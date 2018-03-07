from .private_key import *

MIN_IP_AGE = 300  # How long in secs does an IP need to wait to register a new account?
WITNESS_URL = "wss://transnet.tech:10443/ws"  # Url of node for registering

REGISTRAR = "u-tech-faucet"
DEFAULT_REFERRER = "u-tech-faucet"
REFERRER_PERCENT = 50  # in percent

BALANCE_NOTIFY_THRESHOLD = 500  # if balances goes below this, you will be notified
CORE_ASSET = "bts"  # Main asset used for paying fees

WELCOME_TRANSFER_ENABLED = True
WELCOME_TRANSFER_ACCOUNT = "u-tech-faucet"  # Account name from which will be send welcome tokens
WELCOME_TRANSFER_ASSET = "bts"  # Asset which which will be welcome token
WELCOME_TRANSFER_AMOUNT = 5  # Amount of welcome tokens whice will be sended

PROXY = None
ADDITIONAL_OWNER_ACCOUNTS = []
ADDITIONAL_ACTIVE_ACCOUNTS = []
ADDITIONAL_OWNER_KEYS = []
ADDITIONAL_ACTIVE_KEYS = []
