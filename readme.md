
# Introduction

- This is a POC project.

- Runs on mac and linux machine

- Put input file(like ttf , otf etc) in input folder at root of the project



# Running project in node container using docker
- Install docker
- Goto root of the project
- Run command: $ docker pull node:latest
- docker run -v $(pwd):/home/app -w /home/app node npm start subset TTF
- docker run -v $(pwd):/home/app -w /home/app node npm start subset OTF
- docker run -v $(pwd):/home/app -w /home/app node npm start subset EOT
- docker run -v $(pwd):/home/app -w /home/app node npm start subset WOFF
- docker run -v $(pwd):/home/app -w /home/app node npm start subset MultipleFormats
- docker run -v $(pwd):/home/app -w /home/app node npm start convert TTF
- docker run -v $(pwd):/home/app -w /home/app node npm start convert OTF
- docker run -v $(pwd):/home/app -w /home/app node npm start convert EOT
- docker run -v $(pwd):/home/app -w /home/app node npm start convert WOFF
- docker run -v $(pwd):/home/app -w /home/app node npm start convert MultipleFormats

# Running project using docker file
- Install docker on machine
- Goto root of the project
- In terminal run: docker build -t fcas .
- In terminal run: 
    - docker run -v $(pwd)/output:/home/app/output -v $(pwd)/input:/home/app/input fcas convert TTF
    - docker run -v $(pwd)/output:/home/app/output -v $(pwd)/input:/home/app/input fcas convert OTF
    - docker run -v $(pwd)/output:/home/app/output -v $(pwd)/input:/home/app/input fcas convert WOFF
    - docker run -v $(pwd)/output:/home/app/output -v $(pwd)/input:/home/app/input fcas convert EOT
    - docker run -v $(pwd)/output:/home/app/output -v $(pwd)/input:/home/app/input fcas convert MultipleFormats
    - docker run -v $(pwd)/output:/home/app/output -v $(pwd)/input:/home/app/input fcas subset TTF
    - docker run -v $(pwd)/output:/home/app/output -v $(pwd)/input:/home/app/input fcas subset OTF
    - docker run -v $(pwd)/output:/home/app/output -v $(pwd)/input:/home/app/input fcas subset WOFF
    - docker run -v $(pwd)/output:/home/app/output -v $(pwd)/input:/home/app/input fcas subset EOT
    - docker run -v $(pwd)/output:/home/app/output -v $(pwd)/input:/home/app/input fcas subset MultipleFormats

# Running image of the project on another machine
- Install docker on the machine
- Goto root of the project
- In terminal run: docker build -t fcas .
- Export the image as tar file on machine
    - In terminal run: docker save -o <path for generated tar file> <image name>
        - $ docker save -o $(pwd)/fcasimage.tar fcas
- Take the project docker image (in current case fcas) to other machine
- Install docker on other mahine
- Load tar image in docker
    - docker load -i <path to image tar file>
        - docker load -i fcasimage.tar
- In current directory create two folders
    - input: keep input font file like xyz.ttf
    - output: empty folder
- Run: 
    - docker run -v $(pwd)/output:/home/app/output -v $(pwd)/input:/home/app/input fcas convert TTF
    - docker run -v $(pwd)/output:/home/app/output -v $(pwd)/input:/home/app/input fcas convert OTF
    - docker run -v $(pwd)/output:/home/app/output -v $(pwd)/input:/home/app/input fcas convert WOFF
    - docker run -v $(pwd)/output:/home/app/output -v $(pwd)/input:/home/app/input fcas convert EOT
    - docker run -v $(pwd)/output:/home/app/output -v $(pwd)/input:/home/app/input fcas convert MultipleFormats
    - docker run -v $(pwd)/output:/home/app/output -v $(pwd)/input:/home/app/input fcas subset TTF
    - docker run -v $(pwd)/output:/home/app/output -v $(pwd)/input:/home/app/input fcas subset OTF
    - docker run -v $(pwd)/output:/home/app/output -v $(pwd)/input:/home/app/input fcas subset WOFF
    - docker run -v $(pwd)/output:/home/app/output -v $(pwd)/input:/home/app/input fcas subset EOT
    - docker run -v $(pwd)/output:/home/app/output -v $(pwd)/input:/home/app/input fcas subset MultipleFormats





