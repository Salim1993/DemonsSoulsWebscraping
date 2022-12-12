## About

Downloads demons souls wiki webpages and scrapes the data into database. \
the database is used in the other projects.

## Install
Clone the repo and insert a db file called `demon_souls.db` at the root of the project. 

To install python packages run virtual environement. Here commmands for windows. 

```
py -3 -m venv .venv
.venv\scripts\activate
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Next install the following packages 

`beautifulsoup4, requests, sqlalchemy, pytest`

Project is now setup, and you run in it from `main.py`.
