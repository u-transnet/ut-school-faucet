from .production import *
import django_heroku
django_heroku.settings(locals())

TIME_ZONE = os.environ.get("TIME_ZONE", "UTC")
LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", "en-us")