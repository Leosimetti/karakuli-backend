# Karakuli backend
This is the server side of the application, written using FastApi.

## Features:
1. **Lesson types** - Lessons are split into Radicals, Kanji, Words, Grammar.
1. **Study lists** - users are able to combine lessons into lists available to others.
1. **SRS-reviews** - users can add lessons from their current study list as perosnal reviews to study them later using SRS.
1. **Jwt-authentication** - authentication via jwt-token. To be used by the mobile app
1. **Cookie-authentication** - TBD

## Available settings (env variables)
+ **JWT_SECRET_KEY** - secret key used for authentication
+ **DB_HOST** - database url (preferably use async protocols)
+ **BEKA_DB** - self-hostefd database url (DB_HOST is used if not set)
+ **HOST_IP** - the app IP
+ **PORT** - the app port

## DB schema (the image is clickable):
[![image](https://user-images.githubusercontent.com/42554566/127744390-62b20b3a-8a8b-40c8-ba12-171b91ce0c57.png)](https://dbdiagram.io/d/60b9d692b29a09603d17f068)


## How to start:
Run *main.py*
