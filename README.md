# ut-school-faucet

# Установка

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
