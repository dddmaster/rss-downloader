# rss-downloader

A simple python script to scan an RSS feed for content and download
any new content that is published.

## Quick install

1. Install dependent python modules

        pip install feedparser
        pip install schedule

2. Download `rss_downloader.py`
3. Modify `rss_downloader.py` with the RSS feed url and the output directory to
place the downloaded content
4. Run `python rss_dowloader.py`

## Installing as systemd service

1. Install dependent python modules

        pip install feedparser
        pip install schedule

2. Download `rss_downloader.py` and place it here `/opt/bin/rss_downloader.py`
3. Modify `rss_downloader.py` with the RSS feed url and the output directory to
place the downloaded content
4. Download the `rss_downloader.service` file and place it here `/etc/systemd/system/rss_downloader.service`
5. Run `sudo service rss_downloader start`
