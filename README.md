# Flats and Flatmates

### Motivation

Searching a flat/flatmate in cities like Bengaluru is quite challenging. Brokerage is very high (generally 1 month rent). Fortunately, there are few facebook groups with aim for finding flats and flatmates. 

### Problem

There are many active Flats/Flatmates group and the frequency of posts in these groups are very high. Adding to this, most of the post are addressed to different location than we are looking for. Facebook APIs cannot be used for these groups to get required data unless you are an admin.

## UI crawling and automation to rescue!
The crawler will browse mentioned facebook groups (in config) and check if the post contains any of mentioned keywords and not any exception words. If yes, the *link to post*, *time of posting*, *time of crawling* and *keywords that match* are stored in sqllite3 datbase.

### Steps to setup and use
1. Install Python3
2. Run command : ***pip install -r requirements.txt***  &nbsp; in root of project.
3. Set parameters in ***config/config.yaml*** file and your facebook credentials in ***config/credentials.yaml*** file.
4. Place ***chromedriver*** in drivers folder according to your operation system. [From here](http://chromedriver.chromium.org/downloads)
5. Run ***python main.py***

### CAUTION
1. ```'male only'``` keyword and exceptions in config will also match ```'female only'``` because the later contains the first.
   You can use spaces to handle these situation i.e., ```' male only'```.
2. Facebook might detect unusual activity from your account if you overuse the crawler. 
   It might log you out and restrict certain features of your account (example: like, comments, etc.) for some time. 
   I won't be responsible for any harm done due to this application.  

### TODO
1. Find better way of crawling recent post only. Research ways/APIs to find the same.
2. Automatic chromedriver download.
3. Regular expression instead of keyword match.

```
If you face any problem in using this program or find any error, feel free to create an issue. I will try my best to look into it in my free time.
```

This project can crawl any facebook group in general and filter out post with specific keywords not containing exception words defined in config.
