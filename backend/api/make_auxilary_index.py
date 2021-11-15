import api.make_main_index
from api.models import News
import os
from django.conf import settings
from api.index_constructor import index_constructor
def make_auxilary_index(news_ids_list):
    news = News.objects.filter(pk__in=news_ids_list)
    index_constructor(news,os.path.join(settings.BASE_DIR, 'api/indexes', 'aux_index.txt'))
