'use strict'

process.on('SIGINT', function() {
    process.exit();
});

const rssDownloader = require('./src/rss-downloader')
let urls = process.env.RSS_URLS;

if (urls == undefined) {
	console.log("Missing env RSS_URLS, aborting")
	process.exit(1);
}

if (urls.includes(',')) {
	urls = urls.split(',');
} else {
	urls = [urls];
}

rssDownloader.processFeeds("0 * * * * *", urls)