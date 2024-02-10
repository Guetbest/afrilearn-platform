# -*- coding: utf-8 -*-
import os
from lms.envs.production import *

####### Settings common to LMS and CMS
import json
import os

from xmodule.modulestore.modulestore_settings import update_module_store_settings

# Mongodb connection parameters: simply modify `mongodb_parameters` to affect all connections to MongoDb.
mongodb_parameters = {
    "db": "openedx",
    "host": "mongodb",
    "port": 27017,
    "user": None,
    "password": None,
    # Connection/Authentication
    "ssl": False,
    "authsource": "admin",
    "replicaSet": None,
    
}
DOC_STORE_CONFIG = mongodb_parameters
CONTENTSTORE = {
    "ENGINE": "xmodule.contentstore.mongo.MongoContentStore",
    "ADDITIONAL_OPTIONS": {},
    "DOC_STORE_CONFIG": DOC_STORE_CONFIG
}
# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)
DATA_DIR = "/openedx/data/modulestore"

for store in MODULESTORE["default"]["OPTIONS"]["stores"]:
   store["OPTIONS"]["fs_root"] = DATA_DIR

# Behave like memcache when it comes to connection errors
DJANGO_REDIS_IGNORE_EXCEPTIONS = True

# Elasticsearch connection parameters
ELASTIC_SEARCH_CONFIG = [{
  
  "host": "elasticsearch",
  "port": 9200,
}]

