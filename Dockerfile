FROM node:current-alpine
RUN mkdir /rss-downloader
WORKDIR /rss-downloader 
ADD index.js ./index.js
ADD package.json ./package.json
ADD ./src ./src/
RUN npm install
ENTRYPOINT node index.js
