from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User  # django封装好的验证功能
from django.contrib import auth
from .models import UserInfo
import json
from django.views.decorators.csrf import csrf_exempt


class Login(View):

    def post(self, request):
        print(request.method)
        obj = json.loads(request.body)
        username = obj.get('username', None)
        password = obj.get('password', None)

        if username is not None and password is not None:
            user = auth.authenticate(request, username=username, password=password)
            # user = UserInfo.objects.filter(userName=username, passWord=password)
            if user:
                auth.login(request, user)
                return HttpResponse(json.dumps({'code': 200, 'message': '登陆成功', 'user': username}), content_type="application/json")
            else:
                return JsonResponse({'code': 0, 'message': '没有此用户'})
        else:
            return JsonResponse({'code': 0, 'message': '用户名或密码不能为空'})

    def get(self, request):
        print(request.method)

        return HttpResponse({'code': 0, 'message': 'success'})


# @csrf_exempt
# def user(request):
#     if request.method == "POST":
#         print("-----------POST-------------")
#         obj = json.loads(request.body)
#         username = obj.get("username", "null")
#         password = obj.get("password", "null")
#         user = auth.authenticate(username=username, password=password)
#         # user = UserInfo.objects.get(userName=username, passWord=password)
#         if user:
#             auth.login(request, user)
#             request.session['user'] = username
#             # return JsonResponse({'code': 200, 'msg': '登录成功', 'user': username})
#             return HttpResponse(json.dumps({'code': 200, 'msg': 'success', 'user': username}), content_type="application/json")
#         else:
#             return JsonResponse({'message': 'username or password is error'})
#
# @csrf_exempt
# def get_info(request):
#     pass






# class Register(View):
#     def post(self, request):
#         try:
#             username = request.POST.get('username', None)
#             password = request.POST.get('password', None)
#             user = User.objects.create_user(username=username, password=password)
#             user.save()
#         except:
#             return JsonResponse({'code': 'no', 'message': '注册失败'})
#         return JsonResponse({'code': 'ok', 'message': '注册成功'})


