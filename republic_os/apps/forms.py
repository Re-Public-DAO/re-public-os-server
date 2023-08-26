from django.contrib.auth import forms as admin_forms
from django.utils.translation import gettext_lazy as _

from republic_os.apps.models import App


class AppInstallAdminCreationForm(admin_forms.AppInstallAdminCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.AppInstallAdminCreationForm.Meta):
        model = App

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }
