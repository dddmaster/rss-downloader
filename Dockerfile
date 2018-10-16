FROM jfloff/alpine-python:2.7-slim

COPY dist/rss_downloader.par /rss_downloader.par
RUN mkdir /downloads

ENTRYPOINT /rss_downloader.par -o /downloads -u $FEED_URL
