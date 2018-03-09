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

# Получение access_token'ов
Сначала необходимо авторизоваться в выбранной социальной сети.

**Facebook**
1) Перейти по [этой ссылке](https://developers.facebook.com/tools/explorer);
2) Скопировать значение поля "Марке доступа";

**Google**
1) Перейти по [ссылке](https://developers.google.com/oauthplayground/)
2) В step 1 выбрать "Google+ API v1" и отметить "https://www.googleapis.com/auth/plus.me";
3) Нажать кнопку "Authorize APIs" и пройти авторизацию;
4) В step 2 нажать кнопку "Exchange authorization code for tokens";
5) Скопировать значение поля "Access token";

**VK**
1) Перейти по ссылке
https://oauth.vk.com/authorize?client_id=4979907&scope=photos,groups,email&response_type=token;
2) Пройти авторизацию;
3) Скопировать значение get-параметра "access_token" из адресной строки;
