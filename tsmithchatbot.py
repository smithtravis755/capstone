######################################
# 
# Travis Smith Capstone Program
# 
# Simple chatbot AI
# 
# 
#######################################

# Various imports
# String formatting
import string
from string import maketrans
# Random numbers
import random
# Date and time
import time

# Initialize global variables
global f
global inp
global currWord
global prevGreet

f = open('dbfile.txt', 'r+')     # Main database file



######################################
#
# findGreet()
# Searches through the text file for the next entry
# Itterates over itself to find the user input
# returns the next entry found in the database
#
######################################

def findGreet( ):

    cont = True

    # Loop until : marking the word is found    
    while (cont == True):
        nex = f.read(1)
        if (nex == ':'):
            break
        # Marks the end of the file, return nothing
        elif (nex == '*'):
            return
        else:
            pass

    # init to empty string
    greet = ""

    # Loop concatenates the string together
    while (cont == True):
        try:
            nex = f.read(1)
            if (nex == '\"'):
                cont = False
            else:
                greet = greet + nex
                
        # Exit if the end of the file is reached
        except EOFError:
            print "End of file error; check database file"
            return

    # Returns the found word
    return greet



######################################
#
# searchDB(currWord, prevOcc)
# Searches the file for the phrase most similar to the user input
# by counting the number of words that occur in each
# Itterates over itself multiple times to continue searching
# @currWord: current word with highest number of occurences
# @prevOcc: the number of similar words from most similar phrase
# returns entry with most words similar to the user's input
#
######################################

def searchDB( currWord, prevOcc ):

    prevNum = prevOcc

    # Finds the next phrase in the DB
    greet = findGreet()

    # Returns -1 if no matching response were found, or currWord if the end of the file was reached
    if (greet == None):
        if (prevOcc == 0):
            return -1
        else:
            return currWord


    # A blank translation table and a list of all punctuation; used to remove punctuation
    trantab = maketrans("", "")
    punct = string.punctuation

    # Load greet and user response into new strings
    inputSearch = inp
    greetSearch = greet

    # Changes to lowercase and removes punctuation
    inputSearch = inputSearch.lower()
    inputSearch = inputSearch.translate(trantab, punct)
    greetSearch = greetSearch.lower()
    greetSearch = greetSearch.translate(trantab, punct)

    # Tokenizes the input and the word to be searched
    inputSearch = inputSearch.split()
    greetSearch = greetSearch.split()

    # Initialize counters to 0
    loopIn = 0
    loopGreet = 0
    occurence = 0


    # Reinitialize to 0
    loopIn = 0
    loopGreet = 0

    # Checks for the number of occurences of each word in the user phrase
    # with those in the database
    while loopIn < len(inputSearch):
        while loopGreet < len(greetSearch):
            if inputSearch[loopIn] == greetSearch[loopGreet]:
                occurence = occurence + 1
            loopGreet = loopGreet + 1
        loopIn = loopIn + 1
        loopGreet = 0

    # If the new statement is more similar than previous,
    # replace the old currWord with the new statement
    if (occurence > prevNum):
        currWord = greet
        ans = searchDB(currWord, occurence)
        return ans
        
    # Or else keep the previous statement
    elif (occurence < prevNum):
        ans = searchDB(currWord, prevNum)
        return ans
    
    # Or use the shortest statement if they are tied
    elif (occurence == prevNum):
        if (len(currWord) < len(greet)):
            ans = searchDB(currWord, prevNum)
            return ans
        elif (len(currWord) >= len(greet)):
            currWord = greet
            ans = searchDB(currWord, occurence)
            return ans


    

######################################
#
# findResp(resp)
# Uses the users input to find a response
# Recursively calls to find correct input, then chooses random response
# @resp: the users input that a response must be found for
# returns a random response from list of possible responses
#
######################################


def findResp( resp ):

    # Finds next phrase in the database
    greet = findGreet()

    # Initialize to base values
    words = ""
    cont = True
    listLoop = True
    respList = []
    randNum = 0
    listPos = 0

    # If the correct phrase is found, search for first response
    if (greet == resp):
        while (f.read(1) != ';'):
            pass
    # If wanted phrase is not found, recursively call findResp again
    else:
        words = findResp(resp)
        return words

    # Loop through all possible responses
    while (listLoop == True):      

        cont = True
        # Read letter by letter to make first response
        while (cont == True):
            nex = f.read(1)
            if (nex == '\"'):
                cont = False
            else:
                words = words + nex

        # Add response to list of responses
        respList.insert(listPos, words)
        listPos = listPos + 1
        words = ''

        # Loop until next response is found, or all response have been found
        nex = f.read(1)
        while (nex != ';' and nex != "%"):
            nex = f.read(1)

        if (nex == '%'):
            listLoop = False
            break

    # Produces a random number based on the size of the list
    # Note: Last entry in list will be chosen less than others
    randNum = random.random()
    outp = randNum * len(respList)

    # If asked about the day/time, give the current date and time
    if (respList[int(outp)] == "___"):
        respList[int(outp)] = time.asctime( time.localtime(time.time()) )

    return respList[int(outp)]


