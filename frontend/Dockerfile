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

# Copy code
COPY assets/ /app/assets/
COPY components/ /app/components/
COPY layouts/ /app/layouts/
COPY static/ /app/static/
COPY store/ /app/store/
COPY pages/ /app/pages/
COPY plugins/ /app/plugins/
COPY nuxt.config.js jsconfig.json utils.js /app/

# start command
RUN yarn build
# CMD [ "yarn", "dev" ]
CMD [ "yarn", "start" ]
