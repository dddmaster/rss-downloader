# rss-downloader

A simple python script to scan an RSS feed for content and download any new content that is
published.

## Quick install

1. Download `rss_downloader.par` from the releases of this repo.
2. run it as an executable `rss_downloader.par -o <my-download-dir> -u <http://my-site.com/my-rss-feed.xml>`

## Installing as systemd service

1. Download `rss_downloader.par` and place it here `/opt/bin/rss_downloader.par`
3. Download the `rss_downloader.service` file and place it here
   `/etc/systemd/system/rss_downloader.service`
4. Edit `rss_downloader.service` and point the downloader to the appropriate download directory
   and URL.
5. Run `sudo service rss_downloader start`


## Logging and Debugging

Logs are written to `path/to/download/directory/rssdownloader.log` and will detail what is seen in
the rss feed, what is downloaded, and what isn't.

## Testing

Run `python test_cases.py` to run some basic tests. Tests will spin up a web server with some
hosted RSS feeds and content to confirm the appropriate behavior of the downloader.


## Building

  `bazel build :rss_downloader.par`

## Testing

  `bazel test :test_rss_downloader`
