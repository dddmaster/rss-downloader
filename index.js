'use strict'

process.on('SIGINT', function() {
    process.exit();
});

const rssDownloader = require('./src/rss-downloader')
rssDownloader.processFeeds(process.argv[2], process.argv.slice(3))