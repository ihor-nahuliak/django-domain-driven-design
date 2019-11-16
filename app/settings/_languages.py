from ._settings import DEBUG


def gettext_noop(s):
    """
    This is defined here as a do-nothing function because we can't import
    django.utils.translation -- that module depends on the settings.
    """
    return s


DEFAULT_LANGUAGE = 'en'

LANGUAGES = [
    ('en', gettext_noop('English')),
    ('es', gettext_noop('Spanish')),
    ('ca', gettext_noop('Catalan')),
]

MODELTRANSLATION_LANGUAGES = [lang for lang, _ in LANGUAGES]
MODELTRANSLATION_DEFAULT_LANGUAGE = DEFAULT_LANGUAGE

MODELTRANSLATION_DEBUG = DEBUG
