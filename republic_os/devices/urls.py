from django.urls import path

from republic_os.devices.views import (
    add_device,
    generate_qr_code,
    check_for_device,
)

app_name = "devices"
urlpatterns = [
    path("add/", view=add_device, name="add_device"),
    path("generate-qr-code/", view=generate_qr_code, name="generate_qr_code"),
    path("check/", view=check_for_device, name="check_for_device"),
]