# FROM ubuntu:16.04

# RUN apt-get update
# RUN apt-get install -y software-properties-common
# RUN apt-get install -y libstdc++6
# RUN apt-get install -y curl

# # Install Node.js
# RUN curl --silent --location https://deb.nodesource.com/setup_8.x | bash -
# RUN apt-get install -y nodejs
# RUN apt-get install -y build-essential
FROM node:10.10.0

WORKDIR /home/app

# install dependency
#ADD package.json .
COPY package*.json ./
# Include .npmrc file in project if there are monotype library dependencies like @monotype/xyz libray
# ADD .npmrc . 
RUN npm install

COPY . .

ENTRYPOINT ["npm","start"]
