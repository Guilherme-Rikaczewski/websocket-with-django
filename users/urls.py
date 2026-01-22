from django.urls import path
from users.views import (login_view, create_user, update_user, 
                         get_user, delete_user, logout_view,
                         csrf_view)

urlpatterns = [
    path('csrf/', csrf_view),
    path('login/', login_view),
    path('logout/', logout_view),
    path('register/', create_user),
    path('update/', update_user),
    path('delete/', delete_user),
    path('', get_user),
]
