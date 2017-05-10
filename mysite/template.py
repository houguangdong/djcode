# -*- encoding: utf-8 -*-
'''
Created on 2017年2月27日

@author: houguangdong
'''

import datetime
from django import template
from django.template import Template, Context

# 在python解释器下运行
# python manage.py shell
t = template.Template("my name is {{name}}.")
c = template.Context({"name": "houguangdong"})
print t.render(c)


raw_template = """
<p>Dear {{ person_name }},</p>
<p>Thanks for placing an order from {{ company }}. It's scheduled to
ship on {{ ship_date|date:"F j, Y" }}.</p>
{% if ordered_warranty %}
    <p>Your warranty information will be included in the packaging.</p>
{% else %}
    <p>You didn't order a warranty, so you're on your own when
    the products inevitably stop working.</p>
{% endif %}
<p>Sincerely,<br />{{ company }}</p>
"""
t = Template(raw_template)
c = Context({
    'person_name': 'John Smith',
    'company': 'Outdoor Equipment',
    'ship_date': datetime.date(2009, 4, 2),
    'ordered_warranty': False
    }
)
t.render(c)


t = Template('Hello, {{ name }}')
print t.render(Context({'name': 'John'}))
print t.render(Context({'name': 'Julie'}))
print t.render(Context({'name': 'Pat'}))


t = Template('Hello, {{ name }}')
for name in ('John', 'Julie', 'Pat'):
    print t.render(Context({'name': name}))


person = {'name': 'Sally', 'age': '43'}
t = Template('{{ person.name }} is {{ person.age }} years old.')
c = Context({'person': person})
t.render(c)


d = datetime.date(1993, 5, 2)
print d.year, d.month, d.day

t = Template('The month is {{ date.month }} and the year is {{ date.year }}.')
c = Context({'date': d})
t.render(c)


class Person(object):
    def __init__(self, first_name, last_name):
        self.first_name, self.last_name = first_name, last_name

t = Template('Hello, {{ person.first_name }} {{ person.last_name }}.')
c = Context({'person': Person('John', 'Smith')})
t.render(c)


t = Template('{{ var }} -- {{ var.upper }} -- {{ var.isdigit }}')
t.render(Context({'var': 'hello'}))
t.render(Context({'var': '123'}))


t = Template('Item 2 is {{ items.2 }}.')
c = Context({'items': ['apples', 'bananas', 'carrots']})
t.render(c)


person = {'name': 'Sally', 'age': '43'}
t = Template('{{ person.name.upper }} is {{ person.age }} years old.')
c = Context({'person': person})
t.render(c)


t = Template("My name is {{ person.first_name }}.")
class PersonClass3:
    def first_name(self):
        raise AssertionError, "foo"
p = PersonClass3()
t.render(Context({"person": p}))


class SilentAssertionError(AssertionError):
    silent_variable_failure = True
class PersonClass4:
    def first_name(self):
        raise SilentAssertionError
p = PersonClass4()
t.render(Context({"person": p}))


def delete(self):
    # Delete the account
delete.alters_data = True


t = Template('Your name is {{ name }}.')
t.render(Context())
t.render(Context({'var': 'hello'}))
t.render(Context({'NAME': 'hello'}))
t.render(Context({'Name': 'hello'}))


c = Context({"foo": "bar"})
print c['foo']
del c['foo']
print c['foo']
c['newvariable'] = 'hello'
print c['newvariable']

# 标签
{% if today_is_weekend %}
    <p>Welcome to the weekend!</p>
{% endif %}
# ---------------------------------
{% if today_is_weekend %}
    <p>Welcome to the weekend!</p>
{% else %}
    <p>Get back to work.</p>
{% endif %}

# ---------------------------------
{% if athlete_list and coach_list %}
    Both athletes and coaches are available.
{% endif %}

# -------------------------------
{% if not athlete_list %}
    There are no athletes.
{% endif %}

