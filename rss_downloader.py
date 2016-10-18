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
import schedule
import time

cron_minute_delay = 10
rss_url = "https://[myurl]"
root_download_dir = "[my_rss_working_dir]"

logging.basicConfig(filename=root_download_dir + '/rssdownloader.log',level=logging.DEBUG, format='%(asctime)s %(message)s')
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
            response = urllib2.urlopen(link)
            entry_file_name = response.headers['content-disposition'].split('=')[1]
            content = response.read()
            f = open(entries_dir + entry_file_name, 'w')
            f.write(content)
            f.close()
            break
        except urllib2.URLError as e:
            attempts += 1
            logging.error(type(e))

    read_file_marker = open(get_read_entry_marker_path(title), "w")
    read_file_marker.write(link)


def run():
    logging.info("Checking feed")
    feed_object = feedparser.parse(rss_url)
    for entry in feed_object.entries:
        if not entry_exists(entry.title):
            logging.info('Downloading ' + entry.title)
            download_entry(entry.title, entry.link)
        else:
            logging.info('Skipping ' + entry.title)

def run_forever():
    run()
    schedule.every(cron_minute_delay).minutes.do(run)
    while 1:
        schedule.run_pending()
        time.sleep(1)

logging.info("Starting up application and running forever")
check_dirs()
run_forever()
logging.info("Stopping")
