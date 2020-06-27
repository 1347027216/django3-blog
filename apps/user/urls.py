from django.urls import path

from .views import UserLoginView

from .views import UserRegisterView

from .views import UserActivateView

from .views import UserLogoutView

from .views import UserPasswordForgetView

from .views import UserPasswordVerificationView

from .views import UserPasswordRestView

from .views import UserCollectionView

from .views import UserPersonCenterView

urlpatterns = [

    path('sign-in/', UserLoginView.as_view(),name="login"),

    path('sign-up/', UserRegisterView.as_view(), name="register"),

    # 活跃验证
    path('sign-up/activate/<str:activate_code>/', UserActivateView.as_view(), name="activate"),

    # 退出登录
    path('logout/', UserLogoutView.as_view(), name="logout"),

    # 密码找回
    path('forget/', UserPasswordForgetView.as_view(), name="forget"),

    # 用户收藏
    path('collection/', UserCollectionView.as_view(), name="user-collection"),

    path('person-center/', UserPersonCenterView.as_view(), name="user-person-center"),

    path('forget/verification/<str:activate_code>', UserPasswordVerificationView.as_view(), name="password-verification"),
    path('forget/reset/', UserPasswordRestView.as_view(), name="password-reset"),

]
