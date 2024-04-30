# rss-downloader

Based on https://github.com/WhiteBoardDev/rss-downloader with minor adjustments

## Quick Run

```
docker run -e RSS_URLS=example.com/feed.rss dddmaster/rss-downloader:latest
```

logs will be written to `logs` and all downloaded files will be written to `files`