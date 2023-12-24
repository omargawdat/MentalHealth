from enum import Enum

from django.utils.translation import gettext_lazy as _


class Gender(Enum):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')
    OTHER = 'O', _('Other')
    NOT_SPECIFIED = 'N', _('Prefer not to say')

    def __str__(self):
        return self.value[1]

    @classmethod
    def choices(cls):
        return [(key.value[0], key.name) for key in cls]
