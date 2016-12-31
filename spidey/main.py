#!/usr/bin/env python

import sys
import re
import os
import json
from distutils.dir_util import mkpath
import argparse
import urllib2
import requests
from urlparse import urlparse
from mimetypes import guess_extension
import time


"""
./spidey.py \
	-d test \
	-f 'www.google.com' \
	-u 'https://www.google.com/' \
	-hh '{"Accept" : "application/json"}' \
	-n 2 \
	-m 10

./spidey.py \
	--dir test \
	--filter 'www.google.com' \
	--url 'https://www.google.com/' \
	--headers '{"Accept" : "application/json"}' \
	--depth 2 \
	--max 10
"""

downloaded_urls = []
max_downloads =  100
max_depth = 10
sleep = 0
base_url = None

parser = argparse.ArgumentParser(description='Terrible web spider, but useful for recursive API downloads.')
parser.add_argument('-d', '--dir', dest='dir', metavar="DIR", help="Directory to save to.")
parser.add_argument('-u', '--url', dest='url', metavar="URL", help="The url or api endpint to download.")
parser.add_argument('-b', '--base', dest='base', metavar="URL", help="The base url to use for relative links.")
parser.add_argument('-f', '--filter', dest='filter', metavar="FILTER", help="URL filter to limit recursive API calls.")
parser.add_argument('-hh', '--headers', dest='headers', metavar="HEADERS", help="HTTP Headers.")
parser.add_argument('-n', '--depth', dest='depth', type=int, metavar="DEPTH", help="Recursive depth (Default: {}).".format(max_depth))
parser.add_argument('-m', '--max', dest='max', type=int, metavar="NUM", help="Maximum number of downloads (Default: {}).".format(max_downloads))
parser.add_argument('-s', '--sleep', dest='sleep', type=int, metavar="NUM", help="Pause or sleep time between downloads in secondsi.")
args = parser.parse_args()



def get_ext(content_type):
    ext = guess_extension(content_type.split()[0].rstrip(";"))
    if ext:
        return ext
    elif 'json' in content_type:
        return '.json'
    elif 'html' in content_type:
        return '.html'
    return '.txt'

def find_urls(data, filter):
    results = []
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)
    for url in urls:
        if filter in url:
            results.append(url)

    aurls = re.findall('<a\s+(?:[^>]*?\s+)?href="([^"]*)"', data)
    for aurl in aurls:
        if filter in aurl:
            if aurl.find('http') != 0:
                aurl = base_url + aurl
            results.append(aurl)

    return results

def sanitize(filename):
    valid_chars = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    filename = filename.replace('/', '_')
    filename = filename.replace('?', '..')
    filename = filename.replace('=', '.')
    filename = filename.replace('&', '.')
    filename = filename.replace(';', '-')
    new_name = ''.join(c for c in filename if c in valid_chars)
    if len(new_name) > 1:
        if new_name[0] == '_':
    	    new_name = new_name[1:]
        if new_name[-1] == '_':
    	    new_name = new_name[:-1]
    elif new_name == '_':
        new_name = 'index'
    new_name = new_name[0:125]
    return new_name

def wait():
    if sleep > 0:
        print('Waiting for {} seconds ...'.format(sleep))
        time.sleep(sleep)


def download( url, filter, dir, headers, count_depth=1):
    global max_depth, max_downloads, downloaded_urls
    print('Downloading ({}/{}, {}/{}) {} ...'.format(len(downloaded_urls)+1, max_downloads, count_depth, max_depth, url))
#    print(url, filter, dir)
    ext = '.txt'

    try:
#        req = urllib2.Request(url, headers=headers)
#        data = urllib2.urlopen(req).read()
        resp = requests.get(url, headers=headers)
        content_type = resp.headers['content-type']
        ext = get_ext(content_type)
        try:
            json_data = resp.json()
            if json_data:
                data = json.dumps(json_data, indent=4)
            else:
                data = resp.text
        except Exception as e:
            data = resp.text
    except urllib2.HTTPError as e:
    	msg = '{} for {}'.format(str(e), url)
    	print( msg )
    	data = msg
    except urllib2.URLError as e:
        msg = '{} for {}'.format(str(e), url)
    	print( msg )
    	data = msg
    except requests.exceptions.ConnectionError as e:
        msg = '{} for {}'.format(str(e), url)
    	print( msg )
    	data = msg
    finally:
        downloaded_urls.append(url)

    url_ = urlparse(url)
    file_name = url_.path + (('?' + url_.query) if url_.query else '')
    file_name = sanitize(file_name) + ext
    file_path = os.path.join(args.dir, file_name)

    with open(file_path, 'wb') as f:
        f.write(data.encode('utf8'))

    print('Downloaded to {}'.format(file_path))

    if len(downloaded_urls) >= max_downloads:
        print('\nReached specified maximum downloads {}.\n'.format(max_downloads))
        sys.exit(0)

    urls = find_urls(data, filter)
    print( "{} URLs found.".format(len(urls)) )

    wait()

    count_depth = count_depth+1
    if count_depth <= max_depth:
        for u in urls:
    	    if u not in downloaded_urls:
	            download(u, filter, dir, headers, count_depth)
    else:
        print('\nReached specified maximum depth {}.\n'.format(max_depth))
        sys.exit(0)


def main():
    global max_depth, max_downloads, sleep, base_url
    if args.url == None or args.filter == None or args.dir == None:
        parser.print_help()
    else:
        print ('')
        print('URL: {}'.format(args.url))
        if args.base != None:
          base_url = args.base
        print('Base URL: {}'.format(base_url))
        print('Filter: {}'.format(args.filter))
        print('Directory: {}'.format(args.dir))
        # create header obj
        headers = json.loads(args.headers) if args.headers else {}
        print('Headers: {}'.format(headers))
        print('')
        # depth
        if args.depth != None and args.depth != 0:
            max_depth = args.depth
        # max
        if args.max != None and args.max != 0:
            max_downloads = args.max
        # sleep
        if args.sleep != None and args.sleep != 0:
            sleep = args.sleep
        # Create dir
        mkpath(args.dir)

        try:
            download(args.url, args.filter, args.dir, headers)
        except KeyboardInterrupt as e:
            print('\nAborted by user.')

if __name__ == '__main__':
    main()

