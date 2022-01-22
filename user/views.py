from django.shortcuts import render, redirect
# 매가 가지고 있는 모델 중에 유저 모델을 가지고 오겠다
from .models import UserModel
from django.http import HttpResponse
# 사용자가 데이터베이스 안에 있는지 확인하는 함수
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth.decorators import login_required

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
        # 데이터를 가지고 온다
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        bio = request.POST.get('bio', '')
        # password 확인
        if password != password2:
            # 비번이 같지 않을 때 알람 띄우기
            return render(request, 'user/signup.html', {'error':'패스워드 서로 다릅니다!'})
        else:
            if username == '' or password == '':
                return render(request, 'user/signup.html', {'error': '사용자이름/ 비밀번호를 입력해주세요!'})
            exist_user = get_user_model().objects.filter(username=username)
            # 중복 확인
            if exist_user:
                # 사용자가 존재하기 때문에 사용자를 저장하지 않고 회원가입 페이지를 다시 띄움
                return render(request, 'user/signup.html', {'error': f'{username} 이미 사용 중입니다'})
            else:
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, username=username, password=password)
        if me is not None:
            auth.login(request, me)
            return redirect('/')
        else:
            # 로그인 실패하면 다시 화면을 보여준다
            return render(request, 'user/signin.html', {'error': '이름 또는 패스워드를 확인해주세요!'})

    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')

# @login_required : 사용자가 꼭 로그인 되어 있어야 접근 가능하다는 함수
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