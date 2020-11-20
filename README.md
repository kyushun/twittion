# twittion
## Install Guide

### 1. pip
```
pip install -r requirements.txt
```

### 2. heroku
https://devcenter.heroku.com/articles/heroku-cli

### 3. Redis
```
brew install redis
```

### 4. env
```
heroku plugins:install heroku-config
heroku config:pull
```

### Run
```
redis-server
heroku local
```
Access to http://localhost:5000/
