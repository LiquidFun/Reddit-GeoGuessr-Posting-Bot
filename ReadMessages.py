import praw
import re
import datetime
import os
import sys

def getRedditInstance():
    # Read reddit client_id and client_secret from file (to avoid accidentally publishing it)
    inputFile = open(os.path.join(os.path.dirname(__file__), "RedditAPIAccess.txt"))
    lines = []
    for line in inputFile:
        lines.append(line)
    client_id = lines[0]
    client_secret = lines[1]
    username = lines[2]
    password = lines[3]

    # Get reddit instance
    reddit = praw.Reddit(client_id=client_id.rstrip(), 
                         client_secret=client_secret.rstrip(), 
                         user_agent='linux:geoguessr_posting_bot:0.1 (by /u/LiquidProgrammer',
                         username=username.rstrip(),
                         password=password.rstrip())

    return reddit

def readMessages():
	reddit = getRedditInstance()

	# Get the unread messages from the reddit account
	messages = [message for message in reddit.inbox.unread()]

	subreddit = reddit.subreddit("geoguessr")

	# Iterate through the messages
	for message in messages:
		if "postrequest" in message.subject.lower().strip().replace(' ', ''):
			messageContent = [entry.strip() for entry in message.body.split('\n') if entry.strip() is not '']

			# If the message has too few lines then skip it
			if len(messageContent) < 4:
				print(messageContent)
				print("Too few lines in post request. Quitting.\n")
				continue

			# If the message has a message left by the author then post a challenge
			if len(messageContent) > 4:
				messageContent.insert(4, "---")

			messageContent.insert(4, "### [Challenge link](%s)" % messageContent[2])

			messageContent.append(getInfoLine())

			if messageContent[0] <= datetime.datetime.now().strftime("%Y-%m-%d %H:%M") <= messageContent[1]:
				#print(messageContent[4:])
				postText = ""
				for message in messageContent[4:]:
					postText += message + '\n\n'
				print(postText)

				#subreddit.submit(messageContent[2], selftext = postText, send_replies = false)



def getInfoLine():
    return """---

^(I'm a bot, message the author: /u/LiquidProgrammer if I made a mistake.) ^[Usage ](I'll make a post soon)."""

if __name__ == '__main__':
    readMessages()
