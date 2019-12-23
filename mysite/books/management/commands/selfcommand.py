# -*- encoding: utf-8 -*-
from django.core.management import BaseCommand
from django.core.management import CommandError


from books.models import Publisher


class Command(BaseCommand):

    help = u'创建一个出版商'

    def add_arguments(self, parser):
        # python manage.py -h查看这条命令的帮助，也能看到我么自定义的参数
        parser.add_argument('name', help=u"指定name字段")  # name 必须参数，输入的第一个参数的值将赋值给name，必须参数
        parser.add_argument('-t', '--address', help=u"指定address字段")   # 可选参数 -t 或 --address -t是简写形式。
        parser.add_argument('-n', '--number', help=u"数字参数", type=int)  # 可选参数 -n 或 --number -n是简写形式。

    def handle(self, *args, **options):
        name = options['name']
        print name, '111111111', options['address']
        if options['address']:
            telephone = options['address']
            if len(telephone) > 11:
                raise CommandError(u'手机号码不能超过11位')
        else:
            telephone = '11111111111'
        Publisher.objects.create(name=name, address=telephone,
                                     city='Berkeley', state_province='CA',
                                     country='U.S.A.', website='http://www.apress.com/')
        self.stdout.write(u'出版商创建成功')


    # def handle(self, *args, **options):
    #     Publisher.objects.create(name='hou1', address='2855 Telegraph Avenue',
    #                              city='Berkeley', state_province='CA',
    #                              country='U.S.A.', website='http://www.apress.com/')
    #     self.stdout.write(u'出版商创建成功')