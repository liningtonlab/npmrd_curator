FROM node:10

# Create app directory
WORKDIR /app
COPY package.json yarn.lock /app/

# global install & update
RUN npm i -g npm

# RUN yarn
RUN yarn
# RUN yarn build

ENV HOST 0.0.0.0
EXPOSE 3000

# start command
# CMD [ "yarn", "dev" ]
CMD [ "yarn", "start" ]
