import json
from bitshares.account import Account as BitsharesAccount
from bitshares import BitShares
import re

from django import views
from django.conf import settings
from django.db import IntegrityError

from faucet.configs import local_settings as configs
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse

from logging import getLogger

from faucet.exceptions import ApiException
from faucet.forms import AddLectureForm
from faucet.models import Lecture, Account
from faucet.social_api import VKApi, FacebookApi, GoogleApi

logger = getLogger(__name__)


def create_api_error(api_exc):
    return JsonResponse({
        "error":
            {
                "code": api_exc.code,
                "msg": str(api_exc)
            }
    }
    )


def catch_api_error(fn):
    def wrapper(*args, **kwargs):
        try:
            resp = fn(*args, **kwargs)
        except ApiException as e:
            logger.exception(str(e))
            resp = create_api_error(e)

        return resp

    return wrapper


class RegisterView(views.View):
    required_pub_keys = ["active_key", "memo_key", "owner_key", "name"]
    api_map = {
        Account.NETWORK_VK: VKApi,
        Account.NETWORK_FACEBOOK: FacebookApi,
        Account.NETWORK_GOOGLE: GoogleApi
    }

    ERROR_INVALID_ACCOUNT_DATA = 100
    ERROR_MISSING_PUBLIC_KEY = 101
    ERROR_INVALID_IP = 102
    ERROR_DUPLICATE_ACCOUNT = 103
    ERROR_INVALID_ACCOUNT_NAME = 104
    ERROR_MISSING_ACCOUNT_TOKEN = 105
    ERROR_SN_FETCH_DATA_ERROR = 106
    ERROR_INTERNAL_BLOCKCHAIN_ERROR = 107
    ERROR_UNKNOWN_REFERRER = 108
    ERROR_UNKNOWN_REGISTRAR = 109

    @catch_api_error
    def post(self, request, social_network):

        if social_network not in self.api_map:
            return HttpResponseBadRequest()

        try:
            json_data = json.loads(request.body)
        except:
            return HttpResponseBadRequest()

        account = self.get_account(json_data)
        ip = self.get_ip(request)

        keys = []
        if configs.WIF:
            keys.append(configs.WIF)

        bitshares = BitShares(
            configs.WITNESS_URL,
            nobroadcast=settings.BLOCKCHAIN_NOBROADCAST,
            keys=keys
        )

        self.validate_account(bitshares, account)
        registrar = self.get_registrar(bitshares, account)
        referrer = self.get_referrer(bitshares, account)

        self.create_account(bitshares, account, registrar['id'], referrer['id'], ip, social_network)

        self.check_registrar_balance(registrar)

        return JsonResponse({"account": {
            "name": account["name"],
            "owner_key": account["owner_key"],
            "active_key": account["active_key"],
            "memo_key": account["memo_key"],
            "referrer": referrer["name"]
        }})

    def get_account(self, json_data):
        if not json_data or 'account' not in json_data or 'name' not in json_data['account']:
            raise ApiException(self.ERROR_INVALID_ACCOUNT_DATA, 'Account data was not provided')
        account = json_data['account']

        for key in self.required_pub_keys:
            if key not in account:
                raise ApiException(self.ERROR_MISSING_PUBLIC_KEY, 'Public key %s was missed' % key)

        return account

    def get_ip(self, request):
        if request.META.get('X-Real-IP'):
            ip = request.META.get('X-Real-IP')
        else:
            ip = request.META.get('REMOTE_ADDR')

        if ip == '127.0.0.1':
            raise ApiException(self.ERROR_INVALID_IP, 'Fake ip was provided')

        if ip != "127.0.0.1" and Account.exists(ip):
            raise ApiException(self.ERROR_DUPLICATE_ACCOUNT, 'Only one account per IP')

        return True

    def validate_account(self, bitshares_instance, account):
        account_name = account['name']
        if (not re.search(r"[0-9-]", account_name) and
                re.search(r"[aeiouy]", account_name)):
            raise ApiException(self.ERROR_INVALID_ACCOUNT_NAME, "Only cheap names allowed!")

        if 'access_token' not in account:
            raise ApiException(self.ERROR_MISSING_ACCOUNT_TOKEN, 'You must provide access_token for that account')

        try:
            BitsharesAccount(account_name, bitshares_instance)
        except:
            pass
        else:
            raise ApiException(self.ERROR_DUPLICATE_ACCOUNT, 'Account %s already exists' % account_name)

    def create_account(self, bitshares_instance, account, registrar_id, referrer_id, ip, social_network):
        try:
            social_network_api = self.api_map[social_network](account['access_token'])
            user_data = social_network_api.get_user_info()
            if not user_data:
                raise Exception()
        except Exception as e:
            raise ApiException(self.ERROR_SN_FETCH_DATA_ERROR, "Can't resolve data from social network")

        try:
            account_instance = Account.objects.create(
                name=account["name"],
                ip=ip,

                authorized_network=social_network,
                uid=user_data['uid'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                photo=user_data['photo']
            )
        except IntegrityError:
            raise ApiException(self.ERROR_DUPLICATE_ACCOUNT,
                               'Account with this %s uid already exists' % user_data['uid'])

        referrer_percent = account.get("referrer_percent", configs.REFERRER_PERCENT)
        try:
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
        except Exception as exc:
            account_instance.delete()
            raise ApiException(self.ERROR_INTERNAL_BLOCKCHAIN_ERROR, 'Error during broadcasting data into blockchain')

        self.send_welcome_tokens(account.name)

    def send_welcome_tokens(self, account_name):
        if not configs.WELCOME_TRANSFER_ENABLED:
            return

        if not configs.WELCOME_TRANSFER_ACCOUNT_WIF:
            logger.critical('WELCOME_TRANSFER_ENABLED but WELCOME_TRANSFER_ACCOUNT_WIF was not passed!'
                            'Check configuration and provide correct wif.')
            return

        bitshares_instance = BitShares(
            configs.WITNESS_URL,
            nobroadcast=settings.BLOCKCHAIN_NOBROADCAST,
            keys=[configs.WELCOME_TRANSFER_ACCOUNT_WIF]
        )

        try:
            bitshares_instance.transfer(
                account_name,
                configs.WELCOME_TRANSFER_AMOUNT,
                configs.WELCOME_TRANSFER_ASSET,
                configs.WELCOME_TRANSFER_ACCOUNT
            )
        except:
            logger.exception("Can't send welcome tokens to %s !!!" % account_name)

    def get_registrar(self, bitshares_instance, account):
        registrar = account.get("registrar") or configs.REGISTRAR
        try:
            return BitsharesAccount(registrar, bitshares_instance=bitshares_instance)
        except:
            raise ApiException(self.ERROR_UNKNOWN_REGISTRAR, "Unknown registrar: %s" % account['registrar'])

    def get_referrer(self, bitshares_instance, account):
        registrar = account.get("referrer") or configs.DEFAULT_REFERRER
        try:
            return BitsharesAccount(registrar, bitshares_instance=bitshares_instance)
        except:
            raise ApiException(self.ERROR_UNKNOWN_REFERRER, "Unknown referrer: %s" % account['referrer'])

    def check_registrar_balance(self, registrar):
        balance = registrar.balance(configs.CORE_ASSET)
        if balance and balance.amount < configs.BALANCE_NOTIFY_THRESHOLD:
            logger.critical(
                "The faucet's balances is below {}".format(
                    configs.BALANCE_NOTIFY_THRESHOLD
                ),
            )


class LectureView(views.View):
    ERROR_SN_FETCHING = 100
    ERROR_SN_HAS_NO_PERMISSION = 101
    ERROR_DUPLICATE_LECTURE = 102
    ERROR_ACCOUNT_DOES_NOT_EXISTS = 103

    @catch_api_error
    def post(self, request):
        form_data = request.POST.dict()
        add_lecture_form = AddLectureForm(form_data)
        if not add_lecture_form.is_valid():
            return HttpResponseBadRequest()

        data = add_lecture_form.cleaned_data
        try:
            api = VKApi(data['access_token'])
            is_admin = api.check_is_topic_admin(data['topic_url'])
        except Exception:
            raise ApiException(self.ERROR_SN_FETCHING, 'Error during fetching data from social network')

        if not is_admin:
            raise ApiException(self.ERROR_SN_HAS_NO_PERMISSION,
                               'You have no permission for performing this operation.'
                               ' You must be admin of that group')

        try:
            Lecture.objects.create(
                name=data['name'],
                topic_id=add_lecture_form.get_topic_id()
            )
        except IntegrityError as e:
            logger.error(
                'Account with topic_id %s - already exists'
                % (data['topic_id'])
            )
            raise ApiException(self.ERROR_DUPLICATE_LECTURE,
                               'Account with topic_id %s - already exists' % data['topic_id'])

        return HttpResponse()
