import json
from bitshares.account import Account
from bitshares import BitShares
import re

from django import views
from faucet.configs import local_settings as configs
from django.http import HttpResponseBadRequest, JsonResponse

from logging import getLogger

from faucet import models

logger = getLogger(__name__)


class RegisterView(views.View):
    required_pub_keys = ["active_key", "memo_key", "owner_key", "name"]

    def post(self, request, referrer=None):

        try:
            account = self.get_account(request)
        except Exception as exc:
            logger.exception("During registration exception was occurred")
            return HttpResponseBadRequest()

        try:
            ip = self.get_ip(request)
        except Exception as exc:
            return self.api_error(str(exc))

        bitshares = BitShares(
            configs.WITNESS_URL,
            nobroadcast=configs.NOBROADCAST,
            keys=[configs.WIF]
        )

        try:
            self.validate_account(bitshares, account)
            registrar = self.get_registrar(bitshares, account)
            referrer = self.get_referrer(bitshares, account)
        except Exception as exc:
            return self.api_error(str(exc))

        try:
            self.create_account(bitshares, account, registrar['id'], referrer['id'], ip)
        except Exception as e:
            logger.exception('During creating account exception was occurred')
            return self.api_error(str(e))

        self.check_registrar_balance(registrar)

        return JsonResponse({"account": {
            "name": account["name"],
            "owner_key": account["owner_key"],
            "active_key": account["active_key"],
            "memo_key": account["memo_key"],
            "referrer": referrer["name"]
        }})

    def api_error(self, msg):
        return JsonResponse({"error": {"base": [msg]}})

    def get_account(self, request):
        json_data = json.loads(request.body)

        if not json_data or 'account' not in json_data or 'name' not in json_data['account']:
            raise Exception('Invalid request data')
        account = json_data['account']

        for key in self.required_pub_keys:
            if key not in account:
                raise Exception('Public key %s was missed' % key)

        return account

    def get_ip(self, request):
        if request.META.get('X-Real-IP'):
            ip = request.META.get('X-Real-IP')
        else:
            ip = request.META.get('REMOTE_ADDR')

        if ip != "127.0.0.1" and models.Account.exists(ip):
            raise Exception('Only one account per IP')

        return True

    def validate_account(self, bitshares_instance, account):
        account_name = account['name']
        if (not re.search(r"[0-9-]", account_name) and
                re.search(r"[aeiouy]", account_name)):
            raise Exception("Only cheap names allowed!")

        try:
            Account(account_name, bitshares_instance)
        except:
            pass
        else:
            raise Exception('Account %s already exists' % account_name)

    def create_account(self, bitshares_instance, account, registrar_id, referrer_id, ip):
        referrer_percent = account.get("referrer_percent", configs.REFERRER_PERCENT)
        bitshares_instance.create_account(
            account["name"],
            registrar=registrar_id,
            referrer=referrer_id,
            referrer_percent=referrer_percent,
            owner_key=account["owner_key"],
            active_key=account["active_key"],
            memo_key=account["memo_key"],
            proxy_account=configs.PROXY,
            additional_owner_accounts=configs.ADDITIONAL_OWNER_ACCOUNTS,
            additional_active_accounts=configs.ADDITIONAL_ACTIVE_ACCOUNTS,
            additional_owner_keys=configs.ADDITIONAL_OWNER_KEYS,
            additional_active_keys=configs.ADDITIONAL_ACTIVE_KEYS
        )

        models.Account.objects.create(
            name=account["name"],
            ip=ip
        )

    def get_registrar(self, bitshares_instance, account):
        registrar = account.get("registrar") or configs.REGISTRAR
        try:
            return Account(registrar, bitshares_instance=bitshares_instance)
        except:
            raise Exception("Unknown registrar: %s" % account['registrar'])

    def get_referrer(self, bitshares_instance, account):
        registrar = account.get("referrer") or configs.DEFAULT_REFERRER
        try:
            return Account(registrar, bitshares_instance=bitshares_instance)
        except:
            raise Exception("Unknown referrer: %s" % account['referrer'])

    def check_registrar_balance(self, registrar):
        balance = registrar.balance(configs.CORE_ASSET)
        if balance and balance.amount < configs.BALANCE_NOTIFY_THRESHOLD:
            logger.critical(
                "The faucet's balances is below {}".format(
                    configs.BALANCE_NOTIFY_THRESHOLD
                ),
            )
