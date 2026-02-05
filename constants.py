import re


URL_REG = r'^https?://[^\s/$.?#].[^\s]*$'

EXCLUDE_REG = [
    re.compile(r'.*\.pdf$', re.IGNORECASE),
    re.compile(r'.*(login|registration|auth|reset-password).*'),
    re.compile(r'.*\?.*'),
    re.compile(r'.*\.(jpg|jpeg|png|zip)$'),
]
EMAIL_REG = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
PHONE_REG = r'((?:\+7|8)[- _]*\(?\d{3}\)?[- _]*\d{3}[- _]*\d{2}[- _]*\d{2})'

BASE_OPTIONS = {
    'strategy': 'same-domain',
    'exclude': EXCLUDE_REG,
}
