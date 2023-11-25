from django.urls import path

from republic_os.oauth.views import get_oauth
from republic_os.oauth.api.views import OAuthStateViewSet

app_name = "oauth"
urlpatterns = [
    path('', OAuthStateViewSet.as_view({'get': 'list', 'post': 'create'}), name='get_list_create_oauth'),
    path('<str:republic_id>/', get_oauth, name='get_oauth'),
]