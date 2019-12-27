# twitter-webhook-bot
Automatically creates a connection to the twitter accountActivity webhook using a ngrok connection and flask


# Steps
- install the modules from 'requirements.txt'
- apply for a developer account (https://developer.twitter.com/en/apply-for-access)
- create a new Twitter app (https://developer.twitter.com/en/apps)
- create a new dev env (https://developer.twitter.com/en/docs/basics/developer-portal/guides/dev-environments)
- put your credentials in 'credentials.py' (https://developer.twitter.com/en/apps/ and then click details)
- that's it! now you can just use start.py and the bot should be running

# Quick explanation

In **'start.py'** a new ngrok connection is created,flask ('bot.py') starts,a new webhook is created with the ngrok url and a subscription to webhook is initiated.
  
So if you need to make changes you can modify 'bot.py' to get all the following events from Account Activity :

- Tweets (by user)
- Tweet deletes (by user)
- @mentions (of user)
- Replies (to or from user)
- Retweets (by user or of user)
- Quote Tweets (by user or of user)
- Retweets of Quoted Tweets (by user or of user)
- Likes (by user or of user)
- Follows (by user or of user)
- Unfollows (by user)
- Blocks (by user)
- Unblocks (by user)
- Mutes (by user)
- Unmutes (by user)
- Direct Messages sent (by user)
- Direct Messages received (by user)
- Typing indicators (to user)
- Read receipts (to user)
- Subscription revokes (by user)

more here : https://developer.twitter.com/en/docs/accounts-and-users/subscribe-account-activity/overview



**this project was made for linux and mac users** because it uses os.system()

windows users need to **remoove** or **comment out** all threading methods and start flask and ngrok on their own


also if you need anything contact me at : lennyisnan@gmail.com, bye!