# -------------------------------
{% if athlete_list or coach_list %}
    There are some athletes or some coaches.
{% endif %}

# --------------------------------
{% if not athlete_list or coach_list %}
    There are no athletes or there are some coaches.
{% endif %}

# ----------------------------------
{% if athlete_list and not coach_list %}
    There are some athletes and absolutely no coaches.
{% endif %}


# {% if %} 标签不允许在同一个标签中同时使用 and 和 or ，因为逻辑上可能模糊的，例如，如下示例是错误的： 比如这样的代码是不合法的：
{% if athlete_list and coach_list or cheerleader_list %}

# 系统不支持用圆括号来组合比较操作。 如果你确实需要用到圆括号来组合表达你的逻辑式，考虑将它移到模板之外处理，然后以模板变量的形式传入结果吧。 或者，仅仅用嵌套的{% if %}标签替换吧，就像这样：
{% if athlete_list %}
    {% if coach_list or cheerleader_list %}
        We have athletes, and either coaches or cheerleaders!
    {% endif %}
{% endif %}

# 并没有 {% elif %} 标签， 请使用嵌套的`` {% if %}`` 标签来达成同样的效果：
{% if athlete_list %}
    <p>Here are the athletes: {{ athlete_list }}.</p>
{% else %}
    <p>No athletes are available.</p>
    {% if coach_list %}
        <p>Here are the coaches: {{ coach_list }}.</p>
    {% endif %}
{% endif %}
#一定要用 {% endif %} 关闭每一个 {% if %} 标签。


<ul>
{% for athlete in athlete_list %}
    <li>{{ athlete.name }}</li>
{% endfor %}
</ul>

{% for athlete in athlete_list reversed %}
...
{% endfor %}

{% for athlete in athlete_list %}
    <h1>{{ athlete.name }}</h1>
    <ul>
    {% for sport in athlete.sports_played %}
        <li>{{ sport }}</li>
    {% endfor %}
    </ul>
{% endfor %}

{% if athlete_list %}
    {% for athlete in athlete_list %}
        <p>{{ athlete.name }}</p>
    {% endfor %}
{% else %}
    <p>There are no athletes. Only computer programmers.</p>
{% endif %}

{% for athlete in athlete_list %}
    <p>{{ athlete.name }}</p>
{% empty %}
    <p>There are no athletes. Only computer programmers.</p>
{% endfor %}

# Django不支持退出循环操作。 如果我们想退出循环，可以改变正在迭代的变量，让其仅仅包含需要迭代的项目。 同理，Django也不支持continue语句，我们无法让当前迭代操作跳回到循环头部。 （请参看本章稍后的理念和限制小节，了解下决定这个设计的背后原因）
# forloop.counter 总是一个表示当前循环的执行次数的整数计数器。 这个计数器是从1开始的，所以在第一次循环时 forloop.counter 将会被设置为1。
{% for item in todo_list %}
    <p>{{ forloop.counter }}: {{ item }}</p>
{% endfor %}
# forloop.counter0 类似于 forloop.counter ，但是它是从0计数的。 第一次执行循环时这个变量会被设置为0。
# forloop.revcounter 是表示循环中剩余项的整型变量。 在循环初次执行时 forloop.revcounter 将被设置为序列中项的总数。 最后一次循环执行中，这个变量将被置1。
# forloop.revcounter0 类似于 forloop.revcounter ，但它以0做为结束索引。 在第一次执行循环时，该变量会被置为序列的项的个数减1。

# forloop.first 是一个布尔值，如果该迭代是第一次执行，那么它被置为```` 在下面的情形中这个变量是很有用的：
{% for object in objects %}
    {% if forloop.first %}<li class="first">{% else %}<li>{% endif %}
    {{ object }}
    </li>
{% endfor %}

