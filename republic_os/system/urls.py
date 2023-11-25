from django.urls import path

from republic_os.system.views import (
    login,
    me,
    unlock,
    unlocked,
    test,
    get_version,
)

app_name = "system"
urlpatterns = [
    path("test/", view=test, name="test"),
    path("login/", view=login, name="login"),
    path("unlock/", view=unlock, name="unlock"),
    path("me/", view=me, name="me"),
    path("unlocked/", view=unlocked, name="unlocked"),
    path("version/", view=get_version, name="get_version"),
]
