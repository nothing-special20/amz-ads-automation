from django.conf import settings
from django.contrib.sites.models import Site


def get_protocol(is_secure: bool = settings.USE_HTTPS_IN_ABSOLUTE_URLS) -> str:
    return f'http{"s" if is_secure else ""}'


def absolute_url(relative_url: str, is_secure: bool = settings.USE_HTTPS_IN_ABSOLUTE_URLS):
    return f'{get_protocol(is_secure)}://{Site.objects.get_current().domain}{relative_url}'
