from django.urls import path

from .views import AccountView, LoginUser, LogoutUser, RegisterUser, ProfileView, HistoryOrderView

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('login/', LoginUser.as_view(), name='login'),
    path('account/', AccountView.as_view(), name='account'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('historyorder/', HistoryOrderView.as_view(), name='historyorder'),
]
