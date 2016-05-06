from django.contrib import admin

# Register your models here.
from .models import Page, File, Comment, Hashtag, User, User_page_accessed

admin.site.register(Page)
admin.site.register(File)
admin.site.register(Comment)
admin.site.register(Hashtag)
admin.site.register(User)
admin.site.register(User_page_accessed)
