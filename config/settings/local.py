from .base import *

SECRET_KEY = env('DJANGO_SECRET_KEY', default='!msi1!ep5$+8bh#5r@6zy$jv2f=t^ekyn$3@7$sgj##tz14^s6')

DEBUG = env.bool('DJANGO_DEBUG', default=True)

MEDIA_ROOT = str(APPS_DIR('media'))
