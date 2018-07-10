import praw
import re
import datetime
import os
import sys
from .ReadMessages import getRedditInstance
from .ReadMessages import getInfoLine

#def getRedditInstance():
#    # Read reddit client_id and client_secret from file (to avoid accidentally publishing it)
#    inputFile = open(os.path.join(os.path.dirname(__file__), "RedditAPIAccess.txt"))
#    lines = []
#    for line in inputFile:
#        lines.append(line)
#    client_id = lines[0]
#    client_secret = lines[1]
#    username = lines[2]
#    password = lines[3]
#
#    # Get reddit instance
#    reddit = praw.Reddit(client_id=client_id.rstrip(), 
#                         client_secret=client_secret.rstrip(), 
#                         user_agent='linux:geoguessr_posting_bot:0.1 (by /u/LiquidProgrammer',
#                         username=username.rstrip(),
#                         password=password.rstrip())
#
#    return reddit

def lookForRemoveRequests(onlyConsoleOutput=True):
    reddit = getRedditInstance()

    messages = [message for message in reddit.inbox.unread()]

    validSubjects = ["removerequest"]

    print("Looking for remove requests.")

    for message in messages:
        if message.subject.lower().strip().replace(' ', '') in validSubjects:
            #messageContent = [entry for entry in message.body.split('\n') if entry.strip() is not '']
            messageId = message.body.strip()
            print("Found remove request for this id: " + messageId + " from this user: " + str(message.author))
            removeMessage(messageId, message.author, onlyConsoleOutput)
            if not onlyConsoleOutput:
                message.mark_read()
                

def removeMessage(idToBeRemoved, fromUser, onlyConsoleOutput=True):
    reddit = getRedditInstance()

    print("Trying to remove post with id: " + idToBeRemoved + ". Listing all current requests:")

    # Get the unread messages from the reddit account
    messages = [message for message in reddit.inbox.unread()]

    subreddit = reddit.subreddit("geoguessr")

    validSubjects = ["postrequest", "postingrequest"]

    foundMessage = False

    
    # Iterate through the messages
    for message in messages:
        if message.subject.lower().strip().replace(' ', '') in validSubjects:
            originalMessageContent = [("    " + entry.strip()) for entry in message.body.split('\n')]
            messageContent = [(entry.strip()) for entry in message.body.split('\n') if entry.strip() is not '']
            if message.id == idToBeRemoved:
                print("\u001b[31m -> ", end = "")
                title = "Succesfully Removed Request"
                body = "ID of Removed Message: " + idToBeRemoved + "\n\nThis was the body of the message:\n\n" + '\n'.join(originalMessageContent) + '\n' + getInfoLine()
                if not onlyConsoleOutput:
                    fromUser.message(title, body)
                print("Sending this message, title: " + title + '\n:' + body)
                foundMessage = True
                if not onlyConsoleOutput:
                    message.mark_read()
            print(str(messageContent[3]) + " by " + str(message.author) + " with id: " + message.id + "\u001b[0m")

    if not foundMessage:
        title = "Unsuccesful Remove of Request"
        body = "I could not find a request message with ID: " + idToBeRemoved + ". Perhaps you already had sent a remove request? Or maybe the post is already online?\n\n" + getInfoLine()
        if not onlyConsoleOutput:
            fromUser.message(title, body)
        print("Sending this message, title: " + title + '\n:' + body)



if __name__ == '__main__':
    lookForRemoveRequests(onlyConsoleOutput=False)
    #removeMessage("ak4ul1")
