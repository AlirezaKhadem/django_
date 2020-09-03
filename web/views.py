# -*- coding: utf-8 -*-

from datetime import datetime
from json import JSONEncoder

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string

from .models import Token, User, Expense, Income, Passwordresetcode


# Create your views here.

@csrf_exempt
def submit_expense(request):
    """user submit a expense"""

    this_token = request.POST['token']
    this_user = User.objects.filter(token__token=this_token).get()
    if 'date' not in request.POST:
        date = datetime.now()

    Expense.objects.create(user=this_user, amount=request.POST['amount'], text=request.POST['text'], date=date)

    print(request.POST)

    return JsonResponse({
        'status_code': 200
    }, encoder=JSONEncoder)


@csrf_exempt
def submit_income(request):
    """user submit a income"""

    this_token = request.POST['token']
    this_user = User.objects.filter(token__token=this_token).get()
    if 'date' not in request.POST:
        date = datetime.now()

    Income.objects.create(user=this_user, amount=request.POST['amount'], text=request.POST['text'], date=date)

    print(request.POST)

    return JsonResponse({
        'status_code': 200
    }, encoder=JSONEncoder)


def register(request):
    if 'requestcode' in request.POST:

        # if not grecaptcha_verify(request):
        #     context = {'message': 'captcha not verified'}
        #     print(context)
        #     return JsonResponse(context, encoder=JSONEncoder)

        if User.objects.filter(email=request.POST['email']).exists():
            context = {'message': 'email exist'}
            print(context)
            return JsonResponse(context, encoder=JSONEncoder)

        if not User.objects.filter(username=request.POST['username']).exists():
            code = get_random_string(length=32)
            now = datetime.now()
            email = request.POST['email']
            password = request.POST['password']
            username = request.POST['username']
            temporarycode = Passwordresetcode(email=email, time=now, username=username, password=password, code=code)
            temporarycode.save()

            body = " برای فعال کردن اکانت بستون خود روی لینک روبرو کلیک کنید: <a href=\"{}?code={}\">لینک رو به رو</a> ".format(
                request.build_absolute_uri('/account/register/'), code)
            context = {'message': body}
            print(context)
            # return render(request, 'index.html', context)
            return JsonResponse(context, encoder=JSONEncoder)

        else:
            context = {'message': 'another person use this username'}
            print(context)
            return JsonResponse(context, encoder=JSONEncoder)
    elif 'code' in request.GET:
        code = request.GET['code']

        if Passwordresetcode.objects.filter(code=code).exists():
            new_temp_user = Passwordresetcode.objects.get(code=code)
            new_user = User.objects.create(username=new_temp_user.username,
                                           password=new_temp_user.password,
                                           email=new_temp_user.email)
            this_token = get_random_string(48)
            Token.objects.create(user=new_user, token=this_token)
            Passwordresetcode.objects.filter(code=code).delete()
            context = {'message': "account activated, your token: {},\n please save it".format(this_token)}
            return JsonResponse(context, encoder=JSONEncoder)
        else:
            context = "your account not active"
            print(context)
            return JsonResponse(context, encoder=JSONEncoder)
    else:
        context = {'message': ''}
        print(context)
        return render(request, 'web/register.html', context)
