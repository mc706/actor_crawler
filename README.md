# Actor Crawler
This project is a highspeed website crawler that is designed to take advantage of the actor model in order to quickly 
crawl your website in search of broken links. Unlike a serial spider, this can handle ~1000 links per minute depending
on your internet connection, the site speed, and the hardware you are running on.

It is written in python, using thespian.py for the actor model code.

## Install
Setup instructions on a mac

1. Clone the repo,
```
git clone https://github.com/mc706/actor_crawler.git
```
2. Create a virtualenv
```
mkvirtualenv actor_crawler -p ~/.pyenv/versions/3.6.0/bin/python
```
3. Install python requirements
```
pip install -r requirements.txt
```
4. [Optional] Ensure Phantomjs is installed
```
brew install phantomjs
```

## Setup:
1. Create a folder in the `sites` directory with no spaces: ie: `test_com`
2. Inside of your new folder, create a `config.yaml` file
3. fill the file with the following
```
key: test_com
name: Test.com
domain: http://www.test.com
check_third_party: False
screen_shot: False
output_links: True
entry_points:
  - http://www.test.com
  - http://www.test.com/secret
```

Replacle the above sections as you see fit.

## Running:
This system is setup for scale, so to get it running, you need to start the communication network first, start your job, the close the network once you are done.

1. run `make start`
2. run `python crawler.py test_com`
3. wait for output
4. run `make stop`

* Note if your run fails in the middle, or you want to start again but you are getting an address already in use error, try `killall python`

## Reporting:
There are a few outputs of the run.

Whenever you do a run, it will create a timestamped folder of inside of your directory that has a `pages.json` and a `report.txt`.