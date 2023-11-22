FROM node:12.18.0-alpine3.11

ENV PROJECT_ROOTDIR /app/web_ui/

WORKDIR $PROJECT_ROOTDIR

COPY ./web_ui/package.json $PROJECT_ROOTDIR

RUN yarn install

COPY ./web_ui $PROJECT_ROOTDIR
