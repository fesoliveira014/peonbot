import telegram
import random
import youtube
import imgur
import imghdr
import dice
import feedparser as rss

class PeonBot():
    readyStrings = ['Ready to work!']
    whatStrings = ['Yes?', 'Hmmm?', 'What you want?']
    yesStrings = ['I can do that.', 'Be happy to.', 'Work, work.', 'Okidoki']
    noStrings = ["I can't do that.", "You stupid?", "Not right..."]
    pissedStrings = ['Whaaat?', 'Me busy. Leave me alone!', 'No time for play.', 'Me not that kind of orc!', 'Stop poking me! Well, that was okay.']

    options = ["start", "poke", "wow", "image", "gif", "youtube", "dice"]
    jokeStrings = ["I come from the Orcs. We eat with spoons and forks. We love to eat our pork!",
             "It's not easy being green.",
             "Orc smash!",
             "Man, dawg, you know, it's like I'm feeling you, but I'm not feeling you, you know?",
             "I will CRUSH and DESTROY and... ooo... shiny..."]

    helpMessage = """ Something need doing, chieftan? Just say what you want and I be ready to do!

    Here is what I can do:

    /image   - I can get pretty picture
    /gif     - Hey, this picture moves!
    /youtube - Videos? What be that?
    /dice    - Wanna play some dice?
    /wow     - I hear gossip in the mines sometimes
    /poke    - Stop being annoying
    /joke    - I'm scarry but I can be funny too
    """

    def __init__(self, token = "139023611:AAEOQk5pOVBJrwceKMtCxvEV99_weyCbQYY"):
        self.token = token
        self.bot = telegram.Bot(token)
        try:
           self.lastUpdate = self.bot.getUpdates()[-1].update_id
        except IndexError:
            self.lastUpdate = None

    def startBot(self):
        while True:
            for update in self.bot.getUpdates(offset = self.lastUpdate, timeout=10):
                chat_id = update.message.chat_id
                message = update.message.text

                if message:
                    if(message.startswith('/')):
                        command, _, arguments = message.partition(' ')
                        #print('arguments: ' + arguments)
                        if command == '/start':
                            self.bot.sendMessage(chat_id=chat_id, text=PeonBot.readyStrings[0])

                        elif command == '/poke':
                            rand = random.randint(0, len(PeonBot.pissedStrings)-1)
                            self.bot.sendMessage(chat_id=chat_id, text=PeonBot.pissedStrings[rand])

                        elif command == '/wow':
                            rand = random.randint(0, len(PeonBot.yesStrings)-1)
                            self.bot.sendMessage(chat_id=chat_id, text=PeonBot.yesStrings[rand])
                            url = self.getWowNews()
                            self.bot.sendMessage(chat_id=chat_id, text=url)

                        elif command == '/joke':
                            rand = random.randint(0, len(PeonBot.jokeStrings)-1)
                            self.bot.sendMessage(chat_id=chat_id, text=PeonBot.jokeStrings[rand])

                        elif command == '/help':
                            self.bot.sendMessage(chat_id=chat_id, text=PeonBot.helpMessage)

                        elif command[1:] in PeonBot.options:
                            if arguments != '':
                                rand = random.randint(0, len(PeonBot.yesStrings)-1)
                                self.bot.sendMessage(chat_id=chat_id, text=PeonBot.yesStrings[rand])
                                if command == '/image':
                                    url = self.getImage(arguments)
                                    if url != '':
                                        self.bot.sendPhoto(chat_id=chat_id, photo=url)
                                    else:
                                        self.bot.sendMessage(chat_id=chat_id, text="Got nothin.")    

                                elif command == '/gif':
                                    url = self.getGif(arguments)
                                    if url != '':
                                        self.bot.sendPhoto(chat_id=chat_id, photo=url)
                                    else:
                                        self.bot.sendMessage(chat_id=chat_id, text="Got nothin.")    

                                elif command == '/youtube':
                                    videoName, videoURL = self.getYoutube(arguments)
                                    self.bot.sendMessage(chat_id=chat_id, text=videoName + ' ' + videoURL)

                                elif command == '/dice':
                                    roll = self.rollDice(arguments)
                                    self.bot.sendMessage(chat_id=chat_id, text="Roll " + arguments + ": " + str(roll))

                            else:
                                rand = random.randint(0, len(PeonBot.noStrings)-1)
                                self.bot.sendMessage(chat_id=chat_id, text=PeonBot.noStrings[rand] + " (You need to give some information.)")

                        else:
                            rand = random.randint(0, len(PeonBot.whatStrings)-1)
                            self.bot.sendMessage(chat_id=chat_id, text=PeonBot.whatStrings[rand])    
                            
                    else:
                        rand = random.randint(0, len(PeonBot.whatStrings)-1)
                        self.bot.sendMessage(chat_id=chat_id, text=PeonBot.whatStrings[rand])

                    self.lastUpdate = update.update_id + 1

    def getImage(self, query):
        return imgur.get(query)

    def getGif(self, query):
        return imgur.get(query, gif=True)

    def getYoutube(self, query):
        result = youtube.search(query)
        name = result['snippet']['title']
        url = "https://youtu.be/" + result['id']['videoId']
        return name, url

    def rollDice(self, dices):
        roll = dice.roll(dices)
        diceSum = 0

        for element in roll:
            diceSum += element

        return diceSum

    def getWowNews(self):
        url = rss.parse('http://www.mmo-champion.com/external.php?do=rss&type=newcontent&sectionid=1&days=120&count=10')['items'][0]['link']
        return url

def test_icc_profile_images(h, f):
    if h.startswith(b'\xff\xd8') and h[6:17] == b'ICC_PROFILE':
        return "jpeg"

def main():
    peon = PeonBot()
    peon.startBot()

if __name__ == '__main__':
    imghdr.tests.append(test_icc_profile_images)
    main()