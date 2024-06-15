from django.urls import path
from weather.views import *
from user.viewsUser import *

urlpatterns = [
    path('', WeatherView.as_view(), name='Weather View'),
    path('generate', WeatherGenerate.as_view(), name='Weather Generate'),
    path('reset', WeatherReset.as_view(), name='Weather Reset'),
    path('edit/<id>/', WeatherEdit.as_view(), name='Weather Edit'),
    path('delete/<id>/', WeatherDelete.as_view(), name='Weather Delete'),
    path('filter', WeatherFilter.as_view(), name='Weather Filter'),
    path('login/', LoginView.as_view(), name='Weather Login'),
    path('user/generate', UserGenerate.as_view(), name='User Generate'),
    path('user/edit/<id>/', UserEdit.as_view(), name='User Edit'),
    path('user/delete/<id>/', UserDelete.as_view(), name='User Delete'),
    path('user/list/', UserList.as_view(), name='User List'),
    path('token', UserTokenizer.as_view(), name='User'),
    path('logout/', UserLogout.as_view(), name='Logout'),
]