from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from .models import User
import simplejson
import jwt, datetime
from blog0 import settings

# Create your views here.

def homepage(request):
    return HttpResponse('welcome to glassland')


def gen_token(user_id):
    ret = jwt.encode({
        'user_id': user_id,
        'timestamp': int(datetime.datetime.now().timestamp())
    }, settings.SECRET_KEY, 'HS256')

    return ret.decode()


def reg(request):
    try:
        payload = simplejson.loads(request.body)
        email = payload['email']
        qs = User.objects.filter(email=email)
        print(qs)

        if qs:         # biaoshi email yijing cunzai
            return HttpResponseBadRequest()

        name = payload['name']
        password = payload['password']

        print(email, name, password)

        user = User()
        user.email = email
        user.name = name
        user.password = password
        try:
            user.save()
            print('*' * 25)
            return JsonResponse({'token' : gen_token(user.id)})  #jieshou yige  zidian
        except Exception as e:
            print(e)

    except Exception as e:
        print(e)
        return HttpResponseBadRequest()