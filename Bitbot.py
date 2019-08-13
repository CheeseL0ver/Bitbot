import time, requests as req, os
from flask import Flask, request
from json import dumps
from json import loads
from json import load

app = Flask(__name__)
GOOGLE_CHAT_WEBHOOK = os.getenv('GOOGLE_CHAT_WEBHOOK')
DISCORD_CHANNEL_WEBHOOK = os.getenv('DISCORD_CHANNEL_WEBHOOK')
webhooks = []

# Handle the POST from Bitbucket
@app.route('/', methods=['POST'])
def webhook():
  #print(request.get_json())
  json = request.get_json()
  #print(json)

  webhooks = []
  generateMessages(json)
  sendMessages()

  time.sleep(1)


  return "SUCCESS", 200

def getPhotoURL():
    result = req.get('https://picsum.photos/200?grayscale').url

    return result

def sendMessages():
    for webhook in webhooks:
        print(webhook)
        #print(webhook[0] + '\n' + webhook[1])
        #req.post(webhook[0],data=dumps(webhook[1]))
        req.post(webhook[0],json=(webhook[1]))

def generateMessages(json):
    commitMessage = json['push']['changes'][0]['new']['target']['message'].strip('\n')
    commitAuthor = json['actor']['display_name']
    repoName = json['repository']['name']
    commitLink = json['push']['changes'][0]['new']['target']['links']['html']['href']
    photoUrl = getPhotoURL()

    buildChat(commitMessage,commitAuthor,repoName,commitLink,photoUrl)
    buildDiscord(commitMessage,commitAuthor,repoName,commitLink,photoUrl)

def buildChat(commitMessage,commitAuthor,repoName,commitLink,photoUrl):
  if GOOGLE_CHAT_WEBHOOK == None:
      return

  card = None
  with open('card.json') as fp:
      card = load(fp)

  card['cards'][0]['sections'][1]['widgets'][0]['textParagraph']['text'] = commitMessage
  card['cards'][0]['sections'][0]['widgets'][0]['keyValue']['content'] = commitAuthor
  card['cards'][0]['sections'][0]['widgets'][1]['keyValue']['content'] = repoName
  card['cards'][0]['sections'][2]['widgets'][0]['buttons'][0]['textButton']['onClick']['openLink']['url'] = commitLink
  card['cards'][0]['sections'][0]['widgets'][2]['image']['imageUrl'] = photoUrl
  	
  #print(card)
  webhooks.append((GOOGLE_CHAT_WEBHOOK,card))

def buildDiscord(commitMessage,commitAuthor,repoName,commitLink,photoUrl):
    if DISCORD_CHANNEL_WEBHOOK == None:
        return

    discord = None
    with open('discord.json') as fp:
        discord = load(fp)

    discord['embeds'][0]['description'] = commitMessage
    discord['embeds'][0]['url'] = commitLink
    discord['embeds'][0]['author']['name'] = commitAuthor
    discord['embeds'][0]['image']['url'] = photoUrl

    #print(discord)
    webhooks.append((DISCORD_CHANNEL_WEBHOOK,discord))

#if __name__ == '__main__':
#    app.run()