# forloop.last 是一个布尔值；在最后一次执行循环时被置为True。 一个常见的用法是在一系列的链接之间放置管道符（|）
{% for link in links %}{{ link }}{% if not forloop.last %} | {% endif %}{% endfor %}
# 上面的模板可能会产生如下的结果：
# Link1 | Link2 | Link3 | Link4

# 另一个常见的用途是为列表的每个单词的加上逗号。
{% for p in places %}{{p}}{% if not forloop.last %}, {% endif %}{% endfor %}

# forloop.parentloop是一个指向当前循环的上一级循环的forloop 对象的引用（在嵌套循环的情况下）。
{%for country in countries %}
    <table>
    {%for city in country.city_list %}
    <tr>
        <td>Country  # {{ forloop.parentloop.counter }}</td>
        <td>City  # {{ forloop.counter }}</td>
        <td>{{city}}</td>
    </tr >
    {% endfor %}
    </table>
{% endfor %}
# forloop 变量仅仅能够在循环中使用。 在模板解析器碰到{% endfor %}标签后，forloop就不可访问了。

# Context和forloop变量
# 在一个 {% for %} 块中，已存在的变量会被移除，以避免 forloop 变量被覆盖。 Django会把这个变量移动到
# forloop.parentloop 中。通常我们不用担心这个问题，但是一旦我们在模板中定义了 forloop 这个变量（当然我们反对这样做），
# 在 {% for %} 块中它会在 forloop.parentloop 被重新命名。

# 下面的例子比较两个模板变量 user 和 currentuser :
{% ifequal user currentuser %}
    <h1>Welcome!</h1>
{% endifequal %}

# 参数可以是硬编码的字符串，随便用单引号或者双引号引起来，所以下列代码都是正确的：
{% ifequal section 'sitenews' %}
    <h1>Site News</h1>
{% endifequal %}

{% ifequal section "community" %}
    <h1>Community</h1>
{% endifequal %}

# 和 {% if %} 类似， {% ifequal %} 支持可选的 {% else%} 标签：
{% ifequal section 'sitenews' %}
    <h1>Site News</h1>
{% else %}
    <h1>No News Here</h1>
{% endifequal %}

# 只有模板变量，字符串，整数和小数可以作为 {% ifequal %} 标签的参数。下面是合法参数的例子：
{% ifequal variable 1 %}
{% ifequal variable 1.23 %}
{% ifequal variable 'foo' %}
{% ifequal variable "foo" %}

# 其他任何类型，例如Python的字典类型、列表类型、布尔类型，不能用在 {% ifequal %} 中。 下面是些错误的例子：
{% ifequal variable True %}
{% ifequal variable [1, 2, 3] %}
{% ifequal variable {'key': 'value'} %}
# 如果你需要判断变量是真还是假，请使用 {% if %} 来替代 {% ifequal %} 。

# 注释
# 就像HTML或者Python，Django模板语言同样提供代码注释。 注释使用 {# #} ：
{# This is a comment #}

# 如果要实现多行注释，可以使用`` {% comment %}`` 模板标签，就像这样：
{% comment %}
This is a
multi-line comment.
{% endcomment %}

过滤器
# 就象本章前面提到的一样，模板过滤器是在变量被显示前修改它的值的一个简单方法。 过滤器使用管道字符，如下所示：
{{ name|lower }}

# 过滤管道可以被* 套接* ，既是说，一个过滤器管道的输出又可以作为下一个管道的输入，如此下去。 下面的例子实现查找列表的第一个元素并将其转化为大写。
{{ my_list|first|upper }}

# 有些过滤器有参数。 过滤器的参数跟随冒号之后并且总是以双引号包含。 例如：
{{ bio|truncatewords:"30" }}
# 这个将显示变量 bio 的前30个词。

# addslashes : 添加反斜杠到任何反斜杠、单引号或者双引号前面。 这在处理包含JavaScript的文本时是非常有用的。
# date : 按指定的格式字符串参数格式化 date 或者 datetime 对象， 范例：
{{ pub_date|date:"F j, Y" }}
# length : 返回变量的长度