######################################
#
# learning(corrResp)
# Adds new greetings/responses to the database
# When user says response is incorrect, asks for an appropriate response
# and adds that to the database of possible responses from user's greeting
# @corrResp: correct response the user gave
#
######################################

def learning( corrResp ):

    # Initialize variables
    cont = True
    greetFound = True
    cont2 = True
    testWord = ""
    greetStore = ""
    testF = ''
    testChar = ''
    itr1 = 0         # Used as a pseudo pointer to keep track of location in a string
    global prevGreet
    tempDB = ""
    nextChar = ' '
    stringDB = ""

    # Creates a string for storage purposes
    f.seek(0)
    stringDB = f.read()
    tempDB = f.read()

    # A blank translation table and a list of all punctuation; used to remove punctuation
    trantab = maketrans("", "")
    punct = string.punctuation

    # Store previous user entry for later use
    greetStore = prevGreet

    # Change previous entry to lowercase and remove punctuation
    prevGreet = prevGreet.lower()
    prevGreet = prevGreet.translate(trantab, punct)

    itr1 = 23    # First greeting starts around 25; this places the pointer just before
    
    # Copies main database file into Temp and adds user greeting/response
    while (cont == True):

        testF = stringDB[itr1]
        itr1 = itr1 + 1

        # Read until : marking next greeting is found
        if (testF == ':'):
            testWord = ""
            cont2 = True

            # Make the greeting letter by letter
            while (cont2 == True):
                testF = stringDB[itr1]
                itr1 = itr1 + 1

                if (testF == '\"'):
                    cont2 = False
                else:
                    testWord = testWord + testF

            # Change the greeting to lowercase and remove punctuation
            testWordTemp = testWord.lower()
            testWordTemp = testWordTemp.translate(trantab, punct)

            # If they are the same word for word, add user response as the new first response
            if (prevGreet == testWordTemp):
                tempDB = stringDB[:itr1] + "\"\n\t\t\t[\";" + corrResp + "\", " + stringDB[itr1+6:]  ######
                itr1 = itr1 + 15

                # Mark that the correct greeting was found
                greetFound = False

            # Else, they are not the same so iterate through to add user greeting/response to end of
            # database
            else:
                tempDB = stringDB[:itr1] + ":" + testWord + "\"\n\t\t}" + stringDB[itr1+1:]

        # If no more greetings are found and a matching greeting was not found,
        # enter the user greeting/response to the end of the file
        elif (testF == '*' and greetFound == True):

            # Moves back 9 characters for proper spot to enter new data
            itr1 = itr1 - 9
            tempDB = stringDB[:itr1] + "\t}\n\t\t{\n\t\t\":" + greetStore + "\"\n\t\t\t[\";" + corrResp + "\"]%,\n\t\t}\n\t]\n}\n*"
            cont = False
            break

        # If no more greetings are found and a matching greeting was found, end
        elif (testF == '*' and greetFound == False):
            cont = False
            break

        # If not the end and not a : marking the next greeting, copy the next letter and continue
        else:
            pass

    # Clear out database file and rewrite with stringDB, for any changes
    f.seek(0)
    f.truncate(0)
    f.write(tempDB)

    print("Response stored.")

    
    
######################################
#
# Main
# Where user talks with chatbot
#
######################################

print "To start, type anything. If a response is incorrect, say \"inc resp\""
print "To quit, press ctrl+c"

# Generic loop to repeat user input/response
while True:

    try:

        # Reset to beginning of the file
        f.seek(10)

        # Take in user input
        inp = raw_input("")
        inp = inp.lower()

        # User input marks previous response as incorrect
        if (inp == "inc resp"):

            # Ask for new response, then call learning to add it to Database
            print("Please enter a correct response: ")
            newResp = raw_input("")
            learning(newResp)

        # User does not say previous response was incorrect
        else:
         
            currWord = ""
            prevGreet = inp # Stores user input as previous response, for learning

            # Search DB for what the user said
            inp = searchDB(currWord, 0)

            # If no matching greetings were found, ask for an appropriate response
            if (inp == -1):

                print "I do not recognize that phrase. What would an appropriate response be?"
                inp2 = raw_input("")
                learning(inp2)

            # Or else find an appropriate response and print it
            else:
                # Reset to the beginning of the file
                f.seek(10)

                # Find proper response to user input
                out = findResp(inp)

                # Output
                print out


    #Break on errors or ctrl + c
    except (KeyboardInterrupt, EOFError, SystemExit):
        f.close()
        break
    
