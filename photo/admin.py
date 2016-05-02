# coding: utf-8

from django.contrib import admin

from photo.models import Photo,Nodeset,NewsData

#from .models import Nodeset, Network,NewsData, Keyword, Links,Publisher, Author, Book


admin.site.register(Nodeset)
admin.site.register(Photo)
admin.site.register(NewsData)


