#!/usr/bin/python -u
import time
import sys
import os
import traceback
import urlparse
import StringIO
import json
import time
import urllib2
import urllib
import ssl

args = urlparse.parse_qs(urlparse.urlparse(os.environ['REQUEST_URI']).query)

with open('/home/pyservices/server_creds.json', 'r') as f:
  creds = json.loads(f.read())

mycode = creds['verification_code']

if 'verify' in args:
  code = args['verify'][0]
  if code == mycode:
    print 'Content-type: text/plain'
    print 'Status: 204 No Content'
    print ''
  else:
    print 'Content-type: text/plain'
    print 'Status: 404 Not Found'
    print ''

print 'Content-type: text/plain'
print 'Status: 200 OK'
print ''

#print 'Got it'
#print args

body = sys.stdin.read()
if body != '':
  with open('/tmp/body.json', 'w') as f:
    f.write(body)

ssl._https_verify_certificates(enable=False)

def fetch_new_access_token(creds):
  url = "https://api.fitbit.com/oauth2/token"
  headers = {"Authorization": "Basic " + creds['basic_auth']}
  print 'Requesting: ' + url
  req = urllib2.Request(url, headers=headers, data=urllib.urlencode({'grant_type': 'refresh_token', 'refresh_token': creds['refresh_token']}))
  response = urllib2.urlopen(req)
  the_page = response.read()
  print 'Response code: ', response.getcode()
  print 'Response info: ', response.info()
  print 'Response: %s' % (the_page)
  body = json.loads(the_page)
  creds['access_token'] = body['access_token']
  creds['access_expiration'] = int(time.time()) + body['expires_in']
  creds['refresh_token'] = body['refresh_token']

ts = int(time.time())
if ts + 10 > creds['access_expiration']:
  fetch_new_access_token(creds)
  with open('/home/pyservices/server_creds.json', 'w') as f:
    f.write(json.dumps(creds))

access_token = creds['access_token']
url = "https://api.fitbit.com/1/user/-/profile.json"
headers = {"Authorization": "Bearer " + access_token, "Accept-Language": "en_US"}
#print 'Requesting: ' + url
req = urllib2.Request(url, headers=headers)
response = urllib2.urlopen(req)
the_page = response.read()
body = json.loads(the_page)
weight = body['user']['weight'] / 2.20462
print weight

http_logger = urllib2.HTTPSHandler() #debuglevel = 1)
#http_logger.set_http_debuglevel(1)
opener = urllib2.build_opener(http_logger) # put your other handlers here too!
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib2.install_opener(opener)

def auth():
    global creds
    # curl -X POST https://www.strava.com/api/v3/oauth/token -d client_id=20051 -d client_secret=[client_secret] -d code=[code] -d grant_type=authorization_code
    client_id = creds['strava_client_id']
    client_secret = creds['strava_client_secret']
    refresh_token = creds['strava_refresh_token']
    req = urllib2.Request('https://www.strava.com/api/v3/oauth/token', urllib.urlencode({'client_id': client_id, 'client_secret': client_secret, 'refresh_token': refresh_token, 'grant_type': 'refresh_token'}))
    response = urllib2.urlopen(req)
    return json.loads(response.read())['access_token']

def get(url):
    access_token = auth()
    #print 'Requesting:', url

    req = urllib2.Request(url, headers={"Authorization": "Bearer " + access_token})
    req.get_method = lambda: 'PUT'
    response = urllib2.urlopen(req)
    return json.loads(response.read())
    #except:
    #return []

athlete = get("https://www.strava.com/api/v3/athlete?weight=%f" % (weight))
#print athlete
