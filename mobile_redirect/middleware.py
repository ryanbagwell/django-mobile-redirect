import re
from django.conf import settings
from django.http import HttpResponsePermanentRedirect


class MobileRedirectMiddleware(object):
    """ Adobted from https://djangosnippets.org/snippets/2001/ """

    def process_request(self, request):
        is_mobile = False

        if 'HTTP_USER_AGENT' in request.META:
            user_agent = request.META['HTTP_USER_AGENT']

            patterns = [
                'up.browser',
                '|up.link',
                'mmp',
                'symbian',
                'smartphone',
                'midp',
                'wap',
                'phone',
                'windows ce',
                'pda',
                'mobile',
                'mini',
                'palm',
                'netfront',
                'android',
                'blackberry',
            ]

            pattern = "(%s)" % '|'.join(patterns)

            prog = re.compile(pattern, re.IGNORECASE)

            match = prog.search(user_agent)

            if match:
                is_mobile = True

        request.is_mobile = is_mobile

    def process_response(self, request, response):

        if request.is_mobile:

            return HttpResponsePermanentRedirect(settings.MOBILE_REDIRECT_URL)
        else:

            return response