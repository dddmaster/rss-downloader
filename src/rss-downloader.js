const winston = require('winston')
const DailyRotateFile = require('winston-daily-rotate-file');
const Parser = require('rss-parser');
const fs = require("fs");
const util = require('util');
var http = require('https');
var cron = require('node-cron');

const logger = winston.createLogger({
    level: 'debug',
    format: winston.format.json(),
    transports: [
      new winston.transports.Console(),
      new DailyRotateFile({
        filename: 'logs/rssdownloader-%DATE%.log',
        datePattern: 'YYYY-MM-DD-HH',
        zippedArchive: true,
        maxSize: '20m',
        maxFiles: '180d'
      })
    ]
  });

const downloadDir = 'files'
const manifestTemplate = downloadDir + '/%s_manifest.json'

function alreadyDownloaded(item, callback) {
    logger.log('debug', "Checking if item " + item.title + " has been downloaded")
    fs.access(util.format(manifestTemplate, item.title), (err) => {
        if(err == null) {
            logger.log('debug', util.format("%s already downloaded", item.title))
            callback(true)
        }
        else {
            callback(false)
        }
    })
}

function addManifest(item) {
    fs.writeFile (util.format(manifestTemplate, item.title), JSON.stringify(item, null, 2), function(err) {
        if (err) throw err;
            logger.info(util.format("Added manifest for %s", item.title))
        });
}

function download(item) {
    !fs.existsSync(downloadDir) && fs.mkdirSync(downloadDir);
    var request = http.get(item.link, function(response){
        var fileName = response.headers['content-disposition'].split('=')[1];
        logger.info(util.format("Downloading file %s", fileName))
        var file = fs.createWriteStream(downloadDir + '/' + fileName);
        response.pipe(file)
        addManifest(item)
    });
}

function processFeedsNoSchedule(urls) {
    urls.forEach(url => {
        logger.info("Parsing URL " + url)
        let parser = new Parser();
        (async () => {
            let feed = await parser.parseURL(url);
            logger.info("Feed Title: "  + feed.title)
            feed.items.forEach(item => {
                logger.info("Item: " + item.title)
                alreadyDownloaded(item, (downloaded) => {
                    if(!downloaded) download(item)
                }); 
            })
        })()
    })
}

function processFeeds(cronSchedule, urls) {
    logger.info("Starting feed procesing with CRON " + cronSchedule)
    logger.info("Feeds to use: " + JSON.stringify(urls))
    processFeedsNoSchedule(urls)
    cron.schedule(cronSchedule, () => {
        processFeedsNoSchedule(urls)
    })
}

module.exports = {
    processFeeds : processFeeds
}