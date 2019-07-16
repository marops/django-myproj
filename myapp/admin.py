from django.contrib import admin

from . import models

admin.site.site_header = 'MyProj / MyApp Admin'


class ArticleAdmin(admin.ModelAdmin):
    fields=['headline']
    #inlines = [ArticleInline]
    search_fields = ['headline']

admin.site.register(models.Article,ArticleAdmin)
admin.site.register(models.Reporter)
admin.site.register(models.Author)
admin.site.register(models.Person)