# Common cache config
CACHES = {
    "default": {
        "KEY_PREFIX": "default",
        "VERSION": "1",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "general": {
        "KEY_PREFIX": "general",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "mongo_metadata_inheritance": {
        "KEY_PREFIX": "mongo_metadata_inheritance",
        "TIMEOUT": 300,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "configuration": {
        "KEY_PREFIX": "configuration",
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "celery": {
        "KEY_PREFIX": "celery",
        "TIMEOUT": 7200,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
    "course_structure_cache": {
        "KEY_PREFIX": "course_structure",
        "TIMEOUT": 7200,
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@redis:6379/1",
    },
}

# The default Django contrib site is the one associated to the LMS domain name. 1 is
# usually "example.com", so it's the next available integer.
SITE_ID = 2

# Contact addresses
CONTACT_MAILING_ADDRESS = "Afrilearn Platform - https://www.benouind.io"
DEFAULT_FROM_EMAIL = ENV_TOKENS.get("DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS.get("DEFAULT_FEEDBACK_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
SERVER_EMAIL = ENV_TOKENS.get("SERVER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
TECH_SUPPORT_EMAIL = ENV_TOKENS.get("TECH_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
CONTACT_EMAIL = ENV_TOKENS.get("CONTACT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BUGS_EMAIL = ENV_TOKENS.get("BUGS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
UNIVERSITY_EMAIL = ENV_TOKENS.get("UNIVERSITY_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PRESS_EMAIL = ENV_TOKENS.get("PRESS_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
PAYMENT_SUPPORT_EMAIL = ENV_TOKENS.get("PAYMENT_SUPPORT_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
BULK_EMAIL_DEFAULT_FROM_EMAIL = ENV_TOKENS.get("BULK_EMAIL_DEFAULT_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_MANAGER_EMAIL = ENV_TOKENS.get("API_ACCESS_MANAGER_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])
API_ACCESS_FROM_EMAIL = ENV_TOKENS.get("API_ACCESS_FROM_EMAIL", ENV_TOKENS["CONTACT_EMAIL"])

# Get rid completely of coursewarehistoryextended, as we do not use the CSMH database
INSTALLED_APPS.remove("lms.djangoapps.coursewarehistoryextended")
DATABASE_ROUTERS.remove(
    "openedx.core.lib.django_courseware_routers.StudentModuleHistoryExtendedRouter"
)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/media/"

# Video settings
VIDEO_IMAGE_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS["STORAGE_KWARGS"]["location"] = MEDIA_ROOT

GRADES_DOWNLOAD = {
    "STORAGE_TYPE": "",
    "STORAGE_KWARGS": {
        "base_url": "/media/grades/",
        "location": "/openedx/media/grades",
    },
}

# ORA2
ORA2_FILEUPLOAD_BACKEND = "filesystem"
ORA2_FILEUPLOAD_ROOT = "/openedx/data/ora2"
FILE_UPLOAD_STORAGE_BUCKET_NAME = "openedxuploads"
ORA2_FILEUPLOAD_CACHE_NAME = "ora2-storage"

# Change syslog-based loggers which don't work inside docker containers
LOGGING["handlers"]["local"] = {
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "all.log"),
    "formatter": "standard",
}
LOGGING["handlers"]["tracking"] = {
    "level": "DEBUG",
    "class": "logging.handlers.WatchedFileHandler",
    "filename": os.path.join(LOG_DIR, "tracking.log"),
    "formatter": "standard",
}
LOGGING["loggers"]["tracking"]["handlers"] = ["console", "local", "tracking"]

# Silence some loggers (note: we must attempt to get rid of these when upgrading from one release to the next)
LOGGING["loggers"]["blockstore.apps.bundles.storage"] = {"handlers": ["console"], "level": "WARNING"}

# These warnings are visible in simple commands and init tasks
import warnings
from django.utils.deprecation import RemovedInDjango40Warning, RemovedInDjango41Warning
warnings.filterwarnings("ignore", category=RemovedInDjango40Warning)
warnings.filterwarnings("ignore", category=RemovedInDjango41Warning)
warnings.filterwarnings("ignore", category=DeprecationWarning, module="wiki.plugins.links.wiki_plugin")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="boto.plugin")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="botocore.vendored.requests.packages.urllib3._collections")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pkg_resources")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="fs")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="fs.opener")
SILENCED_SYSTEM_CHECKS = ["2_0.W001", "fields.W903"]

# Email
EMAIL_USE_SSL = False
# Forward all emails from edX's Automated Communication Engine (ACE) to django.
ACE_ENABLED_CHANNELS = ["django_email"]
ACE_CHANNEL_DEFAULT_EMAIL = "django_email"
ACE_CHANNEL_TRANSACTIONAL_EMAIL = "django_email"
EMAIL_FILE_PATH = "/tmp/openedx/emails"

# Language/locales
LOCALE_PATHS.append("/openedx/locale/contrib/locale")
LOCALE_PATHS.append("/openedx/locale/user/locale")
LANGUAGE_COOKIE_NAME = "openedx-language-preference"

# Allow the platform to include itself in an iframe
X_FRAME_OPTIONS = "SAMEORIGIN"


JWT_AUTH["JWT_ISSUER"] = "https://www.benouind.io/oauth2"
JWT_AUTH["JWT_AUDIENCE"] = "openedx"
JWT_AUTH["JWT_SECRET_KEY"] = "VcTh8nSe41YiDKBnMb15sjkM"
JWT_AUTH["JWT_PRIVATE_SIGNING_JWK"] = json.dumps(
    {
        "kid": "openedx",
        "kty": "RSA",
        "e": "AQAB",
        "d": "H1tgQ23UO6B8N3NbAwk3OG1xfJq-1j7WtDT-3-pCmbKqm83qOs27KwffyJhVS50rjstt0-kukCG9ktkQTVS0171ipWR-1ft9RTaV7pJpUDKOIPBe5_OY-4KRT_nNO1tA-b0yHpTEi84-blsKjd9_0V_pHf07F4wcNH0LiiEie0z-F8CEOuyHiRiJJ73POxsO5xYXSwkBVdLZuT3AV_aFUhiMOohXi0g4vz49Swdrz3_IDzRfw73kVZWWc6Mz3u0xPVy8VKWsMRqERgt3X0_rx0n1TXzg9tti2wFHaGFBYl6c2sHkllZKiRgpcklepactWO2C3bBN-tuoXRVlV-Aq2Q",
        "n": "msauQWvcDNrVVxK9erd2DwhRZ3l8nvGzzavmJI8SsR41jTtbPZxgOb8i0gb_Lfbw_UCS1FHWKrZyrIRdewpKJJ5XQqWHj_w04Z7T79lvsgayWzoPmrVuM318OgSXwwFOz1Q-lLq8hNIqI9Us_W1TUbxGuEXRLp12BPDRJDtbnu_LrAxT6vG5TeY4wKYYgaPI769NNW3huufiVoY53eELJSWFR17FAOmdvS7ae9eGjq3ISQxFm3f_y9izRUfOSMoR5p4Z_ecjhkqXSUodMc0137Mt6eLzFhNoywYJFkthFQve7s1DWyTeTjRqfXR45KYdzmfJTiZdHMUIr7SieEiH8w",
        "p": "xOIsOINvbPL1OZEbqMf9ip1V-C6Oor4zWmj0eLz6TyLgetZScv0LKD2ivqzpa1iAJK6g9DFbKjNPo85WKcmXJl36rxn1Qs4ZMH-kX0IpPL4BVlWHTGZ146dLT1fEVv9Fq_CligawB31oYGR6w_t8o5C4m02aRsBXrTDSxnxqsKk",
        "q": "yT_XroR7oL6fFmAF2lvkJ1sECVZ-6Y628yV75ecDdQ2yMUMGDXq11_JEmH3ep-ebhNTXVE3r0j3PtsdNlSWcF-DeE1HOcWMfUYx7-0DMENLXcBJpd3j6AXRIH161bvMn3IfkWbPhDgJJcMmq6s9FeR7i077CD350fKxSa_Ko6Ts",
    }
)
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "AQAB",
                "n": "msauQWvcDNrVVxK9erd2DwhRZ3l8nvGzzavmJI8SsR41jTtbPZxgOb8i0gb_Lfbw_UCS1FHWKrZyrIRdewpKJJ5XQqWHj_w04Z7T79lvsgayWzoPmrVuM318OgSXwwFOz1Q-lLq8hNIqI9Us_W1TUbxGuEXRLp12BPDRJDtbnu_LrAxT6vG5TeY4wKYYgaPI769NNW3huufiVoY53eELJSWFR17FAOmdvS7ae9eGjq3ISQxFm3f_y9izRUfOSMoR5p4Z_ecjhkqXSUodMc0137Mt6eLzFhNoywYJFkthFQve7s1DWyTeTjRqfXR45KYdzmfJTiZdHMUIr7SieEiH8w",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "https://www.benouind.io/oauth2",
        "AUDIENCE": "openedx",
        "SECRET_KEY": "VcTh8nSe41YiDKBnMb15sjkM"
    }
]

# Enable/Disable some features globally
FEATURES["ENABLE_DISCUSSION_SERVICE"] = False
FEATURES["PREVENT_CONCURRENT_LOGINS"] = False
FEATURES["ENABLE_CORS_HEADERS"] = True

# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_INSECURE = False
CORS_ALLOW_HEADERS = corsheaders_default_headers + ('use-jwt-cookie',)

# Add your MFE and third-party app domains here
CORS_ORIGIN_WHITELIST = []

# Disable codejail support
# explicitely configuring python is necessary to prevent unsafe calls
import codejail.jail_code
codejail.jail_code.configure("python", "nonexistingpythonbinary", user=None)
# another configuration entry is required to override prod/dev settings
CODE_JAIL = {
    "python_bin": "nonexistingpythonbinary",
    "user": None,
}

FEATURES["ENABLE_DISCUSSION_SERVICE"] = True
# Student notes
FEATURES["ENABLE_EDXNOTES"] = True
######## End of settings common to LMS and CMS

######## Common LMS settings
LOGIN_REDIRECT_WHITELIST = ["studio.www.benouind.io"]

# Better layout of honor code/tos links during registration
REGISTRATION_EXTRA_FIELDS["terms_of_service"] = "hidden"
REGISTRATION_EXTRA_FIELDS["honor_code"] = "hidden"

# Fix media files paths
PROFILE_IMAGE_BACKEND["options"]["location"] = os.path.join(
    MEDIA_ROOT, "profile-images/"
)

COURSE_CATALOG_VISIBILITY_PERMISSION = "see_in_catalog"
COURSE_ABOUT_VISIBILITY_PERMISSION = "see_about_page"

# Allow insecure oauth2 for local interaction with local containers
OAUTH_ENFORCE_SECURE = False

# Email settings
DEFAULT_EMAIL_LOGO_URL = LMS_ROOT_URL + "/theming/asset/images/logo.png"
BULK_EMAIL_SEND_USING_EDX_ACE = True
FEATURES["ENABLE_FOOTER_MOBILE_APP_LINKS"] = False

# Branding
MOBILE_STORE_ACE_URLS = {}
SOCIAL_MEDIA_FOOTER_ACE_URLS = {}

# Make it possible to hide courses by default from the studio
SEARCH_SKIP_SHOW_IN_CATALOG_FILTERING = False

# Caching
CACHES["staticfiles"] = {
    "KEY_PREFIX": "staticfiles_lms",
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    "LOCATION": "staticfiles_lms",
}

# Create folders if necessary
for folder in [DATA_DIR, LOG_DIR, MEDIA_ROOT, STATIC_ROOT_BASE, ORA2_FILEUPLOAD_ROOT]:
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

# MFE: enable API and set a low cache timeout for the settings. otherwise, weird
# configuration bugs occur. Also, the view is not costly at all, and it's also cached on
# the frontend. (5 minutes, hardcoded)
ENABLE_MFE_CONFIG_API = True
MFE_CONFIG_API_CACHE_TIMEOUT = 1

# MFE-specific settings


FEATURES['ENABLE_AUTHN_MICROFRONTEND'] = True





FEATURES['ENABLE_NEW_BULK_EMAIL_EXPERIENCE'] = True














# Student notes
EDXNOTES_CLIENT_NAME = "notes"

######## End of common LMS settings

ALLOWED_HOSTS = [
    ENV_TOKENS.get("LMS_BASE"),
    FEATURES["PREVIEW_LMS_BASE"],
    "lms",
]
CORS_ORIGIN_WHITELIST.append("https://www.benouind.io")


# Properly set the "secure" attribute on session/csrf cookies. This is required in
# Chrome to support samesite=none cookies.
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "None"


# CMS authentication
IDA_LOGOUT_URI_LIST.append("https://studio.www.benouind.io/logout/")

# Required to display all courses on start page
SEARCH_SKIP_ENROLLMENT_START_DATE_FILTERING = True

# Dynamic config API settings
# https://openedx.github.io/frontend-platform/module-Config.html
MFE_CONFIG = {
    "BASE_URL": "apps.www.benouind.io",
    "CSRF_TOKEN_API_PATH": "/csrf/api/v1/token",
    "CREDENTIALS_BASE_URL": "",
    "DISCOVERY_API_BASE_URL": "",
    "FAVICON_URL": "https://www.benouind.io/favicon.ico",
    "INFO_EMAIL": "postmaster@benouind.io",
    "LANGUAGE_PREFERENCE_COOKIE_NAME": "openedx-language-preference",
    "LMS_BASE_URL": "https://www.benouind.io",
    "LOGIN_URL": "https://www.benouind.io/login",
    "LOGO_URL": "https://www.benouind.io/theming/asset/images/logo.png",
    "LOGO_WHITE_URL": "https://www.benouind.io/theming/asset/images/logo.png",
    "LOGO_TRADEMARK_URL": "https://www.benouind.io/theming/asset/images/logo.png",
    "LOGOUT_URL": "https://www.benouind.io/logout",
    "MARKETING_SITE_BASE_URL": "https://www.benouind.io",
    "PASSWORD_RESET_SUPPORT_LINK": "mailto:postmaster@benouind.io",
    "REFRESH_ACCESS_TOKEN_ENDPOINT": "https://www.benouind.io/login_refresh",
    "SITE_NAME": "Afrilearn Platform",
    "STUDIO_BASE_URL": "https://studio.www.benouind.io",
    "USER_INFO_COOKIE_NAME": "user-info",
    "ACCESS_TOKEN_COOKIE_NAME": "edx-jwt-cookie-header-payload",
}

# MFE-specific settings


AUTHN_MICROFRONTEND_URL = "https://apps.www.benouind.io/authn"
AUTHN_MICROFRONTEND_DOMAIN  = "apps.www.benouind.io/authn"
MFE_CONFIG["DISABLE_ENTERPRISE_LOGIN"] = True



ACCOUNT_MICROFRONTEND_URL = "https://apps.www.benouind.io/account"
MFE_CONFIG["ACCOUNT_SETTINGS_URL"] = ACCOUNT_MICROFRONTEND_URL



COMMUNICATIONS_MICROFRONTEND_URL = "https://apps.www.benouind.io/communications"
MFE_CONFIG["SCHEDULE_EMAIL_SECTION"] = True



MFE_CONFIG["ENABLE_NEW_EDITOR_PAGES"] = True
MFE_CONFIG["ENABLE_PROGRESS_GRAPH_SETTINGS"] = True



DISCUSSIONS_MICROFRONTEND_URL = "https://apps.www.benouind.io/discussions"
DISCUSSIONS_MFE_FEEDBACK_URL = None



WRITABLE_GRADEBOOK_URL = "https://apps.www.benouind.io/gradebook"



LEARNING_MICROFRONTEND_URL = "https://apps.www.benouind.io/learning"
MFE_CONFIG["LEARNING_BASE_URL"] = "https://apps.www.benouind.io/learning"



ORA_GRADING_MICROFRONTEND_URL = "https://apps.www.benouind.io/ora-grading"



PROFILE_MICROFRONTEND_URL = "https://apps.www.benouind.io/profile/u/"
MFE_CONFIG["ACCOUNT_PROFILE_URL"] = "https://apps.www.benouind.io/profile"



LOGIN_REDIRECT_WHITELIST.append("apps.www.benouind.io")
CORS_ORIGIN_WHITELIST.append("https://apps.www.benouind.io")
CSRF_TRUSTED_ORIGINS.append("apps.www.benouind.io")



EDXNOTES_PUBLIC_API = "https://notes.www.benouind.io/api/v1"
EDXNOTES_INTERNAL_API = "http://notes:8000/api/v1"