# user 앱의 모든 url을 관리해 준다
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.sign_up_view, name='sign-up'),
    path('sign-in/', views.sign_in_view, name='sign-in'),
    path('logout/', views.logout, name='logout'),
    path('user/', views.user_view, name='user-list'),
    path('user/follow/<int:id>/', views.user_follow, name='user-follow'),

    path('edit/<int:pk>', views.edit, name='edit'),

    #=============== 장고 인증 URL + 템플릿 연결 ================#
    # 장고 인증 URL 넘어가기 위한 버튼 연결
    path('accounts/login/', views.accounts_login, name='accounts-login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),
         name='password_reset_complete'),

    # 장고 기본 URL
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]