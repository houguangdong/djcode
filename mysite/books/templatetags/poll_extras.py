# -*- encoding: utf-8 -*-
'''
Created on 2017年2月27日

@author: houguangdong
'''

from django import template

register = template.Library()

# 这里是一些定义过滤器的例子：
def cut(value, arg):
    "Removes all values of arg from the given string"
    return value.replace(arg, '')

# 下面是一个可以用来去掉变量值空格的过滤器例子：
# {{ somevariable|cut:" " }}

# 大多数过滤器并不需要参数。 下面的例子把参数从你的函数中拿掉了：
# def lower(value): # Only one argument.
#     "Converts a string into all lowercase"
#     return value.lower()
# 当你定义完过滤器后，你需要用 Library 实例来注册它，这样就能通过Django的模板语言来使用了：
# register.filter('cut', cut)
# register.filter('lower', lower)


# 你可以使用装饰器register.filter()：
# @register.filter(name='cut')
# def cut(value, arg):
#     return value.replace(arg, '')

# 如果你想第二个例子那样不使用 name 参数，那么Django会把函数名当作过滤器的名字。
# @register.filter
# def lower(value):
#     return value.lower()

# 下面是一个完整的模板库的例子，它包含一个 cut 过滤器：
# @register.filter(name='cut')
# def cut(value, arg):
#     return value.replace(arg, '')


# 编写编译函数
# 当遇到一个模板标签（template tag）时，模板解析器就会把标签包含的内容，以及模板解析器自己作为参数调用一个python函数。 这个函数负责返回一个和当前模板标签内容相对应的节点（Node）的实例。
# 例如，写一个显示当前日期的模板标签：{% current_time %}。该标签会根据参数指定的 strftime 格式（参见：http://www.djangoproject.com/r/python/strftime/）显示当前时间。首先确定标签的语法是个好主意。 在这个例子里，标签应该这样使用：
# <p>The time is {% current_time "%Y-%m-%d %I:%M %p" %}.</p>
# 注意
# 没错, 这个模板标签是多余的，Django默认的 {% now %} 用更简单的语法完成了同样的工作。 这个模板标签在这里只是作为一个例子。
# 这个函数的分析器会获取参数并创建一个 Node 对象:
#
#
# def do_current_time(parser, token):
#     try:
#         # split_contents() knows not to split quoted strings.
#         tag_name, format_string = token.split_contents()
#     except ValueError:
#         msg = '%r tag requires a single argument' % token.split_contents()[0]
#         raise template.TemplateSyntaxError(msg)
#     return CurrentTimeNode(format_string[1:-1])
#
# 这里需要说明的地方很多：
# 每个标签编译函数有两个参数，parser和token。parser是模板解析器对象。 我们在这个例子中并不使用它。 token是正在被解析的语句。
# token.contents 是包含有标签原始内容的字符串。 在我们的例子中，它是 'current_time "%Y-%m-%d %I:%M %p"' 。
# token.split_contents() 方法按空格拆分参数同时保证引号中的字符串不拆分。 应该避免使用 token.contents.split() （仅使用Python的标准字符串拆分）。 它不够健壮，因为它只是简单的按照所有空格进行拆分，包括那些引号引起来的字符串中的空格。
# 这个函数可以抛出 django.template.TemplateSyntaxError ，这个异常提供所有语法错误的有用信息。
# 不要把标签名称硬编码在你的错误信息中，因为这样会把标签名称和你的函数耦合在一起。 token.split_contents()[0]总是记录标签的名字，就算标签没有任何参数。
# 这个函数返回一个 CurrentTimeNode （稍后我们将创建它），它包含了节点需要知道的关于这个标签的全部信息。 在这个例子中，它只是传递了参数 "%Y-%m-%d %I:%M %p" 。模板标签开头和结尾的引号使用 format_string[1:-1] 除去。
# 模板标签编译函数 必须 返回一个 Node 子类，返回其它值都是错的。


# 编写模板节点
# 编写自定义标签的第二步就是定义一个拥有 render() 方法的 Node 子类。 继续前面的例子，我们需要定义 CurrentTimeNode ：

import datetime

class CurrentTimeNode(template.Node):
    def __init__(self, format_string):
        self.format_string = str(format_string)

    def render(self, context):
        now = datetime.datetime.now()
        return now.strftime(self.format_string)

