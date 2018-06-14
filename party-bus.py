import discord
import asyncio

class Party:
    def __init__(self, name, creator, dateTime, location, details):
        self.fieldsList = []
        self.author = creator
        self.yes = set()
        self.no = set()
        self.maybe = set()

        #add basic fields
        self.nameF = Field("Name",name)
        self.creatorF = Field("Created by", creator)
        self.dateF = Field("Date & Time", dateTime)
        self.locationF = Field("Location",location)
        self.detailF = Field ("Description", details)

        #append basic fields
        self.fieldsList.append(self.nameF)
        self.fieldsList.append(self.creatorF)
        self.fieldsList.append(self.dateF)
        self.fieldsList.append(self.locationF)
        self.fieldsList.append(self.detailF)

    def getAuthor(self):
        return self.author

    def addField(self, id, data):
        newF = Field(id, data)
        self.fieldsList.append(newF)

    def removeField(self, id):
        self.fieldsList.remove(id)

    def clearCats(self,entry):
        self.yes.discard(entry)
        self.no.discard(entry)
        self.maybe.discard(entry)

    def addYes(self, entry):
        self.clearCats(entry)
        self.yes.add(entry)

    def addMaybe(self, entry):
        self.clearCats(entry)
        self.maybe.add(entry)

    def addNo(self, entry):
        self.clearCats(entry)
        self.no.add(entry)

    def changeField(self, id, newText):
        for i in self.fieldsList:
            if i == id:
                i.setData(newText)

    def toString(self):
        for i in self.fieldsList:
            i.toString()

class Field:
    def __init__(self,id,data):
        self.id = id
        self.data = data

    def setData(self, newData):
        self.data = newData

    def toString(self):
        print("**" + str(self.id) + "**" + "\t" + str(self.data) +"\n")

class Bot(discord.Client):

    async def on_ready(self):
        print("Death Grips is Online %s"%format(self.user))
        print("Opus Grips is Online: ",format(discord.opus.is_loaded()))
        self.partyList = []

    async def on_message(self, message):
        if message.content.startswith("*create"):
            words = message.content.split(" ",4)
            if len(words) >= 5 :
                newP = Party(words[1]+ "Party"+ str(len(self.partyList)),message.author,words[2],words[3],words[4])
                self.partyList.append(newP)
                print("succ")
            else:
                print("Usage: *create name date location")
        if message.content.startswith("*update"):
            if self.partyList:
                found = False
                i = 0
                while found == False and i <= (len(self.partyList) - 1):
                    if self.partyList[i].getAuthor() == message.author:
                        self.partyList[i].toString()
                        found = True
                if not found:
                    newest = self.partyList[len(self.partyList)-1]
                    newest.toString()
            else:
                print("No parties to update found.")



bot = Bot()
bot.run("Mzg0MjQ3NDE1NzgxMTk1Nzc2.DPwF-g.y80kLdPZZZVIhl00U9a_2sKOnGA")
