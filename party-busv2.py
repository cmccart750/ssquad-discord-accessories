import discord
import asyncio
import datetime

#working emoji list scraped from emojiOne's emoji.json file
#https://github.com/emojione/emojione
#credit for dateutil and dateparser goes here

class Party:
    PARTY_GLOBAL_COUNTER = 0

    #check file for higher counter
    with open("storage2.txt", "r", encoding="utf-8") as fileStore:
        storedID = fileStore.readline().strip()
    if storedID.isnumeric(): PARTY_GLOBAL_COUNTER = int(storedID)

    def __init__(self, creator, id = 0):
        # a confusing set of rules to increment the party by default
        if id == 0 : id = Party.PARTY_GLOBAL_COUNTER + 1
        if id == Party.PARTY_GLOBAL_COUNTER + 1:
            Party.PARTY_GLOBAL_COUNTER += 1
        self.partyID = id
        self.openEdit = False
        self.creatorID = creator
        self.authorList = set()
        self.authorList.add(creator)
        self.fieldList = []
        self.catList = set()

    def getEditPrivacy(self):
        return self.openEdit

    def setEditPrivacy(self, newPriv):
        self.openEdit = newPriv

    def getCreator(self):
        return self.creatorID
    def getID(self):
        return self.partyID

    def addField(self, field):
        print("adding"+field.toString())
        if len(self.fieldList) == 0 or self.fieldList[len(self.fieldList)-1].getCategory() == field.getCategory() or self.catExists(field.getCategory()) == False:
            if self.catExists(field.getCategory()) == False:
                self.addCategory(field.getCategory())
            self.fieldList.append(field)
            print("append")
        else:
            print("not append")
            index = 0
            while self.fieldList[index].getCategory() != field.getCategory() and index < (len(self.fieldList) - 1):
                index+=1
            while self.fieldList[index].getCategory() == field.getCategory() and index < (len(self.fieldList) - 1):
                index+=1
            print(index)
            if isinstance(field, CategoryField):
                index+=1
            self.fieldList.insert(index, field)

    #removes first field with name fieldName (optional: starting in fieldCat)
    def removeField(self, fieldName, fieldCat = ""):
        result = ""
        index = 0
        success = True
        if fieldCat:
            while self.fieldList[index].getCategory() != fieldCat and index < (len(self.fieldList)-1):
                index+=1
            #the only possible last field is a cat header, which you can't delete
            if index == len(self.fieldList)-1:
                result += "Fields of specified Category doesn't exist in party.\n"
        while index < (len(self.fieldList)-1) and self.fieldList[index].getName() != fieldName:
            index +=1
        print(index)
        print("End field:"+str(self.fieldList[index]))
        if index == len(self.fieldList) - 1 and self.fieldList[index].getName() != fieldName:
            result += "Field doesn't exist in party.\n"
            success = False
        if isinstance(self.fieldList[index], CategoryField):
            result += "Category header can't be removed.\n"
            success = False
        if success:
            self.fieldList.remove(self.fieldList[index])
            result += "Field successfully removed."
        print("Result:" + result)
        return result

    #def collapseCat(self, category)
    #path to the first of a cat
    #keep doing removeField at the same index until the next removal isn't in the specified category (unless this gives an error, then traverse a copy of the list)

    def collapseCat(self, category):
        index = 0
        while index <= len(self.fieldList) -1 and self.fieldList[index].getCategory() != category:
            index +=1
        if index == len(self.fieldList):
            print("hit the end of the line")
            return False
        while index != len(self.fieldList) and self.fieldList[index].getCategory() == category:
            self.fieldList.remove(self.fieldList[index])
        return True

    def getCatCount(self, category):
        count = 0
        for i in self.fieldList:
            if i.getCategory() == category:
                count += 1
        return count

    def getCatNames(self, category):
        catList =[]
        for i in self.fieldList:
            if i.getCategory() == category:
                catList.append(i.getName())
        return catList

    def generateEmojis(self, customList):
        emojiList = []
        for i in self.fieldList:
            if isinstance(i, EmojiSetField):
                emoji = i.getTag()
                if emoji.startswith("<"):
                    emoji = emoji[1:(len(emoji)-1)]
                emojiList.append(emoji)
        print(emojiList)
        return emojiList

    #def fieldStillExists()

    def catExists(self, category):
        for i in self.catList:
            if category == i:
                return True
        return False

    def addCategory(self, category):
        category = str(category)
        self.catList.add(category)
        catHeader = CategoryField(category)
        print("tryna add a new category")
        self.addField(catHeader)


    def addReactions(self, emoji, author):
        for i in self.fieldList:
            if isinstance(i, EmojiSetField) and i.getTag() == emoji:
                i.addReact(author)

    def clearCategory(self, category, author):
        for i in self.fieldList:
            if isinstance(i, EmojiSetField) and i.getCategory() == category:
                i.removeReact(str(author))

    def findFieldsByEmoji(self, emoji):
        emoteSetList = []
        for i in self.fieldList:
            if isinstance(i, EmojiSetField) and i.getTag() == emoji:
                emoteSetList.append(i)
        return emoteSetList

    def toString(self):
        result = "Party " + str(self.partyID) + " by " + str(self.creatorID) + "\n"
        for i in self.fieldList:
            result = result + i.toString()
        return result


