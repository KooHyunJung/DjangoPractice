# 여기서 많은 작업이 이뤄진다.
from django.http import HttpResponse
from django.shortcuts import render

def base_response(request):
    return HttpResponse("안녕하세요 ! 저는 초기화면입니다 !") # 이걸 어떤 화면과 연결해 줄 것인가? -> usls.py

def first_view(request):
    return render(request, 'my_test.html')