import os


OAUTH2_TOKEN_EXPIRES = os.getenv('OAUTH2_TOKEN_EXPIRES', '31536000')  # 1 year

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
