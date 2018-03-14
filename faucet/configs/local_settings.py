import os


def parse_int(value, default):
    try:
        return int(value)
    except ValueError:
        return default


def parse_float(value, default):
    try:
        return float(value)
    except ValueError:
        return default


def parse_array(value, default):
    if not value or ',' not in value:
        return default
    return [part.strip() for part in value.split(',')]


MIN_IP_AGE = parse_int(os.environ.get('MIN_IP_AGE'),
                       300)  # How long in secs does an IP need to wait to register a new account?
WITNESS_URL = os.environ.get('WITNESS_URL') or "wss://bitshares.openledger.info/ws"  # Url of node for registering
WIF = os.environ.get('WIF')

REGISTRAR = os.environ.get("REGISTRAR") or "u-tech-faucet"
DEFAULT_REFERRER = os.environ.get("DEFAULT_REFERRER") or "u-tech-faucet"
REFERRER_PERCENT = parse_int(os.environ.get("REFERRER_PERCENT"), 50)  # in percent

BALANCE_NOTIFY_THRESHOLD = parse_int(os.environ.get("BALANCE_NOTIFY_THRESHOLD"), 500)  # if balances goes below this, you will be notified
CORE_ASSET = os.environ.get("CORE_ASSET") or "BTS"  # Main asset used for paying fees

WELCOME_TRANSFER_ENABLED = (os.environ.get("WELCOME_TRANSFER_ENABLED") or "True").lower() == 'true'
WELCOME_TRANSFER_ACCOUNT = os.environ.get(
    "WELCOME_TRANSFER_ACCOUNT") or "u-tech-faucet"  # Account name from which will be send welcome tokens
WELCOME_TRANSFER_ASSET = os.environ.get("WELCOME_TRANSFER_ASSET") or "BTS"  # Asset which which will be welcome token
WELCOME_TRANSFER_AMOUNT = parse_float(os.environ.get("WELCOME_TRANSFER_AMOUNT"), 5)  # Amount of welcome tokens which will be sent
WELCOME_TRANSFER_ACCOUNT_WIF = os.environ.get("WELCOME_TRANSFER_ACCOUNT_WIF")

PROXY = os.environ.get("PROXY")
ADDITIONAL_OWNER_ACCOUNTS = parse_array(os.environ.get("ADDITIONAL_OWNER_ACCOUNTS"), [])
ADDITIONAL_ACTIVE_ACCOUNTS = parse_array(os.environ.get("ADDITIONAL_ACTIVE_ACCOUNTS"), [])
ADDITIONAL_OWNER_KEYS = parse_array(os.environ.get("ADDITIONAL_OWNER_KEYS"), [])
ADDITIONAL_ACTIVE_KEYS = parse_array(os.environ.get("ADDITIONAL_ACTIVE_KEYS"), [])