class Field:
    def __init__(self,name,data,category):
        self.name = name
        self.data = data
        self.category = category

    def setData(self, newData):
        self.data = newData

    def getData(self):
        return self.data

    def getName(self):
        return self.name

    def setName(self, newName):
        self.name = newName

    def getCategory(self):
        return self.category

    def setCategory (self, newCat):
        self.category = newCat

    def toString(self):
        dataStr = str(self.data)
        string =("**" + str(self.name) + "**" + "\t" + dataStr +"\n")
        print(string)
        return string

class EmojiSetField(Field):
    def __init__(self,name,data, category, tag):
        super().__init__(name,data,category)
        self.tag = tag
        self.category = category

    def setTag (self, newTag):
        self.tag = newTag

    def getTag (self):
        return self.tag

    def addReact(self, user):
        self.data.add(user)

    def removeReact(self, user):
        self.data.discard(user)

    def toString(self):
        if len(self.data) == 0: dataStr = "N/A"
        else:
            dataStr = str(self.data)
        string =("**" +self.tag + " " + str(self.name) + "**" + "\t" + dataStr +"\n")
        print(string)
        return string

class CategoryField(Field):
    def __init__(self,name):
        super().__init__(name,"--------", name)


class Bot(discord.Client):

    async def on_ready(self):
        print("Death Grips is Online %s"%format(self.user))
        print("Opus Grips is Online: ",format(discord.opus.is_loaded()))
        server = discord.utils.get(self.servers, name= fileServer)
        channel = discord.utils.get(server.channels, name=fileChannel)
        await self.send_message(channel, "hey(v2)")
        self.partyList = []
        self.autoSaveOld = datetime.datetime.utcnow()
        self.updateOld = datetime.datetime.utcnow()

        #open file to read in old parties
        with open("storage2.txt","r",encoding="utf-8-sig") as fileStore:
            pList = fileStore.read().split("###PARTY###")
            pList.remove(pList[0])
            for i in pList:
                fields = i.split("\n#")
                print("field 0= "+ fields[0])
                header = fields[0].rsplit("#",1)
                newParty = Party(header[0],int(header[1]))
                print("file fields:")
                catName = "catErrorLmao"
                for j in range(1, len(fields)):
                    print(fields[j])
                    print(fields[j].startswith("CAT"))
                    workStr = ""

                    #CategoryFields
                    if fields[j].startswith("CAT"):
                        workStr = fields[j].replace("###DATA###--------",'')
                        workStr = workStr.replace("CAT###NAME###",'')
                        print("cat name:" +workStr)
                        catName = workStr
                    #regular Fields
                    if fields[j].startswith("REG"):
                        workingString = fields[j][13:]
                        workingString = workingString.replace("###DATA###","/")
                        attrs = workingString.split("/",1)
                        newF = Field(attrs[0], attrs[1], catName)
                        newParty.addField(newF)
                    #EmojiSetFields
                    if fields[j].startswith("E_SET"):
                        workingString = fields[j][5:]
                        workingString = workingString.replace("###NAME###","/")
                        workingString = workingString.replace("###DATA###","/")
                        attrs = workingString.split("/",2)
                        print(attrs)
                        tag = attrs[0]
                        if attrs[2].strip() == "set()": attrs[2] = set()
                        newF = EmojiSetField(attrs[1], attrs[2], catName, tag)
                        newParty.addField(newF)
                self.partyList.append(newParty)
            await self.send_message(channel, "printout of current parties:")
            for i in self.partyList:
                await self.send_message(channel, i.toString())


    async def on_message(self, message):


        #keep chat clean
        commandList = ["*update","*create","*delete","*add_field","*add_e_field","*custom_create","*commands","*help"]
        def cleanUpComments(msg):
            botRelated = False

            for i in commandList:
                if msg.content.startswith(i):
                    botRelated = True
                    break

            if str(msg.author) == botName:
                botRelated = True

            return botRelated

        def writePartyToFile(party):
            result = "\n###PARTY###"+ str(party.getCreator()) + "#"+ str(party.getID()) + "\n"
            for i in party.fieldList:
                delimiter = "REG"
                if isinstance(i, EmojiSetField):
                    delimiter = "E_SET" + i.getTag()
                if isinstance(i, CategoryField):
                    delimiter = "CAT"
                stringBuild = "#"+ delimiter + "###NAME###" + i.getName() + "###DATA###" + str(i.getData()) + "\n"
                result += stringBuild
            return result

        def writeListToFile():
            result = str(Party.PARTY_GLOBAL_COUNTER)
            for i in self.partyList:
                result += writePartyToFile(i)
            return result

        def autoSave(old, mindiff):
            new = datetime.datetime.utcnow()
            difference = datetime.timedelta(minutes=mindiff)
            if new - difference >= old:
                print("autosaving since time difference = " + str(new - old))
                with open("storage2.txt","w",encoding="utf-8") as fileStore:
                    fileStore.write(writeListToFile())
                    print("autosave success!")
                old = new
            return old

        self.autoSaveOld = autoSave(self.autoSaveOld, 0.5)

        #autosave/autooverwrite list every 10 minutes, or if it has been 5 minutes since the last *update

        #def writePartyToFile
        #take the tostring and add a couple extra symbols for discerning each field class, and where the name becomes the data
        #def writeListToFile
        #concatenate all the parties with appropriate line breaks. open with a counter of the current number of parties (test separately before the file I/O?)

        #in on_ready, a read file program will need to hopefully understand all the trash we put in
        #encoding = utf-8 on both files should solve any issues, and opening them within with: blocks
        #remember custom emoji need <> stripping - before parsing, get both Notepad to read the writeListToFile output, and python to print it to console, and compare the two.



        def update(partyID):
            party = find(partyID)
            if party:
                return party.toString()
            return "I couldn't find a party with that ID."

        def delete(partyID):
            party = find(partyID)
            if party:
                self.partyList.remove(party)
                return True
            return False

        def find(partyID):
            partyID = int(partyID)
            for i in self.partyList:
                if i.getID() == partyID:
                    return i
            return None


        if message.content.startswith("*create"):
            msg = message.content[7:]
            msgFields = msg.split("/",3)
            for i in msgFields:
                i = i.strip()
            if len(msgFields) == 4:
                #create the fields
                pName = Field("Name",msgFields[0].strip(),"Main")
                pDate = Field("Date",msgFields[1].strip(),"Main")
                pLocation = Field("Location",msgFields[2].strip(),"Main")
                pDescription = Field("Description",msgFields[3].strip(),"Main")

                yes = EmojiSetField("Yes",set(),"Availability","📗")
                maybe = EmojiSetField("Maybe",set(),"Availability","📙")
                no = EmojiSetField("No",set(),"Availability","📕")

                newP = Party(message.author)

                #add  the fields
                newP.addField(pName)
                newP.addField(pDate)
                newP.addField(pLocation)
                newP.addField(pDescription)
                newP.addField(yes)
                newP.addField(maybe)
                newP.addField(no)

                self.partyList.append(newP)
                await self.send_message(message.channel, "Party "+str(newP.getID())+" successfully created")

                #print it out
                partyPrint = update(newP.getID())
                discordPrint = await self.send_message(message.channel, partyPrint)
                print(newP.generateEmojis(self.get_all_emojis()))
                for i in newP.generateEmojis(self.get_all_emojis()):
                    print(i)
                for j in newP.generateEmojis(self.get_all_emojis()):
                   await self.add_reaction(discordPrint, j)
                #update if it's off cooldown
                self.updateOld = autoSave(self.updateOld, 0.2)
                #append party
                with open("storage2.txt", "a", encoding="utf-8") as fileStore:
                    fileStore.write(writePartyToFile(newP))
            else:
                await self.send_message(message.channel, "Could not create party. Usage: \*create  *name*/*date*/*location*/*description*")

        if message.content.startswith("*update"):
            msg = message.content[7:]
            if msg.strip().isnumeric():
                id = int(msg.strip())
                partyPrint = update(id)
                party = find(id)
                discordPrint = await self.send_message(message.channel, partyPrint)
                if party:
                    print(party.generateEmojis(self.get_all_emojis()))
                    for j in party.generateEmojis(self.get_all_emojis()):
                       await self.add_reaction(discordPrint, j)
                #update if it's off cooldown
                self.updateOld = autoSave(self.updateOld, 0.2)
            else:
                await self.send_message(message.channel, "I didn't recognize the party ID you entered. Usage: \*update *ID*")

        if message.content.startswith("*delete"):
            msg = message.content[7:]
            if msg.strip().isnumeric():
                id = int(msg.strip())
                partyPrint = delete(id)
                if partyPrint:
                    await self.send_message(message.channel, "Party " + str(id) + " successfully removed")
                    #update if it's off cooldown
                    self.updateOld = autoSave(self.updateOld, 0.2)
                else:
                    await self.send_message(message.channel, "I couldn't find a party with the ID you entered.")
            else:
                await self.send_message(message.channel, "I didn't recognize the party ID you entered. Usage: \*delete *ID*")

        if message.content.startswith("*add_field"):
            msg = message.content[10:]
            success = False
            error = None
            msgFields = msg.split("/",3)
            if len(msgFields) ==4:
                success = True
                for i in range(0,len(msgFields)):
                    msgFields[i] = msgFields[i].strip()
                    print(msgFields[i])
                #id , name and category need to be non-blanks
                if msgFields[0]=="" or msgFields[1] == "" or msgFields[3] == "":
                    await self.send_message(message.channel, "Party ID, Field Name, and Field Category need to be non-blanks.")
                    success = False
                print(success)
                #field name cannot be the exact same as its category
                if msgFields[1] == msgFields[3]:
                    await self.send_message(message.channel, "Field name cannot be the same as the category it's under.")
                    success = False
                #Category names can't contain forward slashes (is this one possible? consider removeing.)
                if "/" in msgFields[3]:
                    await self.send_message(message.channel, "Category names can't contain forward slashes.")
                    success = False
                #bonus idea: no dupes within a cat?
                party = find(msgFields[0])
                if party and msgFields[1] in party.getCatNames(msgFields[3]):
                    await self.send_message(message.channel, "Field name cannot be the same as any other field inside a category.")
                    success = False
                #id needs to be a number
                if  msgFields[0].isnumeric() == False:
                    await self.send_message(message.channel, "Party ID needs to be a number (no commas,spaces, etc.)")
                    success = False
                #id needs to exist
                if msgFields[0].isnumeric() and find(msgFields[0]) is None:
                    await self.send_message(message.channel, "I couldn't find a party with the ID you entered")
                    success = False
                print(success)
                if success == True:
                    newF = Field(msgFields[1],msgFields[2],msgFields[3])
                    party = find(msgFields[0])
                    if party:
                        party.addField(newF)
            if success:
                await self.send_message(message.channel, "Successfully added a standard field.")
                partyPrint = update(int(msgFields[0]))
                discordPrint = await self.send_message(message.channel, partyPrint)
                if party:
                    for i in party.generateEmojis(self.get_all_emojis()):
                        await self.add_reaction(discordPrint, i)
                #update if it's off cooldown
                self.updateOld = autoSave(self.updateOld, 0.2)
            else:
                await self.send_message(message.channel, "I didn't understand your input.\nUsage: \*add_field *ID*/*Field Name*/*Field Data*/*Field Category*\n")
        # e field react currently works only with custom emojes - try to learn emojiOne to read in all the defaults as a bonus
        if message.content.startswith("*add_e_field"):
            msg = message.content[12:]
            success = False
            msgFields = msg.split("/",3)
            if len(msgFields) == 4:
                for i in range(0,len(msgFields)):
                    msgFields[i] = msgFields[i].strip()
                success = True

                #id , name and emoji need to be non-blanks
                for i in msgFields:
                    if i == "":
                        await self.send_message(message.channel, "All parameters need to be non-blanks.")
                        success = False
                        break

                #check if the last field is an emoji
                #future update: check if all characters in a tag are emotes, to support skin tone mods
                all_emojis = self.get_all_emojis()
                success = False
                print("emoj entered:" + str(msgFields[3]))

                #check list of custom emoji
                for i in all_emojis:
                    print(str(i))
                    print(i.name)
                    print(i.id)
                    if str(i) == msgFields[3]:
                        success = True
                        break

                #check discord's regular emoji
                msgFields[3] = msgFields[3].strip("\\")
                emojiFile = open("emojis_alt.txt","r", encoding = "utf-8")
                content = emojiFile.read()
                if (msgFields[3]) in content:
                    print("found it in the file")
                    success = True

                if success == False: await self.send_message(message.channel, "Character entered for emoji tag needs to be a default emoji, its Unicode equivalent, or a custom emoji")

                #Category names can't contain forward slashes
                if "/" in msgFields[2]:
                    await self.send_message(message.channel, "Category names can't contain forward slashes.")
                    success = False
                #field name cannot be the exact same as its category
                if msgFields[1] == msgFields[2]:
                    await self.send_message(message.channel, "Field name cannot be the same as the category it's under.")
                    success = False

                #bonus idea: no dupes within a cat?
                party = find(msgFields[0])
                if party and msgFields[1] in party.getCatNames(msgFields[2]):
                    await self.send_message(message.channel, "Field name cannot be the same as any other field inside a category.")
                    success = False

                #check for duplicates
                if party and msgFields[3] in party.generateEmojis(all_emojis):
                    await self.send_message(message.channel, "Emoji cannot be a duplicate")
                    success = False

                #id needs to be a number
                if  msgFields[0].isnumeric() == False:
                    await self.send_message(message.channel, "Party ID needs to be a number (no commas,spaces, etc.)")
                    success = False

                #id needs to exist
                if msgFields[0].isnumeric() and find((msgFields[0])) == None:
                    await self.send_message(message.channel, "I couldn't find a party with the ID you entered")
                    success = False

                if success == True:
                    print(msgFields[3])
                    print(str(msgFields[3]))
                    print(type(msgFields[3]))
                    newF = EmojiSetField(msgFields[1],set(),msgFields[2],msgFields[3])
                    if party:
                        party.addField(newF)
            #aftermath
            if success:
                await self.send_message(message.channel, "Successfully added an emoji field.")
                partyPrint = update(int(msgFields[0]))
                discordPrint = await self.send_message(message.channel, partyPrint)
                if party:
                    for i in party.generateEmojis(self.get_all_emojis()):
                        await self.add_reaction(discordPrint, i)
                #update if it's off cooldown
                self.updateOld = autoSave(self.updateOld, 0.2)
            else:
                await self.send_message(message.channel, "I didn't understand your input.\nUsage: \*add_e_field *ID*/*Field Name*/*Field Category*/*Emoji Tag*\n")

        if message.content.startswith("*remove_field"):
            msg = message.content[13:].strip()
            msgFields = msg.split("/",2)
            success = True
            if len(msgFields) >= 2:
                print(msgFields)

                #all parameters need to be filled
                for i in msgFields:
                    if i == "":
                        await self.send_message(message.channel, "All parameters need to be non-blanks.")
                        success = False
                        break

                #id needs to be a number
                party = None
                if msgFields[0].isnumeric() == False:
                    await self.send_message(message.channel, "Party ID needs to be a number (no commas,spaces, etc.)")
                    success = False
                else:
                    party = find(msgFields[0])

                #party with id needs to exist
                if success == False or party == None:
                    await self.send_message(message.channel, "I couldn't find a party with the ID you entered \nCommand Usage: \*remove_field *Party ID*/*Field Category*(Optional)/*Field Name*/")
                else:
                    #attempt to remove
                    if len(msgFields) == 2:
                        cat = ""
                        attempt = party.removeField(msgFields[1], cat)
                    else:
                        attempt = party.removeField(msgFields[2], msgFields[1])
                    if attempt != "Field successfully removed.":
                        attempt += "\nSomething went wrong.\n Command Usage: \*remove_field *Party ID*/*Field Category*(Optional)/*Field Name*/"
                    await self.send_message(message.channel , attempt)
                    partyPrint = update(int(msgFields[0]))
                    discordPrint = await self.send_message(message.channel, partyPrint)
                    for i in party.generateEmojis(self.get_all_emojis()):
                        await self.add_reaction(discordPrint, i)
                    #update if it's off cooldown
                    self.updateOld = autoSave(self.updateOld, 0.2)
            else:
                await self.send_message(message.channel, "\nLess than 2 parameters were entered. \nCommand Usage: \*remove_field *Party ID*/*Field Category*(Optional)/*Field Name*/")

        if message.content.startswith("*remove_category"):
            msg = message.content[16:].strip()
            msgFields = msg.split("/", 1)
            success = False
            if len(msgFields) == 2:
                for i in range (0, len(msgFields)):
                    msgFields[i] = msgFields[i].strip()
                if msgFields[0].isnumeric():
                    party = find(msgFields[0])
                    if party:
                        if party.collapseCat(msgFields[1]):
                            success = True
                            await self.send_message(message.channel, "category successfully collapsed")
                            partyPrint = update(msgFields[0])
                            discordPrint = await self.send_message(message.channel, partyPrint)
                            for i in party.generateEmojis(self.get_all_emojis()):
                                await self.add_reaction(discordPrint, i)
                            #update if it's off cooldown
                            self.updateOld = autoSave(self.updateOld, 0.2)
                    else:
                        await self.send_message(message.channel, "couldn't find the party with specified id")
                else:
                    await self.send_message(message.channel, "party ID needs to be a number")

            if success == False:
                await self.send_message(message.channel, "Usage: \*remove_category *Party ID*/*Field Category*")

    async def on_reaction_add(self, reaction, user):
        print("react added:" + str(reaction))
        print("react added:" + str(reaction.emoji))
        def find(partyID):
            partyID = int(partyID)
            for i in self.partyList:
                if i.getID() == partyID:
                    return i
            return None

        msgAuthor = str(reaction.message.author)
        reactUser = str(user)
        print(botName == reactUser)
        if (reactUser != botName) and msgAuthor == botName and "Party" in reaction.message.content:
            words = (str(reaction.message.content)).split(maxsplit=2)
            pID = int(words[1])
            party = find(pID)
            fields = (party.findFieldsByEmoji(str(reaction.emoji)))
            cats = []
            for i in fields:
                cats.append(i.getCategory())
            for i in cats:
                party.clearCategory(i, reactUser)
            party.addReactions(str(reaction.emoji), reactUser)

    async def on_reaction_remove(self, reaction, user):
        print("react added:" + str(reaction))
        print("react added:" + str(reaction.emoji))
        def find(partyID):
            partyID = int(partyID)
            for i in self.partyList:
                if i.getID() == partyID:
                    return i
            return None

        msgAuthor = str(reaction.message.author)
        reactUser = str(user)
        print(msgAuthor == reactUser)
        if (reactUser != botName) and msgAuthor == botName and "Party" in reaction.message.content:
            words = (str(reaction.message.content)).split(maxsplit=2)
            pID = int(words[1])
            party = find(pID)
            fields = (party.findFieldsByEmoji(str(reaction.emoji)))
            cats = []
            for i in fields:
                cats.append(i.getCategory())
            for i in cats:
                party.clearCategory(i, reactUser)






importantBits = open("launchsteps.txt","r")
token = importantBits.readline().strip("\n")
fileServer = importantBits.readline().strip("\n")
fileChannel = importantBits.readline().strip("\n")
botName = importantBits.readline().strip("\n")
importantBits.close()
bot = Bot()
bot.run(token)

