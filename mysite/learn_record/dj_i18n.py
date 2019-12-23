#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time: 2019/12/19 22:49

# Django 国际化
# Django 支持国际化，多语言。Django的国际化是默认开启的，如果您不需要国际化支持，那么您可以在您的设置文件中设置 USE_I18N = False，那么Django会进行一些优化，不加载国际化支持机制。
# NOTE: 18表示Internationalization这个单词首字母I和结尾字母N之间的字母有18个。I18N就是Internationalization（国际化）的意思。

# Django 完全支持文本翻译，日期时间数字格式和时区。
# 本质上讲，Django做了两件事：
# 它允许开发者指定要翻译的字符串
# Django根据特定的访问者的偏好设置 进行调用相应的翻译文本。
# 一，开启国际化的支持，需要在settings.py文件中设置
# MIDDLEWARE_CLASSES = (
#     'django.middleware.locale.LocaleMiddleware',
# )

# LANGUAGE_CODE = 'en'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_L10N = True
# USE_TZ = True
#
# LANGUAGES = (
#     ('en', ('English')),
#     ('zh-cn', ('中文简体')),
#     ('zh-tw', ('中文繁體')),
# )
#
# # 翻译文件所在目录，需要手工创建
# LOCALE_PATHS = (
#     os.path.join(BASE_DIR, 'locale'),
# )
#
# TEMPLATE_CONTEXT_PROCESSORS = (
#     "django.core.context_processors.i18n",
# )

# 注意：Django 1.9 及以上版本中，语言的代码发生变化(详情链接：github, django ticket，如下
# LANGUAGES = (
#     ('en', ('English')),
#     ('zh-hans', ('中文简体')),
#     ('zh-hant', ('中文繁體')),
# )

# 二，生成需要翻译的文件（Django 1.8及以下的版本）：
# python manage.py makemessages -l zh-cn
# python manage.py makemessages -l zh-tw
#
# Django 1.9 及以上版本要改成
# python manage.py makemessages -l zh_hans
# python manage.py makemessages -l zh_hant

# 三，手工翻译 locale 中的 django.po
# 此处省去500字
# ...
#
# #: .\tutorial\models.py:23
# msgid
# "created at"
# msgstr
# "创建于"
#
# #: .\tutorial\models.py:24
# msgid
# "updated at"
# msgstr
# "更新于"
#
# ...
# 此处省去几百字

# 四，编译一下，这样翻译才会生效
# python manage.py compilemessages

# 如果翻译不生效，请检查你的语言包的文件夹是不是有 中划线，请用下划线代替它。
# 比如 zh-hans 改成 zh_hans （但是要注意 setttings.py 中要用 中划线，不要也改了，就这一句话，你可能会浪费几个小时或几天）