from django.urls import path

from republic_os.apps.views import (
    get_storage_info,
    get_file_browser_contents,
    get_file_contents,
)

app_name = "apps"
urlpatterns = [
    path("<str:republic_id>/info/", view=get_storage_info, name="get_storage_info"),
    path("<str:republic_id>/files/", view=get_file_browser_contents, name="get_file_browser_contents"),
    path("<str:republic_id>/content/", view=get_file_contents, name="get_file_contents")
]
