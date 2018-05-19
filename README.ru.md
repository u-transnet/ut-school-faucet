[![English](https://thumb.ibb.co/jDrVkd/gb.png)](README.md) [![Russian](https://thumb.ibb.co/cjYMrJ/ru.png)](README.ru.md)    

# ut-school-faucet
Фасет для направления ut-school предназначен для регистрации пользователей в приложении ut-school, а так же предоставляет доступ к single page application для данного направления

## Установка
Авторизуйтесь на heroku
```
heroku login
```

Добавьт текущее приложение на heroku
```
heroku git:remote -a <application_name>
```

Активируйте postgres add-on
```
heroku addons:create heroku-postgresql:hobby-dev
```

Задеплойте ветку heroku в master ветку приложения
```
git push heroku heroku:master
```

## Связанные проекты
- [python-utransnet](https://github.com/u-transnet/python-utransnet)

## Сотрудничество
Мы будем рады вашей помощи в развитии проекта! Откройте [CONTRIBUTING.ru.md](CONTRIBUTING.ru.md) для того, чтобы узнать чем Вы можете поможете помочь проекту и как присоединиться

## Лицензия
Проект использует MIT лицензию. Откройте [LICENSE](LICENSE) для подробностей
