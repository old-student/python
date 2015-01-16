import os
import sys
import getpass
import urllib2
import urllib
from selenium import webdriver
import json

print 'VK music downloader by Dimon'


def check_connection():
    try:
        urllib2.urlopen('http://www.google.com', timeout = 1)
        return True
    except urllib2.URLError as err: pass
    return False


def get_access_attributes(login, password):
    try:
        driver = webdriver.Firefox()
        payload = {
            'client_id': 4591034,
            'scope': 'audio',
            'redirect_uri': 'https://oauth.vk.com/blank.html',
            'display': 'page',
            'response_type': 'token',
        }
        driver.get("https://oauth.vk.com/authorize?%s" % urllib.urlencode(payload))
        driver.find_element_by_name("email").send_keys(vk_login)
        driver.find_element_by_name("pass").send_keys(vk_password)
        driver.find_element_by_id("install_allow").click()
        driver.close()

        access_list = (driver.current_url.split("#"))[1].split("&")
        return dict(access_token=(access_list[0].split("="))[1],
                    expires_in=(access_list[1].split("="))[1],
                    user_id=(access_list[2].split("="))[1])
    except:
        driver.close()
        return None


def get_audio_list(access_attr):
    url = "https://api.vk.com/method/audio.get?" + \
          "uid=" + access_attr['user_id'] + "&access_token=" + access_attr['access_token']
    return (json.loads(urllib2.urlopen(url).read()))['response']

# main execution

if not check_connection():
    print 'Not connected to Internet'
    exit()

vk_login = raw_input('Please enter your VK login: ')
vk_password = getpass.getpass('Please enter your VK password: ') if sys.stdin.isatty() \
    else raw_input('Please enter your VK password: ').rstrip()

access_attributes = get_access_attributes(vk_login, vk_password)
if access_attributes is None:
    print 'Could not get VK authorization information properly'
    exit()

path = os.path.join(os.path.dirname(__file__), 'Download' + access_attributes['user_id'])
if not os.path.exists(path):
    os.makedirs(path)

for audio_record in get_audio_list(access_attributes):
    filename = os.path.join(path, "%s-%s.mp3" % (audio_record['artist'], audio_record['title']))
    if not os.path.exists(filename):
        print 'Downloading => ' + filename
        try:
            urllib.urlretrieve(audio_record['url'].split("?")[0], filename)
        except:
            print 'Error occurred by processing audio ' + filename + '. Try change the name in VK.'




