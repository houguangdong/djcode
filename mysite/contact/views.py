# -*- encoding: utf-8 -*-
'''
Created on 2017年2月27日

@author: houguangdong
'''

from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.template import RequestContext
from contact.forms import ContactForm


def contact(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('subject', ''):
            errors.append('Enter a subject.')
        if not request.POST.get('message', ''):
            errors.append('Enter a message.')
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Enter a valid e-mail address.')
        if not errors:
            # 我们使用了django.core.mail.send_mail函数来发送e - mail。 这个函数有四个必选参数： 主题，正文，寄信人和收件人列表。
            send_mail(
                request.POST['subject'],
                request.POST['message'],
                request.POST.get('email', 'ghou@vmware.com'),
                ['1737785826@qq.com'],
            )
            return HttpResponseRedirect('/thanks/')
    # return render_to_response('book/contact_form.html',
    # {
    #     'errors': errors,
    #     'subject': request.POST.get('subject', ''),
    #     'message': request.POST.get('message', ''),
    #     'email': request.POST.get('email', ''),
    # })
    return render(request, 'book/contact_form.html',{
          'errors': errors,
          'subject': request.POST.get('subject', ''),
          'message': request.POST.get('message', ''),
          'email': request.POST.get('email', ''),
    })


def contact_new(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreply@example.com'),
                ['siteowner@example.com'],
            )
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm(initial={'subject': 'I love your site!'})
    return render_to_response('book/contact_form_new.html', {'form': form})