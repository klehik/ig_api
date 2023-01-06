# ig_api

A simple Python package to publish content using Instagram Graph API. Expired access token is refreshed automatically.

# Installation 

```python
pip install git+https://github.com/klehik/ig_api

```

# Usage

```python
import ig_api

```

## Credentials
### Create .env file for Instagram credentials. Package updates this file when refreshing expired access token.

```python
ACCESS_TOKEN=
INSTAGRAM_ACCOUNT_ID= #user's instagram account 
CLIENT_ID= #client id from meta developer portal
CLIENT_SECRET= #client secret from meta developer portal
PAGE_ID= #facebook page id
IG_USERNAME= #ig username
```

## Authentication

```python
env_path = '.env'
auth = ig_api.Authentication(env_path=env_path)

```

## Posting
Instagram media needs to be on a public server

Single url creates a normal post, multiple urls(up to 10) creates a Carousel post

```python
urls = ['https://exapmle.com/example.jpg', 'https://exapmle2.com/example2.mp4']
caption = 'test post'
api = ig_api.API(auth)
api.create_post(urls=urls, caption=caption)

```

## Refreshing access token if expired

```python
refresher = ig_api.AccessTokenRefresh(auth)
refresher.access_token_refresh()

```





