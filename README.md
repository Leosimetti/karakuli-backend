# Karakuli backend
This is the server side of the application, written using FastApi.
## Features:
1. **Study lists** - users are able to combine words into lists available to others.
2. **SRS-reviews** - users can add words from study lists to their perosnal reviews to study them later using SRS.
3. **Jwt-authentication** - authentication via jwt-token. To be used by the mobile app
4. **Cookie-authentication** - TBD

## Available setting (env variables)
+ **JWT_SECRET_KEY** - secret key used for authentication
+ **DB_HOST** - database url (preferably use async protocols)

## How to start:
Run *main.py*
