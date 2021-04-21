# Docker / Usage

## Build docker image
`docker build --tag tweepy-stream-img .`

## Run built image as container
### Default
`docker run tweepy-stream-img`

### Detatched mode
#### Run 
`docker run -d -it --name tweepy_container tweepy-stream-img`
* `-d`: detatched
* `--name`: optional for easy identification of container/instance
* `-it`: interactive terminal setup for later docker commands. for details see https://stackoverflow.com/a/41918607

#### Inspect running containers
`docker ps`

#### Atatch
`docker attach tweepy_container`
Exit this without stopping the container by CTRL-p and CTRL-q. (`-it` flag is mandatory to use this!)

#### Start/Stop container
`docker start tweepy_container`

`docker stop tweepy_container`

#### Explore container with shell
`docker exec -it tweepy_container bash`
