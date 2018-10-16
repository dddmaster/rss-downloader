FROM node:latest
RUN mkdir /rss-downloader
WORKDIR /rss-downloader 
ADD . ./
RUN npm install
ENTRYPOINT node index.js "$CRON_SCHEDULE" "$FEED_URL"
