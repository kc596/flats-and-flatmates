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


### TODO
1. Create frontend using data in database to show the output.
2. Code is written in hurry so it's not properly refactored. Refactor it whenever there's free time.
3. Find better way of crawling recent post only. Research ways/APIs to find the same.


    If you face any problem in using this program or find any error, feel free to create an issue. I will try my best to look into it in my free time.


This project can crawl any facebook group in general and filter out post with specific keywords not containing exception words defined in config.
