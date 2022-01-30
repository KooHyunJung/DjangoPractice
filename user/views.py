from django.shortcuts import render, redirect
# 매가 가지고 있는 모델 중에 유저 모델을 가지고 오겠다
from .models import UserModel
# 사용자가 데이터베이스 안에 있는지 확인하는 함수
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import re

# 여기는 api 통신을 받고 기능이 실제로 움직이는 곳이다.
# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST':
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')

        if email == '' or username == '' or password == '':
            return render(request, 'user/signup.html', {'error': '빈 칸에 내용을 입력해 주세요!'})
        else:
            if not(6 < len(password) < 21):
                return render(request, 'user/signup.html', {'error': 'password 길이는 7~20자 입니다.'})
            elif re.search('[0-9]+', password) is None or re.search('[a-zA-Z]+', password) is None:
                return render(request, 'user/signup.html', {'error': 'password 형식은 영문,숫자 포함 7~20자 입니다.'})
            elif password != password2:
                return render(request, 'user/signup.html', {'error': 'password 확인 해 주세요!'})
            if re.search('[0-9]+', username) is None or re.search('[a-zA-Z]+', username) is None:
                return render(request, 'user/signup.html', {'error': 'nickname에 영문,숫자는 필수입니다.'})

            exist_user = get_user_model().objects.filter(username=username)
            exist_email = get_user_model().objects.filter(email=email)

            if exist_email:
                return render(request, 'user/signup.html', {'error': '이미 사용 중인 email입니다.'})
            elif exist_user:
                return render(request, 'user/signup.html', {'error': '이미 사용 중인 nickname입니다.'})
            else:
                UserModel.objects.create_user(email=email, username=username, password=password, bio=bio)
                return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        true_user = auth.authenticate(request, username=username, password=password)
        if true_user is not None:
            auth.login(request, true_user)
            return redirect('/')
        else:
            return render(request, 'user/signin.html', {'error': ' nicknam 또는 패스워드를 확인해주세요!'})


# @login_required : 사용자가 꼭 로그인 되어 있어야 접근 가능한 함수
@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')


# 유저 보여주기
@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})

# 팔로우 기능
@login_required
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')