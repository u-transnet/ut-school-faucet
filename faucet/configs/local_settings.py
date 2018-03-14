import os

MIN_IP_AGE = os.environ.get('MIN_IP_AGE', 300)  # How long in secs does an IP need to wait to register a new account?
WITNESS_URL = os.environ.get('WITNESS_URL',"wss://bitshares.openledger.info/ws")  # Url of node for registering
WIF = os.environ.get('WIF')

REGISTRAR = os.environ.get("REGISTRAR", "u-tech-faucet")
DEFAULT_REFERRER = os.environ.get("DEFAULT_REFERRER", "u-tech-faucet")
REFERRER_PERCENT = os.environ.get("REFERRER_PERCENT", 50)  # in percent

BALANCE_NOTIFY_THRESHOLD = os.environ.get("BALANCE_NOTIFY_THRESHOLD", 500)  # if balances goes below this, you will be notified
CORE_ASSET = os.environ.get("CORE_ASSET", "BTS")  # Main asset used for paying fees

WELCOME_TRANSFER_ENABLED = os.environ.get("WELCOME_TRANSFER_ENABLED", True)
WELCOME_TRANSFER_ACCOUNT = os.environ.get("WELCOME_TRANSFER_ACCOUNT", "u-tech-faucet")  # Account name from which will be send welcome tokens
WELCOME_TRANSFER_ASSET = os.environ.get("WELCOME_TRANSFER_ASSET", "BTS")  # Asset which which will be welcome token
WELCOME_TRANSFER_AMOUNT = os.environ.get("WELCOME_TRANSFER_AMOUNT", 5)  # Amount of welcome tokens which will be sent
WELCOME_TRANSFER_ACCOUNT_WIF = os.environ.get("WELCOME_TRANSFER_ACCOUNT_WIF", "")

PROXY = os.environ.get("PROXY", None)
ADDITIONAL_OWNER_ACCOUNTS = os.environ.get("ADDITIONAL_OWNER_ACCOUNTS", '').split(',')
ADDITIONAL_ACTIVE_ACCOUNTS = os.environ.get("ADDITIONAL_ACTIVE_ACCOUNTS", '').split(',')
ADDITIONAL_OWNER_KEYS = os.environ.get("ADDITIONAL_OWNER_KEYS", '').split(',')
ADDITIONAL_ACTIVE_KEYS = os.environ.get("ADDITIONAL_ACTIVE_KEYS", '').split(',')