from django.contrib import admin
from .models import Category, Post

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

admin.site.register(Post)
admin.site.register(Category, CategoryAdmin)