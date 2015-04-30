from django.test import TestCase
from django.test import Client
import requests
import xml.etree.ElementTree as ET
from django.conf import settings
import os


class MobileRedirectTests(TestCase):

    @classmethod
    def setUpClass(self):
        super(MobileRedirectTests, self).setUpClass()

        try:
            r = requests.get('http://browscap.org/stream?q=BrowsCapXML')
            tree = ET.fromstring(r.content)
        except Exception:
            print "Encountered exception when trying to download latest user agent strings. Using local data file instead."
            path = os.path.join(os.path.dirname(__file__), 'testdata', 'browscap.xml')
            tree = ET.parse(path)

        print "Compiling list of mobile phone user agent strings ..."

        self.mobile_phones = tree.findall("browsercapitems/browscapitem/item[@name='Device_Type'][@value='Mobile Phone']/..")

        print "Compiling list of mobile device user agent strings ..."

        self.mobile_devices = tree.findall("browsercapitems/browscapitem/item[@name='Device_Type'][@value='Mobile Device']/..")

        print "Compiling list of tablet user agent strings ..."

        self.tablet_devices = tree.findall("browsercapitems/browscapitem/item[@name='Device_Type'][@value='Tablet']/..")

        print "Compiling list of desktop user agent strings ..."

        self.desktop_devices = tree.findall("browsercapitems/browscapitem/item[@name='Device_Type'][@value='Desktop']/..")

    def test_mobile_phone_redirects(self):

        for device in self.mobile_phones:

            ua_string = device.attrib.get('name')

            c = Client(HTTP_USER_AGENT=ua_string)

            response = c.get('/')

            self.assertRedirects(response,
                                 settings.MOBILE_REDIRECT_URL,
                                 status_code=301,
                                 target_status_code=301,
                                 msg_prefix="Didn't correctly redirect for %s" % ua_string)

    def test_mobile_device_redirects(self):

        for device in self.mobile_devices:

            ua_string = device.attrib.get('name')

            c = Client(HTTP_USER_AGENT=ua_string)

            response = c.get('/')

            self.assertRedirects(response,
                                 settings.MOBILE_REDIRECT_URL,
                                 status_code=301,
                                 target_status_code=301,
                                 msg_prefix="Didn't correctly redirect for %s" % ua_string)

    def test_tablet_redirects(self):

        for device in self.tablet_devices:

            ua_string = device.attrib.get('name')

            c = Client(HTTP_USER_AGENT=ua_string)

            response = c.get('/')

            self.assertRedirects(response,
                                 settings.MOBILE_REDIRECT_URL,
                                 status_code=301,
                                 target_status_code=301,
                                 msg_prefix="Didn't correctly redirect for %s" % ua_string)

    def test_desktop_devices_do_not_redirect(self):

        for device in self.desktop_devices:

            ua_string = device.attrib.get('name')

            c = Client(HTTP_USER_AGENT=ua_string)

            response = c.get('/')

            self.assertEqual(response.status_code, 200,
                             msg_prefix="Unexected status code (%s) for Desktop device %s" % (response.status_code, ua_string))
