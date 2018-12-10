from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import *


urlpatterns = [
    path('', IndexView.as_view(), name='indexview'),
    path('signup/', SignUpView.as_view(), name='signupview'),
    path('login/', LoginView.as_view(), name = 'loginview'),
    path('home/', HomeView.as_view(), name = 'homeview'),
    path('logout/', LogoutView.as_view(), name='logoutview'),
    path('edit/', EditView.as_view(), name='editview'),
    path('profile/(?P<id>.*)/', UserProfileView.as_view(), name='profileview'),

    path('postproject/', PostProjectView.as_view(), name='post_project_view'),
    path('deleteproject/(?P<id>.*)/', DeleteProjectView.as_view(), name='deleteprojectview'),
    path('editproject/(?P<id>.*)/', EditProjectView.as_view(), name='editprojectview'),
    path('projectbids/(?P<id>.*)/', BidsProjectView.as_view(), name='projectbidsview'),
    path('project/(?P<id>.*)/', ProjectDetailView.as_view(), name='project_detail_view'),

    path('userbids/(?P<id>.*)/', UserBidView.as_view(), name='userbidsview'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
