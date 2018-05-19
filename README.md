[![English](https://thumb.ibb.co/jDrVkd/gb.png)](README.md) [![Russian](https://thumb.ibb.co/cjYMrJ/ru.png)](README.ru.md)    

# ut-school-faucet
Фасет для направления ut-school предназначен для регистрации пользователей в приложении ut-school, а так же предоставляет доступ к single page application для данного направления

## Installation

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


## Related projects
- [python-utransnet](https://github.com/u-transnet/python-utransnet)

## Contributing
We'd love to have your helping hand on our project! See [CONTRIBUTING.md](CONTRIBUTING.md) for more information on what we're looking for and how to get started.

## License
Project is under the MIT license. See [LICENSE](LICENSE) for more information.
