import django
import os
import re

import api

os.environ['DJANGO_SETTINGS_MODULE'] = 'Arman_varzesh_backend.settings'
django.setup()

from api.models import News
from api import signals
from django.conf import settings
from api.index_constructor import index_constructor



def make_main_index():
    news = News.objects.all()
    index_constructor(news,os.path.join(settings.BASE_DIR, 'api/indexes', 'main_index.txt'))
    signals.new_docs = []
    with open(os.path.join(settings.BASE_DIR, 'api/indexes/aux_index.txt'), 'w', encoding="utf-8") as writer:
        writer.write('')

make_main_index()

