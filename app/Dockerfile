FROM node:20.6.0

WORKDIR /app
RUN npm cache clean --force
COPY package.json ./
COPY package-lock.json ./

# Print installed npm packages
RUN echo "Hello, world!"
RUN npm list --depth=0

RUN npm install

# Print installed npm packages
RUN echo "Hello, world!"
RUN npm list --depth=0

RUN npm install -g react-scripts
ENV PATH /app/node_modules/.bin:$PATH
COPY . ./
EXPOSE 3000

CMD ["npm", "start"]