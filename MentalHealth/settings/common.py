import os
from datetime import timedelta
from pathlib import Path

from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = "django-insecure-b7*vx#_y*@s6n^t+g@1jvs%eixta52q+q=ge1l8$oh@u19*qv&"

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    'social_django',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.depression_test",
    "apps.authentication",
    "apps.core",
    "apps.journal",
    "apps.meditation",
    "apps.weekly",
    "apps.cbt",
    "apps.learning",
    "apps.plan",
    'apps.community',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "MentalHealth.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "MentalHealth.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Cairo"

USE_I18N = True

USE_TZ = True

# Media files (user-uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static Files Settings
STATICFILES_DIRS = [
    BASE_DIR / 'staticfiles',
]
STATIC_ROOT = BASE_DIR / 'static'
STATIC_URL = '/static/'

# Use Django's built-in FileSystemStorage
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "authentication.CustomUser"

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=600000),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': "q4UCfmqwZ16ccpmW0DEdsNw+a1mcFP1jn1Xb+tAQkfc=",
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",

    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "layout_boxed": False,
    "footer_fixed": False,

    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True,
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-info",
    "navbar": "navbar-gray-dark navbar-dark",
    "navbar_fixed": True,

}

# Geospatial Settings
GDAL_LIBRARY_PATH = os.getenv('GDAL_LIBRARY_PATH')
GEOS_LIBRARY_PATH = os.getenv('GEOS_LIBRARY_PATH')

# Local memory caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'omargawdat0@gmail.com'
EMAIL_HOST_PASSWORD = 'tgyd hcfp mzvd bech'
EMAIL_USE_TLS = True

DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024

UNFOLD = {
    "SITE_TITLE": "SoulSync",
    "SITE_HEADER": "SoulSync",
    "SITE_SYMBOL": "self_improvement",
    "SHOW_HISTORY": True,
    "COLORS": {
        "primary": {
            "50": "235 245 255",
            "100": "207 232 252",
            "200": "174 216 248",
            "300": "140 199 244",
            "400": "100 181 240",
            "500": "60 162 236",
            "600": "30 144 232",
            "700": "20 126 204",
            "800": "15 108 176",
            "900": "10 90 148",
            "950": "5 72 120",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Content Management",
                "items": [
                    {
                        "title": "Topics",
                        "icon": "subject",
                        "link": reverse_lazy("admin:plan_topic_changelist"),
                    },
                    {
                        "title": "Activities",
                        "icon": "directions_run",
                        "link": reverse_lazy("admin:plan_activity_changelist"),
                    },
                    {
                        "title": "Levels",
                        "icon": "bar_chart",
                        "link": reverse_lazy("admin:plan_level_changelist"),
                    },
                    {
                        "title": "Depression Activities",
                        "icon": "psychology",
                        "link": reverse_lazy("admin:plan_depactivity_changelist"),
                    },
                ],
            },
            {
                "title": "User Activities",
                "items": [
                    {
                        "title": "User Activities",
                        "icon": "assignment_ind",
                        "link": reverse_lazy("admin:plan_useractivity_changelist"),
                    },
                    {
                        "title": "User Depression Activities",
                        "icon": "mood",
                        "link": reverse_lazy("admin:plan_userdepactivity_changelist"),
                    },
                ],
            },
            {
                "title": "Education Management",
                "items": [
                    {
                        "title": "Topics",
                        "icon": "subject",
                        "link": reverse_lazy("admin:learning_topic_changelist"),
                    },
                    {
                        "title": "Subtopics",
                        "icon": "topic",
                        "link": reverse_lazy("admin:learning_subtopic_changelist"),
                    },
                    {
                        "title": "Lessons",
                        "icon": "menu_book",
                        "link": reverse_lazy("admin:learning_lesson_changelist"),
                    },
                    {
                        "title": "User Progress",
                        "icon": "trending_up",
                        "link": reverse_lazy("admin:learning_userprogress_changelist"),
                    },
                ],
            },
            {
                "title": "Journal Management",
                "items": [
                    {
                        "title": "Emotions",
                        "icon": "sentiment_satisfied_alt",
                        "link": reverse_lazy("admin:journal_emotion_changelist"),
                    },
                    {
                        "title": "Journal Entries",
                        "icon": "book",
                        "link": reverse_lazy("admin:journal_journalentry_changelist"),
                    },
                    {
                        "title": "Activities",
                        "icon": "directions_run",
                        "link": reverse_lazy("admin:journal_activity_changelist"),
                    },
                    {
                        "title": "Reasons",
                        "icon": "lightbulb",
                        "link": reverse_lazy("admin:journal_reason_changelist"),
                    },
                    {
                        "title": "Tags",
                        "icon": "local_offer",
                        "link": reverse_lazy("admin:journal_tag_changelist"),
                    },
                    {
                        "title": "Tips",
                        "icon": "tips_and_updates",
                        "link": reverse_lazy("admin:journal_tips_changelist"),
                    },
                ],
            },
            {
                "title": "Depression Test Management",
                "items": [
                    {
                        "title": "Test Questions",
                        "icon": "quiz",
                        "link": reverse_lazy("admin:depression_test_testquestion_changelist"),
                    },
                    {
                        "title": "Answer Options",
                        "icon": "check_box",
                        "link": reverse_lazy("admin:depression_test_answeroption_changelist"),
                    },
                    {
                        "title": "Test Attempts",
                        "icon": "analytics",
                        "link": reverse_lazy("admin:depression_test_depressiontestattempt_changelist"),
                    },
                ],
            },
            {
                "title": "Community Management",
                "items": [
                    {
                        "title": "Posts",
                        "icon": "post_add",
                        "link": reverse_lazy("admin:community_post_changelist"),
                    },
                    {
                        "title": "Comments",
                        "icon": "comment",
                        "link": reverse_lazy("admin:community_comment_changelist"),
                    },
                    {
                        "title": "Likes",
                        "icon": "thumb_up",
                        "link": reverse_lazy("admin:community_like_changelist"),
                    },
                ],
            },
            {
                "title": "User Management",
                "items": [
                    {
                        "title": "Profiles",
                        "icon": "person",
                        "link": reverse_lazy("admin:authentication_profile_changelist"),
                    },
                ],
            },
            {
                "title": "CBT Management",
                "items": [
                    {
                        "title": "Negative Thinking Types",
                        "icon": "psychology",
                        "link": reverse_lazy("admin:cbt_negativethinkingtype_changelist"),
                    },
                    {
                        "title": "CBT Questions",
                        "icon": "help",
                        "link": reverse_lazy("admin:cbt_cbtquestion_changelist"),
                    },
                ],
            },
            {
                "title": "Meditation Management",
                "items": [
                    {
                        "title": "Meditations",
                        "icon": "spa",
                        "link": reverse_lazy("admin:meditation_meditation_changelist"),
                    },
                ],
            },
            {
                "title": "Weekly Management",
                "items": [
                    {
                        "title": "Life Aspect Types",
                        "icon": "self_improvement",
                        "link": reverse_lazy("admin:weekly_lifeaspecttype_changelist"),
                    },
                    {
                        "title": "Life Aspects",
                        "icon": "nightlife",
                        "link": reverse_lazy("admin:weekly_lifeaspect_changelist"),
                    },
                    {
                        "title": "Life Activities",
                        "icon": "directions_run",
                        "link": reverse_lazy("admin:weekly_lifeactivity_changelist"),
                    },
                    {
                        "title": "Life Activity Tracks",
                        "icon": "insights",
                        "link": reverse_lazy("admin:weekly_lifeactivitytrack_changelist"),
                    },
                ],
            }
        ],
    }
}
