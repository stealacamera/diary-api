from django.contrib import admin
from .models import Folder, Tag, Entry

admin.site.register(Folder)
admin.site.register(Tag)
admin.site.register(Entry)