from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from .models import User
import simplejson
import jwt, datetime
import bcrypt
from django.conf import settings

AUTH_EXPIRE = 60 * 60 * 5
# Create your views here.

def homepage(request):
    return HttpResponse('welcome to glassland')


def gen_token(user_id):
    ret = jwt.encode({
        'user_id': user_id,
        'exp': int(datetime.datetime.now().timestamp()) + AUTH_EXPIRE
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
        user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        try:
            user.save()
            print('*' * 25)
            return JsonResponse({'token' : gen_token(user.id)})  #jieshou yige  zidian
        except Exception as e:
            print(e)

    except Exception as e:
        print(e)
        return HttpResponseBadRequest()


def login(request):
    try:
        payload = simplejson.loads(request.body)
        email = payload['email']
        password = payload['password']

        # 验证邮箱是否存在，如果存在，就查看密码
        user = User.objects.filter(email=email).first()
        if not user:  # 表示查无此人
            return HttpResponseBadRequest()  #暂时先返回有问题的请求
        if not bcrypt.checkpw(password.encode(), user.password.encode()):
            return HttpResponseBadRequest()  #说明密码不对，暂时返回400

        return JsonResponse({
            'user': {
                'user_id': user.id,
                'name': user.name,
                'email': user.email
            },
            'token': gen_token(user.id)
        })  # 200

    except Exception as e:
        print(e)
        return HttpResponseBadRequest()




def authenticate(view):
    def wrapper(request):
        #将jwt放入header中
        #print(list(request.META.items()))
        token = request.META.get('HTTP_JWT')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            #  取出payload  是 一个header中的token
            print(payload)
            print(payload['exp'])
            # 考虑 过期时间
            #if (datetime.datetime.now().timestamp() - payload['timestamp']) > AUTH_EXPIRE:
            #    return HttpResponse(status=401)
            # 到这里，说明用户已经算是个合法用户
            user_id = payload['user_id']

            #查一次数据库
            user = User.objects.get(pk=user_id)

            request.user = user



            #return HttpResponse('2oo!')
        except Exception as e:
            print(e, '!!!!!!!!!!!!!!!')
            return HttpResponse(status=401)

        return view(request)
    
    return wrapper


@authenticate
def test(request):
    return HttpResponse(b'ok')

