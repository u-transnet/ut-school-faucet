[![English](https://thumb.ibb.co/jDrVkd/gb.png)](README.md) [![Russian](https://thumb.ibb.co/cjYMrJ/ru.png)](README.ru.md)    

# ut-school-faucet
Фасет для направления ut-school предназначен для регистрации пользователей в приложении ut-school, а так же предоставляет доступ к single page application для данного направления

## Installation
```
python3 create_pip_requirements.py
pip install -r requirements.txt
```

Also we have docker container for this project, just click the image

[![Docker](https://www.docker.com/sites/default/files/horizontal.png)](https://github.com/u-transnet/utschool-dockerfiles)


## Configurations

Перед запуском необходимо определить локальные конфигурации Django-проекта.</br>
**Пример содержимого settings/local.py**
```
from .development import * # Выбор режима запуска проекта development/production

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

```


## Базовые конфигурации фасета
Конфигурации фасета находятся в папке /faucet/configs/
1) local_settings - открытые конфигурации; 
2) test_tokens - файл где располагаются access_token'ы для запуска тестов;
 
 **Содержимое local_settings**
 ```

MIN_IP_AGE = 300  # Как много должно пройти времени, чтобы можно было с данным IP зарегистрировать новый аккаунт
WITNESS_URL = "wss://bitshares.openledger.info/ws"  # URL ноды через которую будет проходить регистрация
WIF = "" #  Ключ от учетной записи аккаунта регистратора

REGISTRAR = "u-tech-faucet"
DEFAULT_REFERRER = "u-tech-faucet"
REFERRER_PERCENT = 50  # в процентах

BALANCE_NOTIFY_THRESHOLD = 500  # если баланс будет ниже это значения, будут появляться сообщения в логах
CORE_ASSET = "BTS"  # Основной актив, который будет использоваться для выплаты комиссии

WELCOME_TRANSFER_ENABLED = True
WELCOME_TRANSFER_ACCOUNT = "u-tech-faucet"  # Имя аккаунта с которого будут начислены вступительные токены
WELCOME_TRANSFER_ASSET = "BTS"  # Актив, который является вступительным токеном
WELCOME_TRANSFER_AMOUNT = 5  # Количество вступительных токенов
WELCOME_TRANSFER_ACCOUNT_WIF = "" #  Ключ от ученой записи с которой будет начисляться токены за регистрацию

PROXY = None
ADDITIONAL_OWNER_ACCOUNTS = []
ADDITIONAL_ACTIVE_ACCOUNTS = []
ADDITIONAL_OWNER_KEYS = []
ADDITIONAL_ACTIVE_KEYS = []
 ```
 
  **Содержимое test_tokens**
 ```
VK_ACCESS_TOKEN = 'change_me'
FACEBOOK_ACCESS_TOKEN = 'change_me'
GOOGLE_ACCESS_TOKEN = 'change_me'
 ```


## Related projects
- [python-utransnet](https://github.com/u-transnet/python-utransnet)

## Contributing
We'd love to have your helping hand on our project! See [CONTRIBUTING.md](CONTRIBUTING.md) for more information on what we're looking for and how to get started.

## License
Project is under the MIT license. See [LICENSE](LICENSE) for more information.