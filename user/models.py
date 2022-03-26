from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
# 클래스를 클래스에 상속
class UserModel(AbstractUser):
    class Meta:
        db_table = "my_user" # 여기는 테이블 이름
    bio = models.TextField(max_length=500, blank=True)
    image = models.CharField(max_length=256, blank=True)
    # follow 변수 안에 들어가는 정보는 사용자 정보이다
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee')

