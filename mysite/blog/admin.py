# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import Article, Person


class ArticleAdmin(admin.ModelAdmin):

    search_fields = ['title', 'content']        # 搜索功能：这样就可以按照 标题或内容搜索了
    list_filter = ('author',)                   # 筛选功能：这样就可以根据文章的状态去筛选，比如找出是草稿的文章
    list_display = ['title', 'pub_date', 'update_time']

    # 3.修改保存时的一些操作，可以检查用户，保存的内容等，比如保存时加上添加人
    def save_model(self, request, obj, form, change):
        if change:  # 更改的时候
            obj_original = self.model.objects.get(pk=obj.pk)    # 如果需要获取修改前的对象的内容可以用
        else:       # 新增的时候
            obj_original = None
        obj.user = request.user
        obj.save()
    # 其中obj是修改后的对象，form是返回的表单（修改后的），当新建一个对象时change = False, 当修改一个对象时change = True
    # 那么又有问题了，这里如果原来的obj不存在，也就是如果我们是新建的一个怎么办呢，这时候可以用try, except的方法尝试获取,
    # 当然更好的方法是判断一下这个对象是新建还是修改，是新建就没有 obj_original，是修改就有

    # 4, 删除时做一些处理,
    def delete_model(self, request, obj):
        """
        Given a model instance delete it from the database.
        """
        # handle something here
        obj.delete()

    # Django的后台非常强大，这个只是帮助大家入门，更完整的还需要查看官方文档，如果你有更好的方法或不懂的问题，欢迎评论！



# 1.定制加载的列表, 根据不同的人显示不同的内容列表，比如输入员只能看见自己输入的，审核员能看到所有的草稿，
# 这时候就需要重写get_queryset方法
class MyModelAdmin(admin.ModelAdmin):
    # 该类实现的功能是如果是超级管理员就列出所有的，如果不是，就仅列出访问者自己相关的
    def get_queryset(self, request):
        qs = super(MyModelAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(author=request.user)

# 2.定制搜索功能（django1.6及以上才有)

class PersonAdmin(admin.ModelAdmin):

    list_display = ['full_name']
    search_fields = ['first_name']

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(PersonAdmin, self).get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(age=search_term_as_int)
        except:
            pass
        return queryset, use_distinct
# queryset是默认的结果，search_term是在后台搜索的关键词


# Register your models here.
admin.site.register(Article, ArticleAdmin)
admin.site.register(Person, PersonAdmin)
# list_display 就是来配置要显示的字段的，当然也可以显示非字段内容，或者字段相关的内容，比如：