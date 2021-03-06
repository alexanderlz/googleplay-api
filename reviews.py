#!/usr/bin/python

# Do not remove
GOOGLE_LOGIN = GOOGLE_PASSWORD = AUTH_TOKEN = None

import sys
import datetime
from pprint import pprint

from config import *
from googleplay import GooglePlayAPI
from helpers import sizeof_fmt

def print_header_line():
    l = [ "authorName",
            "url",
            "documentVersion",
            "timestampMsec",
            "starRating",
            "title",
            "comment",
            "commentId",
            "deviceName",
            "replyText",
            "replyTimestampMsec" ]
    print SEPARATOR.join(l)

def print_result_line(c):
    #c.offer[0].micros/1000000.0
    #c.offer[0].currencyCode
    l = [ 
            c.author.name,
            c.author.urls.url,
            c.documentVersion,
            datetime.datetime.utcfromtimestamp(c.timestampMsec/1000.0),
            c.starRating,
            c.title,
            c.comment.replace("\n", ' '),
            c.commentId,
            c.deviceName,
            c.replyText.replace("\n", ' '),
            c.replyTimestampMsec]
    print SEPARATOR.join(unicode(i).encode('utf8') for i in l)
    

if (len(sys.argv) < 2):
    print "Usage: %s request [package] [offset]" % sys.argv[0]
    print "Returns 20 reviews for a given app package."
    sys.exit(0)

request = sys.argv[1]
nb_res = 20
offset = 0

if (len(sys.argv) >= 3):
    offset = int(sys.argv[2])

api = GooglePlayAPI(ANDROID_ID)
api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)

try:
    reviews = api.reviews(request, False, 0, nb_res, offset)
except:
    print "Error: something went wrong. Maybe the nb_res you specified was too big?"
    sys.exit(1)

resp = reviews.getResponse
print_header_line()
try:
	for c in resp.review:
	    if c != None:
	        print_result_line(c)
except Exception,e:
	print e

