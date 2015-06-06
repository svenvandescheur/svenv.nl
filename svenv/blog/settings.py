BLOG_TITLE = 'Svenv.nl'
BLOG_DESCRIPTION = 'Blogposts about tech related subject like Unix, Linux, Docker and programming.'

BASE_URL = 'http://svenv.nl'

CONTACT_THANK_YOU_PAGE = '/thankyou'
EMAIL = 'svenvandescheur@gmail.com'
EMAIL_FROM = 'noreply@svenv.nl'
SMTP_HOST = 'localhost'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.OrderingFilter',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
}