# 这两个函数（ __init__() 和 render() ）与模板处理中的两步（编译与渲染）直接对应。 这样，初始化函数仅仅需要存储后面要用到的格式字符串，而 render() 函数才做真正的工作。
# 与模板过滤器一样，这些渲染函数应该静静地捕获错误，而不是抛出错误。 模板标签只允许在编译的时候抛出错误。
# 注册标签
# 最后，你需要用你模块的Library 实例注册这个标签。 注册自定义标签与注册自定义过滤器非常类似（如前文所述）。 只需实例化一个 template.Library 实例然后调用它的 tag() 方法。 例如：
# register.tag('current_time', do_current_time)
# tag() 方法需要两个参数:
# 模板标签的名字（字符串）。
# 编译函数。
# 和注册过滤器类似，也可以在Python2.4及其以上版本中使用 register.tag装饰器：
# @register.tag(name="current_time")
# def do_current_time(parser, token):
#     # ...
#
# @register.tag
# def shout(parser, token):
#     # ...
# 如果你像在第二个例子中那样忽略 name 参数的话，Django会使用函数名称作为标签名称。


# 在上下文中设置变量
# 前一节的例子只是简单的返回一个值。 很多时候设置一个模板变量而非返回值也很有用。 那样，模板作者就只能使用你的模板标签所设置的变量。
# 要在上下文中设置变量，在 render() 函数的context对象上使用字典赋值。 这里是一个修改过的 CurrentTimeNode ，其中设定了一个模板变量 current_time ，并没有返回它：
#
# class CurrentTimeNode2(template.Node):
#     def __init__(self, format_string):
#         self.format_string = str(format_string)
#
#     def render(self, context):
#         now = datetime.datetime.now()
#         context['current_time'] = now.strftime(self.format_string)
#         return ''
#
# (我们把创建函数do_current_time2和注册给current_time2模板标签的工作留作读者练习。)
# 注意 render() 返回了一个空字符串。 render() 应当总是返回一个字符串，所以如果模板标签只是要设置变量， render() 就应该返回一个空字符串。
# 你应该这样使用这个新版本的标签：
# {% current_time2 "%Y-%M-%d %I:%M %p" %}
# <p>The time is {{ current_time }}.</p>
# 但是 CurrentTimeNode2 有一个问题: 变量名 current_time 是硬编码的。 这意味着你必须确定你的模板在其它任何地方都不使用 {{ current_time }} ，因为 {% current_time2 %} 会盲目的覆盖该变量的值。
# 一种更简洁的方案是由模板标签来指定需要设定的变量的名称，就像这样：
# {% get_current_time "%Y-%M-%d %I:%M %p" as my_current_time %}
# <p>The current time is {{ my_current_time }}.</p>
# 为此，你需要重构编译函数和 Node 类，如下所示：
# import re
# class CurrentTimeNode3(template.Node):
#     def __init__(self, format_string, var_name):
#         self.format_string = str(format_string)
#         self.var_name = var_name
#
#     def render(self, context):
#         now = datetime.datetime.now()
#         context[self.var_name] = now.strftime(self.format_string)
#         return ''
#
# def do_current_time(parser, token):
#     # This version uses a regular expression to parse tag contents.
#     try:
#         # Splitting by None == splitting by spaces.
#         tag_name, arg = token.contents.split(None, 1)
#     except ValueError:
#         msg = '%r tag requires arguments' % token.contents[0]
#         raise template.TemplateSyntaxError(msg)
#
#     m = re.search(r'(.*?) as (\w+)', arg)
#     if m:
#         fmt, var_name = m.groups()
#     else:
#         msg = '%r tag had invalid arguments' % tag_name
#         raise template.TemplateSyntaxError(msg)
#
#     if not (fmt[0] == fmt[-1] and fmt[0] in ('"', "'")):
#         msg = "%r tag's argument should be in quotes" % tag_name
#         raise template.TemplateSyntaxError(msg)
#
#     return CurrentTimeNode3(fmt[1:-1], var_name)
# 现在 do_current_time() 把格式字符串和变量名传递给 CurrentTimeNode3 。


# 分析直至另一个模板标签
# 标准的 {% comment %} 标签是这样实现的：

def do_comment(parser, token):
    nodelist = parser.parse(('endcomment',))
    parser.delete_first_token()
    return CommentNode()

class CommentNode(template.Node):
    def render(self, context):
        return ''

