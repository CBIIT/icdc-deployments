#ARG ECR_REPO
#FROM ${ECR_REPO}/base-images:node-16.17.0
FROM node:16.17.0-alpine3.16
ENV PORT 4030
ENV NODE_ENV production
WORKDIR /usr/src/app
COPY package*.json ./
#RUN npm ci --only=production
RUN npm install
COPY  --chown=node:node . .
EXPOSE 4030
CMD [ "node", "./bin/www" ]
