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

cron_minute_delay = 10
rss_url = "https://[myurl]"
root_download_dir = "[my_rss_working_dir]"
logger = logging.getLogger("rssLogger")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(root_download_dir + '/rssdownloader.log', maxBytes=50000,backupCount=5)
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
logger.addHandler(handler)
entries_dir = root_download_dir + "/entries/"
read_entry_marker_dir = root_download_dir + "/marked_as_read/"

def check_dirs():
    if not os.path.isdir(root_download_dir):
        os.mkdir(root_download_dir)
    if not os.path.isdir(entries_dir):
        os.mkdir(entries_dir)
    if not os.path.isdir(read_entry_marker_dir):
        os.mkdir(read_entry_marker_dir)

def get_read_entry_marker_path(title):
    return read_entry_marker_dir + base64.b64encode(title)

def entry_exists(title):
    return os.path.isfile(get_read_entry_marker_path(title))

def download_entry(title, link):
    attempts = 1
    while attempts < 3:
        try:
            response = urllib2.urlopen(link, timeout=5)
            entry_file_name = response.headers['content-disposition'].split('=')[1]
            content = response.read()
            f = open(entries_dir + entry_file_name, 'w')
            f.write(content)
            f.close()
            break
        except urllib2.URLError as e:
            attempts += 1
            logger.error(type(e))

    read_file_marker = open(get_read_entry_marker_path(title), "w")
    read_file_marker.write(link)


def run():
    logger.info("Checking feed")
    try:
        resp = requests.get(rss_url, timeout=10.0)
    except requests.ReadTimeout:
        logger.warn("Timeout when reading RSS %s", rss_url)
        return
    # Put it to memory stream object universal feedparser
    content = BytesIO(resp.content)
    feed_object = feedparser.parse(content)
    for entry in feed_object.entries:
        if not entry_exists(entry.title):
            logger.info('Downloading ' + entry.title)
            download_entry(entry.title, entry.link)
        else:
            logger.info('Skipping ' + entry.title)

def run_forever():
    run()
    schedule.every(cron_minute_delay).minutes.do(run)
    while 1:
        schedule.run_pending()
        time.sleep(1)

logger.info("Starting up application and running forever")
check_dirs()
run_forever()
logger.info("Stopping")
