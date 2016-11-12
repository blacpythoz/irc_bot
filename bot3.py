#! /usr/bin/env python3
# -*- coding: utf8 -*-
# To do # Factorize code with classes and threds

import weather
import nepali_date
from connector import Connection
import time


# This is class bot it can to anythings
class Bot():
    
    #connection object
    bot = ""

    #User info
    users={}

    #local user to whom bot sents the message
    luser=""

    #xada work kolist
    words = ["mugi","muj","randi","fuck","chikney","rando","kera","machis","lado","puti","muj"]

    # Message when user type !fuck
    fuckMessage = "You ass hole, Mother Fucker"

    def bot_reply(self,message):
        msg = message.split(' ')
        print(message)
        # the message starts with ! marks then it is command
        if msg[0][0] == "!":
            # Just for fun
            if msg[0] == "!fuck":
                self.sendMsg(self.fuckMessage)

            # Provides the date 
            elif msg[0] == "!date":
                date = nepali_date.get_nepali_date()
                self.sendMsg(date)

            # Sends the weather info to user
            elif msg[0] == "!weather":
                if len(msg) == 2:
                    condition = weather.get_weather(msg[1])
                    self.sendMsg(condition)
                else:
                    self.sendMsg("Enter the city as  !weather Kathmandu")

            # Change bot name through admin
            elif self.luser == self.bot.getadmin() and msg[0] == "!botnick":
                if len(msg) == 2:
                    self.bot.irc_send("NICK {}".format(msg[1]))
                else:
                    self.sendMsg("Enter name of bot properly")

            # Change fuck message
            elif self.luser == self.bot.getadmin() and msg[0] == "!fuckmsg":
                if len(msg) == 2:
                    self.fuckMessage = msg[1]
                else:
                    self.sendMsg("Enter the message as !fuckmsg [MESSAGE]")

            # Provides help to the user
            elif msg[0] == "!help":
                self.sendMsg(" Currently available commads are !date, !weather [location], !fuck  [Admin Only] : !fuckmsg [MSG] !botnick [NAME]  kill bot")

            # Exit the bots
            elif self.luser == self.bot.getadmin() and message == "kill bot":
                self.bot.irc_send("QUIT")

            else:
                self.sendMsg("Unknown command: Type !help for more info")

    def analyzeText(self,msg):
        # Respond ping message
        if msg.find("PING :") != -1:
            ping_value = msg.split(":")[1]
            self.bot.irc_send("PONG :{}".format(ping_value))

        if msg.find("PRIVMSG {}".format(self.bot.getchannel())) != -1:
            self.luser = msg.split('!')[0][1:]
            message = msg.split('PRIVMSG',1)[1].split(':',1)[1]
            self.bot_reply(message)

        self.testKick(msg)

    # Kick user if the speak rude words
    # Function determines whether to kick the guy or not
    def testKick(self,msg):
        if any(word in msg for word in self.words):
            if self.luser in self.users:
                self.users[self.luser] += 1
                if self.users[self.luser] == 4:
                    self.bot.irc_send("PRIVMSG chanserv :op ##linuxnepal")
                    time.sleep(2)
                    self.bot.irc_send("KICK {} {}".format(self.bot.getchannel(),self.luser))
                    time.sleep(1)
                    self.bot.irc_send("PRIVMSG chanserv :deop ##linuxnepal")
                if self.users[self.luser] == 0:
                    return
                self.sendMsg("You have {} chances".format(4 - self.users[self.luser]))
            else:
                self.users[self.luser] = 0

    # THis functions sent the message to user directly
    def sendMsg(self,msg):
        self.bot.irc_send_priv("{} {}".format(self.luser,msg))

    def run(self):
        self.bot = Connection()
        self.bot.main()
        while True:
            buffer_msg = self.bot.irc_buffer_msg()
            self.analyzeText(buffer_msg)
            print(buffer_msg)
 
if __name__ == "__main__":
    bot = Bot()
    bot.run()

