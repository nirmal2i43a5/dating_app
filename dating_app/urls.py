from django.urls import path ,include
from dating_app.views import ChangePasswordView,Register,Login, ListUserDetail
from knox import views as knox_views
from .views import Logout

#for chat


from .chat_views import (
    ChatListView,
    ChatDetailView,
    ChatCreateView,
    ChatUpdateView,
    ChatDeleteView
)


app_name = 'chat'
urlpatterns = [
    path('api/register/', Register.as_view(), name='register'),
    path('api/listUser/', ListUserDetail, name='register'),
    path('api/login/', Login.as_view(), name='login'),
    path('api/logout/', Logout.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    

    #for chat urls
    path('chat/list/', ChatListView.as_view()),
    path('chat/create/', ChatCreateView.as_view()),
    path('chat/<pk>/', ChatDetailView.as_view()),
    path('<pk>/update/', ChatUpdateView.as_view()),
    path('<pk>/delete/', ChatDeleteView.as_view())
    
]
