import re
from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class MobileRedirectMiddleware(object):
    """ Adobted from https://djangosnippets.org/snippets/2001/ """

    def process_request(self, request):

        request.is_mobile = False

        if 'HTTP_USER_AGENT' in request.META:
            user_agent = request.META['HTTP_USER_AGENT']

            patterns = [
                'up.browser',
                'up.link',
                'mmp',
                'symbian',
                'smartphone',
                'midp',
                'wap',
                'phone',
                'pda',
                'mobile',
                'mini',
                'palm',
                'netfront',
                'android',
                'blackberry',
                'WordPress App',
                'wp-iphone',
                'pluckItCrawler',
                'tablet',
                'SAMSUNG-SGH-i900',
                'Facebook App 29.0',
                'ipad',
                'iOS',
                '^Flipboard App .*$',
                'Flixster App .*$',
                'GT-P3100',
                '!NBPC724',
            ]

            pattern = "(%s)" % '|'.join(patterns)

            prog = re.compile(pattern, re.IGNORECASE)

            match = prog.search(user_agent)

            if match:
                request.is_mobile = True

    def process_response(self, request, response):

        if request.is_mobile:

            return HttpResponsePermanentRedirect(settings.MOBILE_REDIRECT_URL)
        else:

            return response
