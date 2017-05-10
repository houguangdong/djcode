# -*- encoding: utf-8 -*-
'''
Created on 2017年2月27日

@author: houguangdong
'''


from django import forms


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100) # 选项min_length参数同样可用。
    email = forms.EmailField(required=False, label='Your e-mail address') # 像在模块中做过的那样，我们同样可以自定义字段的标签。 仅需使用label，像这样：
    message = forms.CharField(widget=forms.Textarea)

    # 自定义校验函数
    def clean_message(self):
        message = self.cleaned_data['message']
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("Not enough words!")
        return message


# shell 环境
# from contact.forms import ContactForm
# f = ContactForm()
# 默认输出按照HTML的<`` table`` >格式
# print f
# <tr><th><label for="id_subject">Subject:</label></th><td><input type="text" name="subject" id="id_subject" /></td></tr>
# <tr><th><label for="id_email">Email:</label></th><td><input type="text" name="email" id="id_email" /></td></tr>
# <tr><th><label for="id_message">Message:</label></th><td><input type="text" name="message" id="id_message" /></td></tr>

# 其他格式
# print f.as_ul()
# <li><label for="id_subject">Subject:</label> <input type="text" name="subject" id="id_subject" /></li>
# <li><label for="id_email">Email:</label> <input type="text" name="email" id="id_email" /></li>
# <li><label for="id_message">Message:</label> <input type="text" name="message" id="id_message" /></li>

# print f.as_p()
# <p><label for="id_subject">Subject:</label> <input type="text" name="subject" id="id_subject" /></p>
# <p><label for="id_email">Email:</label> <input type="text" name="email" id="id_email" /></p>
# <p><label for="id_message">Message:</label> <input type="text" name="message" id="id_message" /></p>
# 这些类方法只是一般情况下用于快捷显示完整表单的方法。 你同样可以用HTML显示个别字段：

# print f['subject']
# <input type="text" name="subject" id="id_subject" />

# Form对象做的第二件事是校验数据。 为了校验数据，我们创建一个新的对Form象，并且传入一个与定义匹配的字典类型数据：
# f = ContactForm({'subject': 'Hello', 'email': 'adrian@example.com', 'message': 'Nice site!'})
# 一旦你对一个Form实体赋值，你就得到了一个绑定form：
# f.is_bound

# 调用任何绑定form的is_valid()方法，就可以知道它的数据是否合法。 我们已经为每个字段传入了值，因此整个Form是合法的：
# f.is_valid()

# 如果我们不传入email值，它依然是合法的。因为我们指定这个字段的属性required=False：
# f = ContactForm({'subject': 'Hello', 'message': 'Nice site!'})
# f.is_valid()

# 但是，如果留空subject或message，整个Form就不再合法了：
# f = ContactForm({'subject': 'Hello'})
# f.is_valid()

# 你可以逐一查看每个字段的出错消息：
# f = ContactForm({'subject': 'Hello', 'message': ''})
# f['message'].errors

# 最终，如果一个Form实体的数据是合法的，它就会有一个可用的cleaned_data属性。 这是一个包含干净的提交数据的字典。 Django的form框架不但校验数据，它还会把它们转换成相应的Python类型数据，这叫做清理数据。
# f = ContactForm({subject': Hello, email: adrian@example.com, message: Nice site!})
# f.is_valid()
# f.cleaned_data
# {message': uNice site!, email: uadrian@example.com, subject: uHello}
# 我们的contact form只涉及字符串类型，它们会被清理成Unicode对象。如果我们使用整数型或日期型，form框架会确保方法使用合适的Python整数型或datetime.date型对象。


# 对于单独的变量
# 用safe过滤器为单独的变量关闭自动转意：
# This will be escaped: {{ data }}
# This will not be escaped: {{ data|safe }}
#
# This will be escaped: &lt;b&gt;
# This will not be escaped: <b>


# 对于模板块
# 为了控制模板的自动转意,用标签autoescape来包装整个模板(或者模板中常用的部分),就像这样：
# Auto-escaping is on by default. Hello {{ name }}
# {% autoescape off %}
#     This will not be auto-escaped: {{ data }}.
#     Nor this: {{ other_data }}
#     {% autoescape on %}
#         Auto-escaping applies again: {{ name }}
#     {% endautoescape %}
# {% endautoescape %}


# auto-escaping 标签的作用域不仅可以影响到当前模板还可以通过include标签作用到其他标签,就像block标签一样。 例如：
# # base.html
# {% autoescape off %}
# <h1>{% block title %}{% endblock %}</h1>
# {% block content %}
# {% endblock %}
# {% endautoescape %}
#
# # child.html
# {% extends "base.html" %}
# {% block title %}This & that{% endblock %}
# {% block content %}{{ greeting }}{% endblock %}
# 由于在base模板中自动转意被关闭,所以在child模板中自动转意也会关闭.因此,在下面一段HTML被提交时,变量greeting的值就为字符串Hello!
# <h1>This & that</h1>
# <b>Hello!</b>


# 过滤器参数里的字符串常量的自动转义
# 就像我们前面提到的,过滤器也可以是字符串.
# {{ data|default:"This is a string literal." }}
# 所有字符常量没有经过转义就被插入模板,就如同它们都经过了safe过滤。 这是由于字符常量完全由模板作者决定,因此编写模板的时候他们会确保文本的正确性。
#
# 这意味着你必须这样写
# {{ data|default:"3 &lt; 2" }}
# 而不是这样
# {{ data|default:"3 < 2" }}  <-- Bad! Don't do this.
# 这点对来自变量本身的数据不起作用。 如果必要,变量内容会自动转义,因为它们不在模板作者的控制下。


# Django有两种方法加载模板
# django.template.loader.get_template(template_name) ： get_template 根据给定的模板名称返回一个已编译的模板（一个 Template 对象）。 如果模板不存在，就触发 TemplateDoesNotExist 的异常。
# django.template.loader.select_template(template_name_list) ： select_template 很像 get_template ，不过它是以模板名称的列表作为参数的。 它会返回列表中存在的第一个模板。 如果模板都不存在，将会触发TemplateDoesNotExist异常。