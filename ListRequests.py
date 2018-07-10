import praw
import re
import datetime
import os
import sys
from .ReadMessages import getRedditInstance
from .ReadMessages import getInfoLine

def lookForShowRequests(onlyConsoleOutput=True):
    reddit = getRedditInstance()

    messages = [message for message in reddit.inbox.unread()]

    validSubjects = ["showmyrequests", "showrequests"]
    validSubjectsAll = ["showallmymessages", "showallmyrequests", "showallrequests", "showallmessages"]

    print("Looking for show requests.")

    for message in messages:
        subject = message.subject.lower().strip().replace(' ', '')
        if subject in validSubjects:
            print("Found a show request from " + str(message.author))
            sendMessageWithRequests(message.author, showAll=False, onlyConsoleOutput=onlyConsoleOutput)
            if not onlyConsoleOutput:
                message.mark_read()
        if subject in validSubjectsAll:
            print("Found a show all request from " + str(message.author))
            sendMessageWithRequests(message.author, showAll=True, onlyConsoleOutput=onlyConsoleOutput)
            if not onlyConsoleOutput:
                message.mark_read()

def sendMessageWithRequests(forRedditor, showAll, onlyConsoleOutput=True):
    reddit = getRedditInstance()
    validSubjects = ["postrequest", "postingrequest"]

    # Get the unread messages from the reddit account
    if showAll == False:
        messages = [message for message in reddit.inbox.unread() if message.subject.lower().strip().replace(' ', '') in validSubjects and message.author == str(forRedditor)]
    else:
        messages = [message for message in reddit.inbox.messages() if message.author == str(forRedditor)]

    subreddit = reddit.subreddit("geoguessr")

    # Format all the messages into one string 
    creatingList = '\n\n'.join([str(index + 1) + getMessageMetaString(message, not showAll) +
        prefix4Spaces(message.body) for index, message in enumerate(messages)])


    print("Sending this message to " + str(forRedditor) + ": ")
    print(str(creatingList))

    if not onlyConsoleOutput:
        forRedditor.message("Request List", "Found " + str(len(messages)) + " messages: \n\n" + creatingList)

def prefix4Spaces(text):
     return '\n'.join(["    " + line for line in text.split('\n')])

def getMessageMetaString(message, addRemoveLink=False):
    
    m_subject = "\\. Message Title: `" + message.subject + "`"
    m_id = " Message ID: `" + message.id + "`"
    m_date = " Sent: `" +  str(datetime.datetime.fromtimestamp(message.created)) + "`"
    m_sep = "\n\n"
    m_remove_link = ""

    if addRemoveLink:
        m_remove_link = " <- [Remove This Requst](https://www.reddit.com/message/compose/?to=GeoGuessrBot&subject=Remove%20Request&message=" + message.id + ')'

    return m_subject + m_id + m_date + m_remove_link + m_sep
    


if __name__ == '__main__':
    lookForShowRequests(onlyConsoleOutput=False)
    #removeMessage("ak4ul1")
