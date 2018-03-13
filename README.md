# ut-school-faucet

# Предустановки

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


# Базовые конфигурации фасета
Конфигурации фасета находятся в папке /faucet/configs/
1) local_settings - открытые конфигурации; 
2) private_key - файл с WIF ключами, который не публикуется в открытых источниках;
3) test_tokens - файл где располагаются access_token'ы для запуска тестов;
 
 **Содержимое private_key**
 ```
 WIF = "change_me" #  Ключ от учетной записи аккаунта регистратора
 WELCOME_TRANSFER_ACCOUNT_WIF = "change_me" #  Ключ от ученой записи с которой будет начисляться токены за регистрацию
 ```
 
  **Содержимое test_tokens**
 ```
VK_ACCESS_TOKEN = 'change_me'
FACEBOOK_ACCESS_TOKEN = 'change_me'
GOOGLE_ACCESS_TOKEN = 'change_me'
 ```
