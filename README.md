# rss-downloader

A simple node script to scan an RSS feed for content and download any new content that is
published.

## Quick install

```
npm install
node index.js "*/30 * * * * *" https://myrssfeed.blarg/feed.rss
```

You can also give more arguments for many more feeds

```
node index.js "*/30 * * * * *" https://myrssfeed.blarg/feed.rss https://myrssfeed.blarg/feed2.rss https://myrssfeed.blarg/feed3.rss 
```

logs will be written to `logs` and all downloaded files will be written to `files`

## Running as a docker container

  `docker build -t rss-downloader .`
  `docker run -e FEED_URL=<url> -v /path/to/files:/rss-downloader/files -v /path/to/logs:/rss-downloader/logs`
