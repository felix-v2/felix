FROM node:20.6.0

WORKDIR /app
COPY package.json ./
COPY package-lock.json ./
RUN npm install
RUN npm install -g react-scripts
ENV PATH /app/node_modules/.bin:$PATH
COPY . ./
EXPOSE 3000

CMD ["npm", "start"]