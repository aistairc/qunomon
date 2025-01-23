FROM node:22-alpine3.19

ENV PROJECT_ROOTDIR /app/web_ui/

WORKDIR $PROJECT_ROOTDIR

COPY ./web_ui/package.json $PROJECT_ROOTDIR

RUN yarn install

COPY ./web_ui $PROJECT_ROOTDIR
