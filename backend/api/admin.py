from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

class AuthorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Player, AuthorAdmin)
admin.site.register(Team, AuthorAdmin)
admin.site.register(News, AuthorAdmin)
admin.site.register(RegisteredUser, AuthorAdmin)
admin.site.register(Video, AuthorAdmin)
admin.site.register(Match, AuthorAdmin)
admin.site.register(League, AuthorAdmin)
admin.site.register(RssLinks, AuthorAdmin)