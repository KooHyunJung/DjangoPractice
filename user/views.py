from django.shortcuts import render, redirect
# 매가 가지고 있는 모델 중에 유저 모델을 가지고 오겠다
from .models import UserModel
from django.http import HttpResponse
# 사용자가 데이터베이스 안에 있는지 확인하는 함수
from django.contrib.auth import get_user_model
from django.contrib import auth

# 여기는 api 통신을 받고 기능이 실제로 움직이는 곳이다.
# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        return render(request, 'user/signup.html')
    elif request.method == 'POST':
        # 데이터를 가지고 온다
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        password2 = request.POST.get('password2', None)
        bio = request.POST.get('bio', None)
        # password 확인
        if password != password2:
            return render(request, 'user/signup.html')
        else:
            exist_user = get_user_model().objects.filter(username=username)
            # 중복 확인
            if exist_user:
                return render(request, 'user/signup.html')  # 사용자가 존재하기 때문에 사용자를 저장하지 않고 회원가입 페이지를 다시 띄움
            else:
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        me = auth.authenticate(request, username=username, password=password)
        if me is not None:
            auth.login(request, me)
            return HttpResponse(f"{me.username}님 로그인 성공")
        else:
            return redirect('/sign-in') # 로그인 실패하면 다시 화면을 보여준다

    elif request.method == 'GET':
        return render(request, 'user/signin.html')