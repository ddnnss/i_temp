import json

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from datetime import datetime,timedelta
from django.contrib.auth import login, logout,authenticate
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from random import choices
import string
from .forms import *
from customuser.models import *
import uuid
from django.utils.http import urlquote
from django.http import JsonResponse, HttpResponseRedirect








def login_req(request):
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    print(request_body)
    user = authenticate(username=request_body['email'], password=request_body['password'])
    if user is not None:
        login(request, user)
        return JsonResponse({'status': 'success'}, safe=False)
    else:
        return JsonResponse({'status':'error'}, safe=False)

def register(request):
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    data = request.POST.copy()
    form = SignUpForm(request_body)
    if form.is_valid():
        new_user = form.save(data)
        new_user.is_social_reg = False
        new_user.save()
        login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
        # msg_html = render_to_string('email/new_user.html')
        # send_mail(f'Регистрация на сайте ugscash.ru', None, 'UGSsupport@ugscash.ru',
        #           [new_user.email],
        #           fail_silently=False, html_message=msg_html)
        return JsonResponse({'status': 'success'}, safe=False)
    else:

        return JsonResponse({'status':'error','errors': form.errors}, safe=False)


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')



def password_recovery(request):
    if request.POST:
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            new_password = ''.join(choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=8))
            user.set_password(new_password)
            user.save()
            msg_html = render_to_string('email/new_password.html',{'new_password':new_password})
            send_mail(f'Новый пароль на сайте ugscash.ru', None, 'UGSsupport@ugscash.ru',
                      [email],
                      fail_silently=False, html_message=msg_html)
            messages.success(request, 'Спасибо, Ваш новый пароль выслан на почту')
        except:
            messages.success(request, 'Проверьте введенные данные')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def add_money(request):
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    print(request_body)
    request.user.balance += decimal.Decimal(request_body['amount'])
    request.user.save()
    return JsonResponse({'status': 'success'}, safe=False)
def transfer(request):
    request_unicode = request.body.decode('utf-8')
    request_body = json.loads(request_unicode)
    print(request_body)
    user=None
    wallet = request_body['id']
    try:
        user = User.objects.get(wallet=wallet)
    except:
        pass
    if user:
        user.balance += decimal.Decimal(request_body['amount'])
        user.save()
        request.user.balance -= decimal.Decimal(request_body['amount'])
        request.user.save()
        Transaction.objects.create(from_user=request.user,to_user=user,amount=decimal.Decimal(request_body['amount']))
        return JsonResponse({'status': 'success'}, safe=False)
    else:
        return JsonResponse({'status': 'user not found'}, safe=False)
def profile_index(request):
    if request.user.is_authenticated:
        profilePage = True
        profile_index = 'active'
        pageTitle = 'Личный кабинет | UGS'
        pageDescription = 'Сервис создан для игроков, которые любят и будут рисковать. UGS - финансовая подушка для игроков, которые привыкли играть на крупные суммы'
        allTransfer = Transaction.objects.all()
        if request.POST:
            print(request.POST)
            request.user.username = request.POST.get('username')
            request.user.email = request.POST.get('email')

            if request.POST.get('password') != '':
                request.user.set_password(request.POST.get('password'))
            request.user.save()
            if request.POST.get('password') != '':
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        return render(request, 'pages/lk.html', locals())

