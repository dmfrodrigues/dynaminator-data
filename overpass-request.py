#!/usr/bin/python3

import sys

import urllib.request
import urllib.parse

request_template_filepath = sys.argv[1]
date = sys.argv[2]
destination = sys.argv[3]

with open(request_template_filepath) as request_template_file:
    request_template = request_template_file.read()

request = request_template.replace("{date}", date)
request = urllib.parse.quote(request)

url = "http://overpass-api.de/api/interpreter?data=" + request

urllib.request.urlretrieve(
    url,
    destination
)
