FROM node:14.5.0-alpine

COPY / /

RUN cd Samples/TypeScript/Demo && npm install

EXPOSE 5000

WORKDIR /Samples/TypeScript/Demo

CMD [ "npm", "start"]


