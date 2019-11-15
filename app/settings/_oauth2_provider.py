import os


OAUTH2_TOKEN_EXPIRES = os.environ.get(
    'OAUTH2_TOKEN_EXPIRES', 60 * 60 * 24 * 365)  # 1 year by default

OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'user.groups': 'Access to your groups',
        'user.emails': 'Access to your email address',
        'user.phones': 'Access to your phone number',
        'user.photo': 'Access to your profile photo',
        'user.full_name': 'Access to your full name',
        'user.description': 'Access to your profile description',
    },
    'ACCESS_TOKEN_EXPIRE_SECONDS': OAUTH2_TOKEN_EXPIRES,
}
