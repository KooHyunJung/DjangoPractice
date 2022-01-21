#user/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
# 장고에서 사용하는 기본 유저 모델, 클래스를 import한 것이다
from django.conf import settings

# Create your models here.
# 클래스를 클래스에 상속
class UserModel(AbstractUser):
    class Meta:
        db_table = "my_user" # 여기는 테이블 이름
    # 나 원래 있던 모델을 가지고 왔고 거기에 bio만 추가 했다
    bio = models.TextField(max_length=500, blank=True)
    # follow 변수 안에 들어가는 정보는 사용자 정보이다
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee')

