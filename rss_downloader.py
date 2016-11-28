# Rss auto downloader
#
# First time setup:
#   pip install feedparser
#   pip install schedule
#
#
# If you have systemd to control services then you can make this a
# service by creating a file at /etc/systemd/system/rss_downloader.service
# with the following contents
#
#[Unit]
#Description=runs the rss_downloader
#
#[Service]
#ExecStart=/usr/bin/python /opt/bin/rss_dowloader.py
#
#[Install]
#WantedBy=multi-user.target
#
#
import feedparser
import os
import base64
import urllib2
import logging
import requests
from io import BytesIO
from logging.handlers import RotatingFileHandler
import schedule
import time
import getopt
import sys

class RssDownloader:

    def __init__(self, root_download_dir, rss_urls):
        self.root_download_dir = root_download_dir
        self.entries_dir = root_download_dir + "/entries/"
        self.read_entry_marker_dir = root_download_dir + "/marked_as_read/"
        self.rss_urls = rss_urls
        logger = logging.getLogger("rssLogger")
        logger.setLevel(logging.DEBUG)
        handler = RotatingFileHandler(root_download_dir + '/rssdownloader.log', maxBytes=50000,backupCount=5)
        handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        logger.addHandler(handler)
        self.logger = logger
        self.cron_minute_delay = 10
        self.check_dirs()
        self.logger.info("Rss downloader initialized to " + self.root_download_dir)

    def check_dirs(self):
        if not os.path.isdir(self.root_download_dir):
            os.mkdir(self.root_download_dir)
        if not os.path.isdir(self.entries_dir):
            os.mkdir(self.entries_dir)
        if not os.path.isdir(self.read_entry_marker_dir):
            os.mkdir(self.read_entry_marker_dir)

    def get_read_entry_marker_path(self, title):
        return self.read_entry_marker_dir + base64.b64encode(title)

    def entry_exists(self, title):
        return os.path.isfile(self.get_read_entry_marker_path(title))

    def download_entry(self, title, link):
        attempts = 1
        while attempts < 3:
            try:
                response = urllib2.urlopen(link, timeout=5)
                entry_file_name = title
                if response.headers.has_key('content-disposition'):
                    entry_file_name = response.headers['content-disposition'].split('=')[1]
                content = response.read()
                f = open(self.entries_dir + entry_file_name, 'w')
                f.write(content)
                f.close()
                read_file_marker = open(self.get_read_entry_marker_path(title), "w")
                read_file_marker.write(link)
                break
            except urllib2.URLError as e:
                attempts += 1
                self.logger.error(type(e))

    def run(self):
        for rss_url in self.rss_urls:
            self.logger.info("Checking feed %s", rss_url)
            try:
                resp = requests.get(rss_url, timeout=10.0)
            except Exception as e:
                self.logger.warn("Problem downlading RSS %s", rss_url)
                self.logger.warn(e)
                return
            # Put it to memory stream object universal feedparser
            content = BytesIO(resp.content)
            feed_object = feedparser.parse(content)
            for entry in feed_object.entries:
                if not self.entry_exists(entry.title):
                    self.logger.info('Downloading ' + entry.title)
                    self.download_entry(entry.title, entry.link)
                else:
                    self.logger.info('Skipping ' + entry.title)
            self.logger.info("Done checking feed %s", rss_url)

    def run_forever(self):
        self.logger.info("Starting up application and running forever")
        self.run()
        schedule.every(self.cron_minute_delay).minutes.do(self.run)
        while 1:
            schedule.run_pending()
            time.sleep(1)


def main(argv):
    rss_urls = []
    root_download_dir = ""

    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'rss_downloader.py -o <outputdir> -u <url> [-u <url>...]'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'rss_downloader.py -o <outputdir> -u <url> [-u <url>...]'
            sys.exit()
        elif opt in ("-u", "--url"):
            rss_urls.append(arg)
        elif opt in ("-o", "--outputdir"):
            root_download_dir = arg
    rss_downloader = RssDownloader(root_download_dir, rss_urls)
    rss_downloader.run_forever()

if __name__ == '__main__':
    main(sys.argv[1:])