# parser.parse() 接收一个包含了需要分析的模板标签名的元组作为参数。 它返回一个django.template.NodeList实例，它是一个包含了所有Node对象的列表，这些对象是解析器在解析到任一元组中指定的标签之前遇到的内容.
# 因此在前面的例子中， nodelist 是在 {% comment %} 和 {% endcomment %} 之间所有节点的列表，不包括 {% comment %} 和 {% endcomment %} 自身。
# 在 parser.parse() 被调用之后，分析器还没有清除 {% endcomment %} 标签，因此代码需要显式地调用 parser.delete_first_token() 来防止该标签被处理两次。
# 之后 CommentNode.render() 只是简单地返回一个空字符串。 在 {% comment %} 和 {% endcomment %} 之间的所有内容都被忽略。

# 分析直至另外一个模板标签并保存内容
# 例如，这个自定义模板标签{% upper %}，它会把它自己和{% endupper %}之间的内容变成大写：
# {% upper %}
#     This will appear in uppercase, {{ user_name }}.
# {% endupper %}
# 就像前面的例子一样，我们将使用 parser.parse() 。这次，我们将产生的 nodelist 传递给 Node ：

def do_upper(parser, token):
    nodelist = parser.parse(('endupper',))
    parser.delete_first_token()
    return UpperNode(nodelist)


class UpperNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist


    def render(self, context):
        output = self.nodelist.render(context)
        return output.upper()
# 这里唯一的一个新概念是 UpperNode.render() 中的 self.nodelist.render(context) 。它对节点列表中的每个 Node 简单的调用 render() 。
# 更多的复杂渲染示例请查看 django/template/defaulttags.py 中的 {% if %} 、 {% for %} 、 {% ifequal %} 和 {% ifchanged %} 的代码。

# 简单标签的快捷方式
# 我们之前的的 current_time 函数于是可以写成这样：
def current_time(format_string):
    try:
        return datetime.datetime.now().strftime(str(format_string))
    except UnicodeEncodeError:
        return ''

register.simple_tag(current_time)

# 在Python 2.4中，也可以使用装饰器语法：
@register.simple_tag
def current_time(token):
    pass

# 包含标签
# 另外一类常用的模板标签是通过渲染 其他 模板显示数据的。 比如说，Django的后台管理界面，它使用了自定义的模板标签来显示新增/编辑表单页面下部的按钮。 那些按钮看起来总是一样的，但是链接却随着所编辑的对象的不同而改变。 这就是一个使用小模板很好的例子，这些小模板就是当前对象的详细信息。
# 这些排序标签被称为 包含标签 。如何写包含标签最好通过举例来说明。 让我们来写一个能够产生指定作者对象的书籍清单的标签。 我们将这样利用标签：

# {% books_for_author author %}
# 结果将会像下面这样：
# <ul>
#     <li>The Cat In The Hat</li>
#     <li>Hop On Pop</li>
#     <li>Green Eggs And Ham</li>
# </ul>
# 首先，我们定义一个函数，通过给定的参数生成一个字典形式的结果。 需要注意的是，我们只需要返回字典类型的结果就行了，不需要返回更复杂的东西。 这将被用来作为模板片段的内容：

def books_for_author(author):
    books = Book.objects.filter(authors__id=author.id)
    return {'books': books}
# 接下来，我们创建用于渲染标签输出的模板。 在我们的例子中，模板很简单：
# <ul>
# {% for book in books %}
#     <li>{{ book.title }}</li>
# {% endfor %}
# </ul>
# 最后，我们通过对一个 Library 对象使用 inclusion_tag() 方法来创建并注册这个包含标签。
# 在我们的例子中，如果先前的模板在 polls/result_snippet.html 文件中，那么我们这样注册标签：
# register.inclusion_tag('book_snippet.html')(books_for_author)
# Python 2.4装饰器语法也能正常工作，所以我们可以这样写：

@register.inclusion_tag('book_snippet.html')
def books_for_author(author):
    # ...
    pass

# 有时候，你的包含标签需要访问父模板的context。 为了解决这个问题，Django为包含标签提供了一个 takes_context 选项。 如果你在创建模板标签时，指明了这个选项，这个标签就不需要参数，并且下面的Python函数会带一个参数： 就是当这个标签被调用时的模板context。
# 例如，你正在写一个包含标签，该标签包含有指向主页的 home_link 和 home_title 变量。 Python函数会像这样：

@register.inclusion_tag('link.html', takes_context=True)
def jump_link(context):
    return {
        'link': context['home_link'],
        'title': context['home_title'],
    }
# （注意函数的第一个参数 必须 是 context 。）
# 模板 link.html 可能包含下面的东西：
# Jump directly to <a href="{{ link }}">{{ title }}</a>.
# 然后您想使用自定义标签时，就可以加载它的库，然后不带参数地调用它，就像这样：
# {% jump_link %}

