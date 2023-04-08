from django.urls import path

from .views import AccountView, LoginUser, LogoutUser, ProfileEditView, HistoryOrderView, RegisterUser

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('login/', LoginUser.as_view(), name='login'),
    path('account/', AccountView.as_view(), name='account'),
    path('profile/', ProfileEditView.as_view(), name='profile'),
    path('historyorder/<int:pk>', HistoryOrderView.as_view(), name='historyOrder'),
]
