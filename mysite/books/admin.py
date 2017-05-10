# -*- encoding: utf-8 -*-
from django.contrib import admin
from books.models import Publisher, Author, Book
# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name')


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'publication_date')
    list_filter = ('publication_date',)
    # date_hierarchy = 'publication_date'
    ordering = ('-publication_date',)
    # fields = ('title', 'authors', 'publisher', 'publication_date')
    # 这样，在编辑页面就无法对publication date进行改动。
    # fields = ('title', 'authors', 'publisher')
    # filter_horizontal和filter_vertical选项只能用在多对多字段上, 而不能用于ForeignKey字段
    # filter_horizontal = ('authors',) # 水平显示
    filter_vertical = ('authors',) # 垂直显示
    raw_id_fields = ('publisher',) # publisher的数据库ID号。


admin.site.register(Publisher)
# admin.site.register(Author)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)

# 用户、用户组和权限
# 因为你是用超级用户登录的，你可以创建，编辑和删除任何对像。