# 编写自定义模板加载器
# Djangos 内置的模板加载器（在先前的模板加载内幕章节有叙述）通常会满足你的所有的模板加载需求，但是如果你有特殊的加载需求的话，编写自己的模板加载器也会相当简单。 比如：你可以从数据库中，或者利用Python的绑定直接从Subversion库中，更或者从一个ZIP文档中加载模板。
#
# 模板加载器，也就是 TEMPLATE_LOADERS 中的每一项，都要能被下面这个接口调用：
#
# load_template_source(template_name, template_dirs=None)
# 参数 template_name 是所加载模板的名称 (和传递给 loader.get_template() 或者 loader.select_template() 一样), 而 template_dirs 是一个可选的代替TEMPLATE_DIRS的搜索目录列表。
#
# 如果加载器能够成功加载一个模板, 它应当返回一个元组： (template_source, template_path) 。在这里的 template_source 就是将被模板引擎编译的的模板字符串，而 template_path 是被加载的模板的路径。 由于那个路径可能会出于调试目的显示给用户，因此它应当很快的指明模板从哪里加载。
#
# 如果加载器加载模板失败，那么就会触发 django.template.TemplateDoesNotExist 异常。
#
# 每个加载函数都应该有一个名为 is_usable 的函数属性。 这个属性是一个布尔值，用于告知模板引擎这个加载器是否在当前安装的Python中可用。 例如，如果 pkg_resources 模块没有安装的话，eggs加载器（它能够从python eggs中加载模板）就应该把 is_usable 设为 False ，因为必须通过 pkg_resources 才能从eggs中读取数据。
#
# 一个例子可以清晰地阐明一切。 这儿是一个模板加载函数，它可以从ZIP文件中加载模板。 它使用了自定义的设置 TEMPLATE_ZIP_FILES 来取代了 TEMPLATE_DIRS 用作查找路径，并且它假设在此路径上的每一个文件都是包含模板的ZIP文件：
#
# from django.conf import settings
# from django.template import TemplateDoesNotExist
# import zipfile
#
# def load_template_source(template_name, template_dirs=None):
#     "Template loader that loads templates from a ZIP file."
#
#     template_zipfiles = getattr(settings, "TEMPLATE_ZIP_FILES", [])
#
#     # Try each ZIP file in TEMPLATE_ZIP_FILES.
#     for fname in template_zipfiles:
#         try:
#             z = zipfile.ZipFile(fname)
#             source = z.read(template_name)
#         except (IOError, KeyError):
#             continue
#         z.close()
#         # We found a template, so return the source.
#         template_path = "%s:%s" % (fname, template_name)
#         return (source, template_path)
#
#     # If we reach here, the template couldn't be loaded
#     raise TemplateDoesNotExist(template_name)
#
# # This loader is always usable (since zipfile is included with Python)
# load_template_source.is_usable = True
# 我们要想使用它，还差最后一步，就是把它加入到 TEMPLATE_LOADERS 。 如果我们将这个代码放入一个叫mysite.zip_loader的包中，那么我们要把mysite.zip_loader.load_template_source加到TEMPLATE_LOADERS中。
#
# 配置独立模式下的模板系统
# 注意：
#
# 这部分只针对于对在其他应用中使用模版系统作为输出组件感兴趣的人。 如果你是在Django应用中使用模版系统，请略过此部分。
#
# 通常，Django会从它的默认配置文件和由 DJANGO_SETTINGS_MODULE 环境变量所指定的模块中加载它需要的所有配置信息。 （这点在第四章的”特殊的Python命令提示行”一节解释过。）但是当你想在非Django应用中使用模版系统的时候，采用环境变量并不方便，因为你可能更想同其余的应用一起配置你的模板系统，而不是处理配置文件并通过环境变量指向他们。
#
# 为了解决这个问题，你需要使用附录D中所描述的手动配置选项。概括的说，你需要导入正确的模板中的片段，然后在你访问任一个模板函数之前，首先用你想指定的配置访问Django.conf.settings.configure()。
#
# 你可能会考虑至少要设置 TEMPLATE_DIRS （如果你打算使用模板加载器）， DEFAULT_CHARSET （尽管默认的 utf-8 编码相当好用），以及 TEMPLATE_DEBUG 。所有可用的选项在附录D中都有详细描述，所有以 TEMPLATE_ 开头的选项都可能使你感兴趣。