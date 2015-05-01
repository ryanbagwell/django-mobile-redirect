from django.test import TestCase
from django.test import Client
import requests
import xml.etree.ElementTree as ET
from django.conf import settings
import os
import json


def get_pruned_user_agents():

    try:
        r = requests.get('http://browscap.org/stream?q=BrowsCapJSON')
        data = json.loads(r.content)
    except Exception:
        print "Encountered exception when trying to download latest user agent strings. Using local data file instead."
        path = os.path.join(os.path.dirname(__file__), 'browscap.json')
        f = open(path, 'r')
        data = f.read()
        f.close()
        data = json.loads(data)

    """ Only test user agent strings from these families """
    parents = [
        'Chromium',
        'Maxthon',
        'Facebook',
        'Android WebView',
        'QQbrowser',
        'Yandex Browser',
        'Opera',
        'Google App',
        'UC Browser',
        'Iron',
        'Silk',
        'Midori',
        'RockMelt',
        'Chrome',
        'Qt',
        'YahooMobile',
        'NetFront',
        'Airmail',
        'OneBrowser',
        'iBrowser',
        'IEMobile',
        'Nokia',
        'Android',
        'Mercury',
        'Mobile',
        'Safari',
        'Instagram',
        'Adobe Air',
        'Atomic',
        'Blackberry',
        'IE',
        'Thunderbird',
        'FirefoxOS',
        'Firefox',
        'Comodo Dragon',
        'Motorola',
        'Mozilla',
    ]

    """ Specific strings to exclude """
    exclude = [
        'Android?2.3*i9999_custom',
        'Android?2.3*i9988_custom',
        'Android?2.2*NBPC724',
        'MSN Mobile Proxy',
    ]

    pruned = {}

    def should_exclude(ua):

        for e in exclude:
            if e in ua:
                return True
        return False

    for ua, props in data.items():

        if 'comments' in ua:
            continue

        if should_exclude(ua):
            continue

        try:

            props = json.loads(props)

            parent = props.get('Parent')

            dtype = props.get('Device_Type')

            if dtype not in dtype in ['Mobile Phone', 'Tablet', 'Desktop']:
                continue

            for x in parents:

                if x in parent:
                    pruned[ua] = props
        except:
            pass

    return pruned


class MobileRedirectTests(TestCase):

    @classmethod
    def setUpClass(self):

        super(MobileRedirectTests, self).setUpClass()

        user_agents = get_pruned_user_agents()

        print "Compiling list of mobile phone user agent strings ..."

        self.mobile_phones = [k for k, v in user_agents.items() if v['Device_Type'] == 'Mobile Phone']

        print "Compiling list of tablet user agent strings ..."

        self.tablet_devices = [k for k, v in user_agents.items() if v['Device_Type'] == 'Tablet']

        print "Compiling list of desktop user agent strings ..."

        self.desktop_devices = [k for k, v in user_agents.items() if v['Device_Type'] == 'Desktop']

    def test_mobile_phone_redirects(self):

        count = 1

        for ua_string in self.mobile_phones:

            c = Client(HTTP_USER_AGENT=ua_string)

            response = c.get('/')

            self.assertRedirects(response,
                                 settings.MOBILE_REDIRECT_URL,
                                 status_code=301,
                                 target_status_code=301,
                                 msg_prefix="Didn't correctly redirect for %s (test %s of %s)" % (ua_string, count, len(self.mobile_phones)))

            count = count + 1

    def test_tablet_redirects(self):

        count = 1

        for ua_string in self.tablet_devices:

            c = Client(HTTP_USER_AGENT=ua_string)

            response = c.get('/')

            self.assertRedirects(response,
                                 settings.MOBILE_REDIRECT_URL,
                                 status_code=301,
                                 target_status_code=301,
                                 msg_prefix="Didn't correctly redirect for %s (test %s of %s)" % (ua_string, count, len(self.tablet_devices)))

            count = count + 1

    def test_desktop_devices_do_not_redirect(self):

        count = 1

        for ua_string in self.desktop_devices:

            c = Client(HTTP_USER_AGENT=ua_string)

            response = c.get('/')

            self.assertEqual(response.status_code, 200,
                             msg="Unexected status code (%s) for Desktop device %s (test %s of %s)" % (response.status_code, ua_string, count, len(self.desktop_devices)))

            count = count + 1
