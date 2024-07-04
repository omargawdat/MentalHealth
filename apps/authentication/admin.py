from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.decorators import display

from .models import CustomUser
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ['user_info', 'full_name', 'gender', 'age', 'user_status']
    list_filter = ['gender', 'user__is_verified', 'user__is_staff']
    search_fields = ['user__email', 'first_name', 'last_name']
    readonly_fields = ['user']

    @display(header=True)
    def user_info(self, obj):
        return [
            obj.user.email,
            _("Staff") if obj.user.is_staff else _("Regular User"),
            obj.user.email[:2].upper(),
            {
                "path": obj.image.url if obj.image else None,
                "squared": True,
                "borderless": True,
            }
        ]

    @display(description=_("Full Name"))
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    @display(description=_("Age"))
    def age(self, obj):
        if obj.birthdate:
            from datetime import date
            today = date.today()
            return today.year - obj.birthdate.year - (
                    (today.month, today.day) < (obj.birthdate.month, obj.birthdate.day))
        return _("N/A")

    @display(description=_("Status"), label={True: "success", False: "warning"})
    def user_status(self, obj):
        return obj.user.is_verified, _("Verified") if obj.user.is_verified else _("Unverified")


admin.site.register(CustomUser)
