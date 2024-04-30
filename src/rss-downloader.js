const winston = require('winston')
const DailyRotateFile = require('winston-daily-rotate-file');
const Parser = require('rss-parser');
const fs = require("fs");
const asyncFs = require('fs/promises');
const util = require('util');
var https = require('https');
var cron = require('node-cron');
const sanitize = require('sanitize-filename');
const downloadDir = 'files'
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

const titleToManifestFilePath = (title) => {
    return `${sanitize(title)}.json`
}

const titleToFile = (item) => {
	return `${sanitize(item.title)}.${item.link.split('.').at(-1)}`
}

const fullDownloadPath = (feed) => {
	return downloadDir+'/'+feed.title	
}

const alreadyDownloaded = async (feed,item) => {
    try {
        await asyncFs.access(fullDownloadPath(feed)+'/'+titleToManifestFilePath(item.title), fs.constants.R_OK)
        return true
    } catch(err) {
        logger.log('debug',  `${item.title} not downloaded`)
        return false
    }
}

const addManifest = async (feed,item) => {
    let manifestFileName = titleToManifestFilePath(item.title)
    await fs.writeFile (fullDownloadPath(feed)+'/'+manifestFileName, JSON.stringify(item, null, 2), (err) => { 
        if(err) { 
            logger.error(err)
        }
    });
    logger.info(util.format("Added manifest %s", manifestFileName))
}
const processFeedsNoSchedule = async (urls) => {
    !fs.existsSync(downloadDir) && fs.mkdirSync(downloadDir);
    await Promise.all(urls.map(async (url) => {
        logger.info("Parsing URL " + url)
        let parser = new Parser();
        let feed = await parser.parseURL(url);
        logger.info("Feed Title: "  + feed.title)
        logger.info(`Items in Feed ${feed.items.length}`)
        !fs.existsSync(fullDownloadPath(feed)) && fs.mkdirSync(fullDownloadPath(feed));
        await Promise.all(feed.items.map(async (item) => {
            const isAlreadyDownloaded = await alreadyDownloaded(feed,item)
            if(!isAlreadyDownloaded) {
                    https.get(item.link, response => {
                    addManifest(feed,item)
                    var fileName = titleToFile(item);
                    logger.info(util.format("Downloading file %s", fileName))
                    var file = fs.createWriteStream(fullDownloadPath(feed) + '/' + fileName);
                    response.pipe(file)
                })
            }
        }))
    }))
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